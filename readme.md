# Linux CLI Document Management System

## Features
 - Uses SANE backend
 - Single & multiple document mode
 - Saved documents are searchable via:
   - meta tags
   - OCR text

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
-n --name file name                  # file name root
-l --labels label1 label2 .. labeln  # meta data labels for the document(s)
-o --ocr                             # process with OCR engine (default = No)
-m --many                            # scan multiple pages (default = No)
-r --resolution 75|150|300           # DPI value (default = 150)
-c --color Gray|Color                # color mode (default = Gray)

# scan usage
scancli scan
scancli scan --resolution 300
scancli scan -n 'paystub-feb-2023-1' --ocr
scancli scan -n 'paystub-feb-2023-1' -l 2023 paystub 'XYZ Corp'
scancli scan -n 'tax-return-2023' -l 2023 tax --many

```
