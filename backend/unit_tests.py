import unittest
import numpy as np
from PIL import Image
from data_processing import transform_coordinates, generate_image_from_raster

class TestFunctions(unittest.TestCase):

    def test_transform_coordinates(self):
        class MockDataset:
            bounds = (500000, 0, 600000, 100000)

        dataset = MockDataset()

        expected_south_west = (0.0, 14.999999999999982)
        expected_north_east = (0.904618578893133, 15.898748937075336)


        south_west, north_east = transform_coordinates(dataset)

        self.assertAlmostEqual(south_west[0], expected_south_west[0], places=5)
        self.assertAlmostEqual(south_west[1], expected_south_west[1], places=5)
        self.assertAlmostEqual(north_east[0], expected_north_east[0], places=5)
        self.assertAlmostEqual(north_east[1], expected_north_east[1], places=5)

    def test_generate_image_from_raster(self):
        raster_data = np.array([[0, 1], [2, 3]], dtype=np.float32)

        buffer = generate_image_from_raster(raster_data)

        buffer.seek(0)
        image = Image.open(buffer)

        self.assertEqual(image.mode, "L")  # Grayscale mode
        self.assertEqual(image.size, (2, 2))  # Dimensions should match raster data

        expected_image = np.array([[0, 85], [170, 255]], dtype=np.uint8)
        image_data = np.array(image)
        np.testing.assert_array_equal(image_data, expected_image)

if __name__ == "__main__":
    unittest.main()
