from lightnimage.image import LightningImage

from unittest import TestCase

import numpy as np


class TestLightningImage(TestCase):

    def setUp(self):
        """
        Added 04.11.2018

        Changed 06.11.2018
        Added another array, which is used to test the width and height parameters
        @return:
        """
        # Setting up an array, whose row and column sums are different for the methods testing the row and column sum
        # methods of the LightningImage objects.
        # row sum is [1, 3]
        # column sum is [2, 2]
        self.sum_array = np.asarray([
            [0, 1],
            [2, 1]
        ], np.uint8)

        # 06.11.2018
        # Setting up an array, which is not quadratic, to test if the width and height values are correct
        # The array has 4 columns and only 2 rows
        self.shape_array = np.asarray([
            [0, 1, 2, 3],
            [4, 5, 6, 7]
        ])

    def test_height_and_width_values_are_assigned_correctly(self):
        """
        Added 06.11.2018
        @return:
        """
        lightning_image = LightningImage(self.shape_array)

        self.assertEqual(2, lightning_image.height)
        self.assertEqual(4, lightning_image.width)

    def test_image_row_sum_is_calculated_correctly(self):
        """
        Added 04.11.2018
        @return:
        """
        lightning_image = LightningImage(self.sum_array)

        row_sum = lightning_image.row_sum()
        self.assertListEqual([1, 3], list(row_sum))

    def test_image_row_sum_scaling_works(self):
        """
        Added 04.11.2018
        @return:
        """
        lightning_image = LightningImage(self.sum_array)

        row_sum = lightning_image.row_sum(scale=1)
        # Here we need to test each element separately because the elements are float and we obviously cannot
        # hard-compare two floats & there is no "ListAlmostEqual" Assertion
        self.assertAlmostEqual(0.333, row_sum[0], 2)
        self.assertAlmostEqual(1.0, row_sum[1], 2)

    def test_image_column_sum_is_calculated_correctly(self):
        """
        Added 04.11.2018
        @return:
        """
        lightning_image = LightningImage(self.sum_array)

        column_sum = lightning_image.column_sum()
        self.assertListEqual([2, 2], list(column_sum))

    def test_image_column_sum_scaling_works(self):
        """
        Added 04.11.2018
        @return:
        """
        lightning_image = LightningImage(self.sum_array)

        column_sum = lightning_image.column_sum(scale=1)
        # Here we need to test each element separately because the elements are float and we obviously cannot
        # hard-compare two floats & there is no "ListAlmostEqual" Assertion
        self.assertAlmostEqual(1.0, column_sum[0], 2)
        self.assertAlmostEqual(1.0, column_sum[1], 2)

