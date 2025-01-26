# Hebrew Transcriber & Translator

The purpose of this little code is to OCRise automate the following two processes:
1. to transcribe a PDF written in Hebrew into a TXT file using Tesseract.
  - PDF are converted into PNGs in a temporary folder
  - Each images are then converted into strings by Tesseract
3. translate the TXT file into French using Google Translate.

Currently, the translation is not very good (and not as good as you'd expect from Google Translate online).
It is a really work in progress code.

### To install requirements
`pip install -r requirements.txt`


