# Terminal Document Management System

```bash
# set env variable
export SCANNER_DEFAULT_DEVICE='escl:http://localhost:60000'

# install OCR engine
sudo apt install tesseract-ocr
```

```bash
# Example usage
python3 main.py scan
python3 main.py scan -n 'paystub-feb-2023-1'
python3 main.py scan -n 'paystub-feb-2023-1' -l 2023 paystub 'XYZ Corp'
python3 main.py scan -n 'tax-return-2023' -l 2023 tax -m
```

```bash
# options
-n --name file name                  # file name root
-l --labels label1 label2 .. labeln  # labels for the document(s)
-o --ocr                             # process with OCR engine (default = No)
-m --many                            # scan multiple pages (default = No)
-r --resolution 75|150|300           # DPI value (default = 150)
-c --color Gray|Color                # color mode (default = Gray)
```
