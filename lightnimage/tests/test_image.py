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
        self.assertListEqual([2, 2], list(row_sum))

    def test_image_row_sum_scaling_works(self):
        """
        Added 04.11.2018
        @return:
        """
        lightning_image = LightningImage(self.sum_array)

        row_sum = lightning_image.row_sum(scale=1)
        # Here we need to test each element separately because the elements are float and we obviously cannot
        # hard-compare two floats & there is no "ListAlmostEqual" Assertion
        self.assertAlmostEqual(1.0, row_sum[0], 2)
        self.assertAlmostEqual(1.0, row_sum[1], 2)

    def test_image_column_sum_is_calculated_correctly(self):
        """
        Added 04.11.2018
        @return:
        """
        lightning_image = LightningImage(self.sum_array)

        column_sum = lightning_image.column_sum()
        self.assertListEqual([1, 3], list(column_sum))

    def test_image_column_sum_scaling_works(self):
        """
        Added 04.11.2018
        @return:
        """
        lightning_image = LightningImage(self.sum_array)

        column_sum = lightning_image.column_sum(scale=1)
        # Here we need to test each element separately because the elements are float and we obviously cannot
        # hard-compare two floats & there is no "ListAlmostEqual" Assertion
        self.assertAlmostEqual(0.333, column_sum[0], 2)
        self.assertAlmostEqual(1.0, column_sum[1], 2)

    def test_applying_function_on_image_that_returns_scalar(self):
        """
        Added 16.11.2018
        @return:
        """
        # Defining a function, that returns the global sum of all elements
        summation = 0

        def add(array):
            nonlocal summation
            it = np.nditer(array)
            while not it.finished:
                summation += it[0]
                it.iternext()
            return array

        # The array to test on
        array = np.asarray([
            [1, 2, 1],
            [1, 1, 2]
        ])
        image = LightningImage(array)

        # Applying the function
        image.transform(add)
        self.assertEqual(8, summation)

    def test_applying_function_transformation_on_each_element(self):
        """
        Added 16.11.2018
        @return:
        """
        def quadratic(value, index0, index1):
            return value ** 2

        # Creating the array to test on
        array = np.asarray([
            [1, 3],
            [2, 5]
        ])
        image = LightningImage(array)

        # Applying the function
        image.transform_element_wise(quadratic)
        # testing each element
        expected = ([
            [1, 9],
            [4, 25]
        ])
        self.assertTrue((image.array == expected).all())

    def test_applying_function_element_wise_with_outer_scope_variable(self):
        """
        Added 16.11.2018
        @return:
        """
        summation = 0

        def add(value, index0, index1):
            nonlocal summation
            summation += value
            return value

        # The array to test on
        array = np.asarray([
            [1, 2, 1],
            [1, 1, 2]
        ])
        image = LightningImage(array)

        # Applying the function
        image.transform_element_wise(add)
        self.assertEqual(8, summation)

    def test_applying_function_masked_element_wise(self):
        """
        Added 16.11.2018
        @return:
        """
        def quadratic(value, index0, index1):
            return value ** 2

        # Defining the array to test on, the mask to be used and the expected resulting array
        array = np.asarray([
            [1, 3, 5],
            [6, 2, 1],
            [3, 2, 4]
        ])
        mask = np.asarray([
            [1, 1, 0],
            [1, 0, 1],
            [1, 0, 0]
        ])
        expected = np.asarray([
            [1, 9, 5],
            [36, 2, 1],
            [9, 2, 4]
        ])

        # Applying the function on the array
        image = LightningImage(array)
        image.transform_masked(quadratic, mask)

        self.assertTrue((expected == image.array).all())

    def test_applying_function_masked_element_wise_with_additional_replace(self):
        """
        Added 16.11.2018
        @return:
        """
        def quadratic(value, index0, index1):
            return value ** 2

        # Defining the array to test on, the mask to be used and the expected resulting array
        array = np.asarray([
            [1, 3, 5],
            [6, 2, 1],
            [3, 2, 4]
        ])
        mask = np.asarray([
            [1, 1, 0],
            [1, 0, 1],
            [1, 0, 0]
        ])
        expected = np.asarray([
            [1, 9, 0],
            [36, 0, 1],
            [9, 0, 0]
        ])

        # Applying the function on the array
        image = LightningImage(array)
        image.transform_masked(quadratic, mask, 0)

        self.assertTrue((expected == image.array).all())


