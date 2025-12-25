"""File containing the unit tests.
"""
import unittest
from pathlib import Path
from transklate.transklate import translate_txt, convert_to_png
from pymupdf import FileNotFoundError

PDF_EXAMPLE_FILE = Path(__file__).resolve().parent / "tests_data" / "config.yaml"

class TestTransklate(unittest.TestCase):

    def test_translate_txt(self):
        """Tests that the transkate text function works as expected.
        """
        example_text = "Hello, how are you?"
        expected_output = "Bonjour comment allez-vous?"
        self.assertEqual(
            translate_txt(example_text, "fr", source_lang="en"), expected_output
        )

    def test_translate_txt_unknown_language(self):
        """Tests that the transkate text fails as expected when the language
        is unknown.
        """
        example_text = "Hello, how are you?"
        with self.assertRaises(ValueError):
            translate_txt(example_text, output_lang="unknown")


class TestConvertToPNG(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""
        self.test_pdf = Path(__file__).resolve().parent / "tests_data" / "test.pdf"
        self.output_dir = self.test_pdf.parent / (self.test_pdf.stem + "_img")
        self.output_file = self.output_dir / "10001.png"

    def tearDown(self):
        """Clean up after the test."""
        if self.output_dir.exists():
            for file in self.output_dir.glob("*"):
                file.unlink()
            self.output_dir.rmdir()

    def test_convert_to_png(self):
        """Tests that the convert to PNG function works as expected : creation of folder and creation of image.
        """
        convert_to_png(str(self.test_pdf))
        self.assertTrue(self.output_dir.exists(), "Output directory was not created.")
        self.assertTrue(self.output_file.exists(), f"Expected PNG file {self.output_file} was not created.")
        

    def test_convert_to_png_invalid_file(self):
        """Tests that the convert to PNG function fails as expected when the
        file is invalid.
        """
        with self.assertRaises(FileNotFoundError):
            convert_to_png("non_existent.pdf")



if __name__ == '__main__':
    unittest.main()