import unittest
from unittest.mock import patch
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from docugen.docugen import clean_title, chunk_content, get_wikipedia_page
from docugen.text_processor import paraphrase

class TestDocuGen(unittest.TestCase):
    def test_clean_title(self):
        test_cases = [
            ("This is a (test) title [with] {brackets} and spaces  ", "This Is A Title And Spaces"),
            ("Python (programming language)", "Python"),
            ("The Quick [Brown] Fox {Jumps} Over (The Lazy) Dog", "The Quick Fox Over Dog"),
            ("  Spaces   at   ends  ", "Spaces At Ends"),
            ("ALL CAPS TITLE", "All Caps Title"),
            ("mixed CASE tiTLe", "Mixed Case Title"),
            ("Title with numbers 123", "Title With Numbers 123"),
            ("Very long title that should be truncated to fifty characters", "Very Long Title That Should Be Truncated To Fifty"),
        ]
        
        for input_title, expected_output in test_cases:
            with self.subTest(input_title=input_title):
                clean = clean_title(input_title)
                self.assertEqual(clean, expected_output)

    def test_chunk_content(self):
        content = "This is the first sentence. This is the second sentence. This is the third sentence."
        chunks = chunk_content(content, 2)
        self.assertEqual(len(chunks), 2)
        self.assertEqual(chunks[0], "This is the first sentence. This is the second sentence.")
        self.assertEqual(chunks[1], "This is the third sentence.")

    @patch('wikipedia.page')
    def test_get_wikipedia_page(self, mock_wikipedia_page):
        mock_page = unittest.mock.MagicMock()
        mock_page.title = "Python (programming language)"
        mock_wikipedia_page.return_value = mock_page
        
        page = get_wikipedia_page("Python (programming language)")
        self.assertIsNotNone(page)
        self.assertTrue("Python" in page.title)

    def test_paraphrase(self):
        original = "The quick brown fox jumps over the lazy dog."
        paraphrased = paraphrase(original)
        self.assertNotEqual(original, paraphrased)
        self.assertTrue(len(paraphrased) > 0)

if __name__ == '__main__':
    unittest.main()