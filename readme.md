# Linux CLI Document Management System

```bash
# set env variable
export SCANNER_DEFAULT_DEVICE='escl:http://localhost:60000'

# add bin to path
export PATH="$PATH:/path/to/scan-cli/bin"

# install OCR engine
sudo apt install tesseract-ocr
```

```bash
# scan usage
python3 main.py scan
python3 main.py scan --resolution 300
python3 main.py scan -n 'paystub-feb-2023-1' --ocr
python3 main.py scan -n 'paystub-feb-2023-1' -l 2023 paystub 'XYZ Corp'
python3 main.py scan -n 'tax-return-2023' -l 2023 tax --many

```

```bash
# scan options
-n --name file name                  # file name root
-l --labels label1 label2 .. labeln  # meta data labels for the document(s)
-o --ocr                             # process with OCR engine (default = No)
-m --many                            # scan multiple pages (default = No)
-r --resolution 75|150|300           # DPI value (default = 150)
-c --color Gray|Color                # color mode (default = Gray)
```
