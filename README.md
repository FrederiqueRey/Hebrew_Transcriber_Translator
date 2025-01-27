# Transklate - A small tools to convert PDF in Hebrew in to txt and to translate them

The purpose of this little code is to automate the following two processes:
1. to transcribe a PDF written in Hebrew into a TXT file using Tesseract.
  - PDF are converted into PNGs in a temporary folder
  - Each images are then converted into strings by Tesseract
3. translate the TXT file into French using Google Translate.

Currently, the translation is not very good (and not as good as you'd expect from Google Translate online).
It is a really work in progress code.

## Instalation
```bash
pip install transklate
```

## Basic CLI use
```bash
transklate <file_name.pdf>
```


