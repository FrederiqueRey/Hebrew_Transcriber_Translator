# Transklate - A small tools to convert PDF in Hebrew to txt and to translate it

The purpose of this little code is to automate the following two processes
1. to transcribe a PDF written in Hebrew into a TXT file using Tesseract.
  - The PDFs are converted to PNGs in a temporary folder.
  - Each image is then converted to a string by Tesseract.
2. translate the TXT file into the language of your choice using Google Translate.

At the moment the translation is not very good (and not as good as you'd expect from Google Translate online).

## Instalation
```bash
pip install transklate
```

## Basic CLI use
```bash
transklate <file_name.pdf> --lang en
```
For the output language, use the Google translate code list.
