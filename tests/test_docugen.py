import unittest
from docugen.docugen import chunk_content, get_wikipedia_page
from docugen.text_processor import paraphrase

class TestDocuGen(unittest.TestCase):
    def test_chunk_content(self):
        content = "This is the first sentence. This is the second sentence. This is the third sentence."
        chunks = chunk_content(content, 2)
        self.assertEqual(len(chunks), 2)
        self.assertEqual(chunks[0], "This is the first sentence. This is the second sentence.")
        self.assertEqual(chunks[1], "This is the third sentence.")

    def test_get_wikipedia_page(self):
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