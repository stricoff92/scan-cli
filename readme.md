# Linux CLI Document Management System

## Features
 - SANE backend for scanning images
 - Tesseract OCR engine for searching scanned documents
 - Single & multiple document scan mode
 - Search documents with arbitrary meta tags

<hr>

```bash
# set env variable
export SCANNER_DEFAULT_DEVICE='escl:http://localhost:60000'

# add bin to path
export PATH="$PATH:/path/to/scan-cli/bin"

# install OCR engine
sudo apt install tesseract-ocr
```

```bash
# scan options

-n --name outfile_name_root    # file name root
-l --labels label1 label2 ...  # meta data labels for the document(s)
-r --resolution 75|150|300     # DPI value (default = 150)
-o --ocr                       # process with OCR engine (default = No)
-m --many                      # scan multiple pages (default = No)
-c --color                     # color mode

# scan usage
doccli scan
doccli scan --resolution 300
doccli scan -n 'paystub-feb-2023-1' --ocr
doccli scan -n 'paystub-feb-2023-1' -l 2023 paystub 'XYZ Corp'
doccli scan -n 'tax-return-2023' -l 2023 tax --many

```

```bash
# show all tags in use
doccli tags
```

```bash
# list files options

-f --fullpaths # show full paths

doccli files
doccli files --fullpaths
```

```bash
# show all files in doccli's data directory
doccli ls
```

<hr>

![](document.gif)

