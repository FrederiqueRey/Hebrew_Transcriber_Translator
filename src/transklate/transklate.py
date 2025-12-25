import pytesseract
import re
import fitz  # To Convert PDF in PNG
import click  # To get the file name from the command line
import os, shutil  # To remove the directory
from pathlib import Path
from PIL import Image
from alive_progress import alive_bar  # To show progress bar
from deep_translator import GoogleTranslator
from deep_translator.exceptions import LanguageNotSupportedException

# from deep_translator import ChatGptTranslator


def convert_to_png(file: str) -> None:
    """
    Convert each PDF files in PNG

    Args:
        file (str): The name of the file to convert.
    
    Returns:
        None: None, only outputs the converted PNG files in a directory.
    """
    # for file in sorted(Path('.').glob('*.pdf')): # old command for converting all pdf files in the directory

    pdf_path = Path(file)
    file_name = pdf_path.stem
    img_dir = pdf_path.parent / f"{file_name}_img"
    print(f"Converting {file} to PNG...")
    doc = fitz.open(file)
    zoom = 4
    mat = fitz.Matrix(zoom, zoom)
    count = 0
    img_dir.mkdir(parents=True, exist_ok=True)
    # Count variable is to get the number of pages in the pdf
    for p in doc:
        count += 1
    for i in range(count):
        val = img_dir / f"{i+10001}.png"
        page = doc.load_page(i)
        pix = page.get_pixmap(matrix=mat)
        pix.save(str(val))
    doc.close()


def convert_png_to_txt(file: str, lang: str) -> None:
    """
    Convert each Png into tex and translate them into french.

    Args:
        file (str): The name of the file to convert.
        lang (str): The language to translate to.

    Returns:
        None: None, only outputs the transcribed and translated text in txt
            files.
    """
    pdf_path = Path(file)
    file_name = pdf_path.stem
    img_dir = pdf_path.parent / f"{file_name}_img"
    transcribed_article = ""
    translated_article = ""
    images = sorted(img_dir.glob("*.png"))
    nb_images = len(images)
    with alive_bar(nb_images, title="Converting PNGs to TXT...") as bar:
        for img in sorted(img_dir.glob("*.png")):
            transcribed_page = (
                "*** PAGE "
                + str(img)[:-4]
                + " ***\n\n"
                + pytesseract.image_to_string(Image.open(img), lang="heb")
            )
            # print(transcribed_page)
            translated_page = re.sub(
                "\n(?!\n)", " ", translate_txt(transcribed_page, lang)
            )
            transcribed_page = re.sub("\n(?!\n)", " ", transcribed_page)
            transcribed_article = transcribed_article + transcribed_page + "\n\n"
            translated_article = translated_article + translated_page + "\n\n"
            bar()

    # Save the transcribed and translated article in txt files
    transcribed_file_name = file.split(".")[0] + "_transcribed.txt"
    with open(transcribed_file_name, "w") as text_file:
        text_file.write(transcribed_article)
    translated_file_name = file.split(".")[0] + "_translated.txt"
    with open(translated_file_name, "w") as text_file:
        text_file.write(translated_article)


    # Remove the tmp img directory
    dir = img_dir  # Get directory name
    try:  # Try to remove the tree; if it fails, throw an error using try...except.
        shutil.rmtree(dir)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))


def translate_txt(text_to_trans: str, output_lang: str, source_lang: str = "hebrew") -> str:
    """Translate the text to the desired language.

    Args:
        text_to_trans (str): The text to translate.
        lang (str): The language to translate to.

    Returns:
        str: The translated text.
    """
    try:
        translator = GoogleTranslator(source=source_lang, target=output_lang)
        translated_text = translator.translate(text_to_trans)
        return translated_text
    except LanguageNotSupportedException as e:
        raise ValueError(f"Language {output_lang} is not supported by the translator. {e}")


@click.command()
@click.argument("file")
@click.option(
    "-o", "--output_lang",
    default="fr",
    help="Language to translate to, see Googletranslate for available languages",
)
def transcribe(file, output_lang):
    convert_to_png(file)
    convert_png_to_txt(file, output_lang)


if __name__ == "__main__":
    transcribe()
