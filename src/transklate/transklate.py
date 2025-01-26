import pytesseract
import re
import fitz #To Convert PDF in PNG
import click #To get the file name from the command line
import os, shutil #To remove the directory
from pathlib import Path
from PIL import Image
from alive_progress import alive_bar #To show progress bar
#from libretranslatepy import LibreTranslateAPI
from deep_translator import GoogleTranslator

def convert_to_png(file):
    """
    Convert each PDF files in PNG 
    """
    # for file in sorted(Path('.').glob('*.pdf')): # old command for converting all pdf files in the directory
    
    print(f"Converting {file} to PNG...")
    doc = fitz.open(file)
    zoom = 4
    mat = fitz.Matrix(zoom, zoom)
    count = 0
    Path(f"./{file}_img").mkdir(parents=True, exist_ok=True)
    # Count variable is to get the number of pages in the pdf
    for p in doc:
        count += 1
    for i in range(count):
        val = f"./{file}_img/{i+10001}.png"
        page = doc.load_page(i)
        pix = page.get_pixmap(matrix=mat)
        pix.save(val)
    doc.close()

def convert_png_to_txt(file):
    """
    Convert each Png into tex and translate it into french
    """
    transcribed_article = ""
    images = sorted(Path(f'./{file}_img/').glob('*.png'))
    nb_images = len(images)
    with alive_bar(nb_images, title='Converting PNGs to TXT...') as bar:
        for img in sorted(Path(f'./{file}_img/').glob('*.png')):
            #print(f"Converting {img} to TXT...")
            transcribed_page= "*** PAGE " + str(img)[:-4] + " ***\n\n" + pytesseract.image_to_string(Image.open(img), lang='heb')
            translated_txt = translate_txt(transcribed_page)
            transcribed_page= re.sub("\n[^\n]", " ", transcribed_page)
            transcribed_article=transcribed_article + transcribed_page + "\n\n"
            bar()

    # Save the transcribed article in a txt file        
    file_name = file.split(".")[0]+"_transcribed.txt"
    with open(file_name, "w") as text_file:
        text_file.write(transcribed_article)

    # Remove the tmp img directory
    # Get directory name
    dir = file + "_img"
    # Try to remove the tree; if it fails, throw an error using try...except.
    try:
        shutil.rmtree(dir)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

def translate_txt(text_to_trans):
    translator = GoogleTranslator(source='hebrew', target='french')
    translated_text = translator.translate(text_to_trans)
    return translated_txt


def translate_txt_old(file):
    file_name = file.split(".")[0] + "_transcribed.txt"
    with open(file_name, "r", encoding="utf-8") as text_file:
        file_txt = text_file.read()

    translator = GoogleTranslator(source='hebrew', target='french')
    translated_article = translator.translate(file_txt)

    translated_file_name = file.split(".")[0] + "_translated.txt"
    with open(translated_file_name, "w", encoding="utf-8") as text_file:
        text_file.write(translated_article)

    print(f"Translation completed. Translated file saved as {translated_file_name}")



# def translate_txt(file):
#     file_name = file.split(".")[0]+"_transcribed.txt"
#     with open(file_name, "r") as text_file:
#         file_txt = text_file.read()
#     translator = Translator()
#     translated_article = ""
#     translated_article = str(translator.translate(file_txt, src='he', dest='fr'))
#     #translated_article = translated_article + translated_page + "\n\n"
#     with open("translated_article.txt", "w") as text_file:
#         text_file.write(translated_article)

@click.command()
@click.argument('file')
def transcribe(file):
   # convert_to_png(file)
    #convert_png_to_txt(file)
    translate_txt(file)

if __name__ == "__main__":
    transcribe()



    