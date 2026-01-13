import unittest
from unittest.mock import patch, MagicMock
import os
from image_poetry.generator import generate_poem

class TestGenerator(unittest.TestCase):
    @patch('image_poetry.generator.genai')
    @patch('image_poetry.generator.Image')
    @patch('os.getenv')
    def test_generate_poem_success(self, mock_getenv, mock_image, mock_genai):
        # Setup mocks
        mock_getenv.return_value = "fake_key"
        mock_model = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        mock_response = MagicMock()
        mock_response.text = "Roses are red, violets are blue..."
        mock_model.generate_content.return_value = mock_response

        # Create a dummy file for the test (or just mock os.path.exists)
        with patch('os.path.exists', return_value=True):
            poem = generate_poem("dummy.jpg")
            
        self.assertEqual(poem, "Roses are red, violets are blue...")
        mock_model.generate_content.assert_called_once()

    @patch('os.getenv')
    def test_missing_api_key(self, mock_getenv):
        mock_getenv.return_value = None
        with self.assertRaises(ValueError):
            generate_poem("dummy.jpg")

if __name__ == '__main__':
    unittest.main()
