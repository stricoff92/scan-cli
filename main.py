
"""
    scancli scan [--name name] [-label label, ...] [--ocr]
"""

import argparse
import datetime as dt
import os
import os.path
import pathlib
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

def command_scan(
    device: str,
    file_name: Optional[str],
    labels: List[str],
    resolution: int,
    ocr: bool,
    many: bool,
    color: bool,
):
    original_cwd = None

    out_file_name = file_name if file_name is not None else get_default_file_name()
    if '.' in out_file_name:
        print("error: file name cannot contain '.'")
        sys.exit(128)

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

    print("executing command " + command)
    os.system(command)
    if original_cwd:
        os.chdir(original_cwd)

    # write meta data files
    if many:
        pass
    else:
        meta_file_full_path = os.path.join(
            OUT_DIR, full_out_file + ".json"
        )


def main():
    print("Parsing arguments")

    parser = argparse.ArgumentParser()
    parser.add_argument("command")
    args, _ = parser.parse_known_args()

    if args.command == 'scan':

        device_name = os.environ['SCANNER_DEFAULT_DEVICE']

        parser = argparse.ArgumentParser()
        parser.add_argument("command")
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

        command_scan(
            device_name,
            args.name,
            args.labels,
            args.resolution,
            args.ocr,
            args.many,
            args.color
        )



if __name__ == "__main__":
    main()
