from unittest import TestCase
import numpy as np

from lightnimage.calculate import average_2d, threshold_sequencing


class TestAverageCalculations(TestCase):

    def test_2d_average_basically_working(self):
        array = np.asarray([
            [1, 2, 4],
            [4, 5, 2]
        ])

        av = average_2d(array)
        self.assertEqual(3, av)

    def test_2d_average_sub_area_works(self):
        array = np.asarray([
            [1, 2, 4, 5],
            [4, 5, 2, 9],
            [8, 7, 7, 1]
        ])
        x_sequence = (0, 2)
        y_sequence = (0, 1)
        area = (x_sequence, y_sequence)
        av = average_2d(array, area)
        self.assertEqual(3, av)


class TestSequencingCalculations(TestCase):

    def test_1d_threshold_sequencing(self):
        array = np.asarray([0, 1, 2, 4, 5, 4, 5, 9, 4, 3, 0])
        sequences = threshold_sequencing(array, 4)
        self.assertEqual(1, len(sequences))
        sequence = sequences[0]
        self.assertEqual((3, 9), sequence)