
"""
    Frontend for SANE scanimage program
"""

import argparse
from collections import Counter
from copy import deepcopy
import datetime as dt
import json
import os
import os.path
import pathlib
import re
import sys
from typing import List, Optional
import uuid


USABLE_RESOLUTIONS = (
    75, 150, 300
)
USABLE_MODES = (
    'Gray', 'Color'
)
OUT_DIR = os.path.join(pathlib.Path(__file__).parent, 'data')


def get_default_file_name():
    return 'scan_at_' + dt.datetime.now().strftime("%Y-%m-%d_%H:%M") + "_" + str(uuid.uuid4())[:6]

def clean_ocr_text(v: str) -> str:
    text = ""
    for l in v.split("\n"):
        text += ''.join(c for c in l if ord(c) <= 127) + " "
    return re.sub(' +', ' ', text)

def apply_macros(file_name_root: str) -> str:
    name = deepcopy(file_name_root)
    if 'DATE' in name:
        name = name.replace("DATE", dt.date.today().strftime('%b_%d_%Y'))
    if 'TIME' in name:
        name = name.replace("TIME", dt.datetime.now().strftime('%H-%M-%S'))
    if 'UID' in name:
        name = name.replace("UID", str(uuid.uuid4())[:6])
    return name


def command_scan(
    device: str,
    file_name: Optional[str],
    labels: List[str],
    resolution: int,
    ocr: bool,
    many: bool,
    color: bool,
    verbose: bool,
):
    original_cwd = None

    out_file_name = file_name if file_name is not None else get_default_file_name()
    if '.' in out_file_name:
        print("error: file name cannot contain '.'")
        sys.exit(128)

    if ' ' in out_file_name:
        print("error: file name cannot contain ' '")
        sys.exit(128)

    out_file_name = apply_macros(out_file_name)

    command = f"scanimage -d '{device}' --resolution {resolution} --mode {'Color' if color else 'Gray' }"
    if many:
        # Scan multiple pages
        for i in range(1, 200):
            full_out_file = os.path.join(OUT_DIR, out_file_name) + f"_{i}.jpeg"
            if os.path.exists(full_out_file):
                print(f"error: file name exists {out_file_name}")
                sys.exit(128)
        command += (
            f' --batch-prompt --batch=\'{out_file_name + "_%d.jpeg"}\' --format=jpeg'
        )

        original_cwd = os.getcwd()
        if verbose:
            print("RUNNING COMMAND: cd " + OUT_DIR)
        os.chdir(OUT_DIR)

    else:
        # Scan a single page
        full_out_file = os.path.join(OUT_DIR, out_file_name) + ".jpeg"

        if os.path.exists(full_out_file):
            print(f"error: file name exists {out_file_name}")
            sys.exit(128)

        command += (
            f' -o \'{full_out_file}\''
        )

    if verbose:
        print("RUNNING COMMAND: " + command)
    elif not many:
        command += " > /dev/null 2>&1"
    exit_code = os.system(command)
    if verbose:
        print("exit code ", exit_code)
    if original_cwd:
        if verbose:
            print("RUNNING COMMAND: cd " + original_cwd)
        os.chdir(original_cwd)

    # write meta data files
    if many:
        pass
    else:
        meta_file_full_path = full_out_file + ".meta.json"
        data = {
            'created': dt.datetime.now().isoformat(),
            'labels':labels,
        }
        if ocr:
            ocr_out_file = f'/tmp/{uuid.uuid4()}'
            ocr_command = f'tesseract {full_out_file} {ocr_out_file}'
            if verbose:
                print("RUNNING COMMAND: " + ocr_command)
            else:
                ocr_command += " > /dev/null 2>&1"
            exit_code = os.system(ocr_command)
            if verbose:
                print("exit code", exit_code)
            with open(ocr_out_file  + ".txt") as f:
                data['ocr'] = clean_ocr_text(f.read())
            os.remove(ocr_out_file + ".txt")
        with open(meta_file_full_path, 'w') as f:
            json.dump(data, f)

def command_list_files(fullpaths: bool):
    for fname in os.listdir(OUT_DIR):
        if re.search('\.\S+\.meta.json$', fname):
            continue # skip meta data files
        if not bool(re.search(r'\S+\.\S+$', fname)):
            continue # skip files that don't look like foooo.bar
        has_meta_data = os.path.exists(
            os.path.join(OUT_DIR, fname + ".meta.json")
        )
        meta_data = {}
        if has_meta_data:
            with open(os.path.join(OUT_DIR, fname + ".meta.json")) as fp:
                meta_data = json.load(fp)
            if 'ocr' in meta_data:
                meta_data['ocr'] = True
            else:
                meta_data['ocr'] = False

        print(
            os.path.join(OUT_DIR, fname) if fullpaths else fname,
            meta_data,
        )


def command_list_tags():
    counts = Counter()
    for fname in os.listdir(OUT_DIR):
        if fname.endswith(".meta.json"):
            with open(os.path.join(OUT_DIR, fname)) as fp:
                data = json.load(fp)
            for label in data['labels']:
                counts[label] += 1

    counts = [(k, v) for k, v in counts.items()]
    counts.sort(key=lambda t: t[1], reverse=True)
    for (k, v) in counts:
        print(v, k)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command")
    parser.add_argument("--verbose", "-v", action="store_true", default=False)
    args, _ = parser.parse_known_args()

    if args.verbose:
        print("OUT_DIR", OUT_DIR)
        print('SCANNER_DEFAULT_DEVICE', os.environ.get('SCANNER_DEFAULT_DEVICE'))

    if args.command == 'scan':

        device_name = os.environ['SCANNER_DEFAULT_DEVICE']

        parser = argparse.ArgumentParser()
        parser.add_argument("command")
        parser.add_argument("--verbose", "-v", action="store_true", default=False)
        parser.add_argument("--name", "-n", default=None)
        parser.add_argument("--labels", "-l", nargs='*', default=[])
        parser.add_argument("--ocr", "-o", action='store_true', default=False)
        parser.add_argument("--many", "-m", action='store_true', default=False)
        parser.add_argument("--resolution", "-r", default="150", type=int)
        parser.add_argument("--color", "-c", action="store_true", default=False)
        args = parser.parse_args()

        if args.resolution not in USABLE_RESOLUTIONS:
            print(f"Error: invalid resolution. Use: {USABLE_RESOLUTIONS}")
            sys.exit(128)

        if args.verbose:
            print('arguments ', args)
        command_scan(
            device_name,
            args.name,
            args.labels,
            args.resolution,
            args.ocr,
            args.many,
            args.color,
            args.verbose,
        )

    elif args.command == 'ls':
        print("contents of ", OUT_DIR)
        os.system(f"ls -lh {OUT_DIR}")

    elif args.command == 'tags':
        if args.verbose:
            print('arguments ', args)
        command_list_tags()

    elif args.command == 'files':
        parser = argparse.ArgumentParser()
        parser.add_argument("command")
        parser.add_argument("--verbose", "-v", action="store_true", default=False)
        parser.add_argument("--fullpaths", "-f", action="store_true", default=False)
        args = parser.parse_args()
        if args.verbose:
            print('arguments ', args)

        command_list_files(args.fullpaths)

    else:
        print("Error: unknown command")
        sys.exit(128)

if __name__ == "__main__":
    main()
