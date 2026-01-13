import unittest
import os
from PIL import Image
from bw_converter.converter import process_image

class TestConverter(unittest.TestCase):
    def setUp(self):
        # Create a dummy image for testing
        self.input_image = "test_input.jpg"
        self.output_image = "test_output.jpg"
        img = Image.new('RGB', (100, 100), color = 'red')
        img.save(self.input_image)

    def tearDown(self):
        # Clean up files after testing
        if os.path.exists(self.input_image):
            os.remove(self.input_image)
        if os.path.exists(self.output_image):
            os.remove(self.output_image)

    def test_process_image(self):
        process_image(self.input_image, self.output_image)
        self.assertTrue(os.path.exists(self.output_image))
        
        # Check if the output image is indeed grayscale (L mode)
        with Image.open(self.output_image) as img:
            self.assertEqual(img.mode, 'L')

if __name__ == '__main__':
    unittest.main()
