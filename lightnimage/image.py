import numpy as np


class LightningImage:
    """
    A numpy array wrapper object for manipulating grayscale images

    CHANGELOG

    Added 04.11.2018

    @author Jonas Teufel
    """

    def __init__(self, img):
        """
        The constructor.


        CHANGELOG

        Added 04.11.2018

        Changed 06.11.2018
        Added separate attributes for the height and width of the image

        @param np.ndarray img: The array should be two dimensions, which means only grayscale images
        """
        self.original = img
        self.array = img

        # 06.11.2018
        # Saving the height and the width of the image and thus the dimensions of the array as well
        self.width = self.array.shape[1]
        self.height = self.array.shape[0]

    def darken(self, threshold, replace=0):
        """

        CHANGELOG

        Added 04.11.2018

        @param int threshold:
        @param int replace:
        @return:
        """
        it = np.nditer(self.array, flags=['multi_index'], op_flags=['writeonly'])
        while not it.finished:
            if it[0] <= threshold:
                it[0] = replace
            it.iternext()

    def lighten(self, threshold, replace=255):
        """

        CHANGELOG

        Added 04.11.2018

        @param int threshold:
        @param int replace:
        @return:
        """
        it = np.nditer(self.array, flags=['multi_index'], op_flags=['writeonly'])
        while not it.finished:
            if it[0] >= threshold:
                it[0] = replace
            it.iternext()

    def invert(self):
        """

        CHANGELOG

        Added 04.11.2018

        @return:
        """
        it = np.nditer(self.array, flags=['multi_index'], op_flags=['writeonly'])
        while not it.finished:
            it[0] = 255 - it[0]
            it.iternext()

    def difference(self, other, threshold=10, replace=255, invert=False, ):
        """

        CHANGELOG

        Added 04.11.2018

        @param LightningImage other:   The other image, which is supposed to be subtracted from this one
        @param int threshold:
        @param int replace:
        @param bool invert:
        @return:
        """
        new = np.zeros(self.array.shape)
        it = np.nditer(new, flags=['multi_index'], op_flags=['writeonly'])
        while not it.finished:
            value_self = self.array[it.multi_index]
            value_other = other.array[it.multi_index]
            diff = abs(int(value_self) - int(value_other))

            if diff <= threshold:
                it[0] = replace
            else:
                it[0] = abs(int(value_self) - int(value_other))
                if invert:
                    it[0] = 255 - it[0]

            it.iternext()

        return LightningImage(new)

    def column_sum(self, scale=None):
        """

        CHANGELOG

        Added 06.11.2018

        @param scale:
        @return:
        """
        return self.directional_sum(0, scale)

    def row_sum(self, scale=None):
        """

        CHANGELOG

        Added 06.11.2018

        @param scale:
        @return:
        """
        return self.directional_sum(1, scale)

    def directional_sum(self, axis, scale):
        """
        Calculates an array, that contains the float sum's of each element either the rows or the columns. The array
        thus has the same size as either the column or the row of the image.
        These sum values could possibly take any value from 0 to 255 * array length (for an all white picture). The
        scale parameter optionally limits the maximum value possible by scaling all elements down proportionally.

        CHANGELOG

        Added 06.11.2018

        @param int axis:    Either 0 or 1. A 1 would be the sum of all rows and 0 the sum of all columns
        @param int scale:   An integer, which sets the maximum value for the sums. All values get scaled
                            relative to this value.
        @return: An array of either the height or width of the image
        """

        # Creating a new one dimensional array with just as many elements as there are pixel rows in the image, which
        # will contain the sum values of each row.
        # For a two dimensional array (as the image is one), the second item of the shape attribute will contain the
        # length of a column and thus the amount of rows
        sum_array = np.ndarray(self.array.shape[axis], np.float64)

        # Iterating through all the rows of the array ans summing up the individual elements
        for i in range(self.array.shape[axis]):
            temp_sum = 0
            for j in range(self.array.shape[1 - axis]):
                # Numpy arrays support multi indexing in a single bracket for higher dimensions and this is also the
                # more efficient way
                if axis:
                    temp_sum += self.array[i, j]
                else:
                    temp_sum += self.array[j, i]

            sum_array[i] = temp_sum

        # If there is a scale value given, all the values in the array will be scaled, so that the maximum value is
        # at most the scale value
        if scale is not None:
            maximum = max(sum_array)
            # The np.vectorize function is used to convert a normal python function object into a function, that can
            # be applied on a numpy array, element-wise
            scaling = np.vectorize(lambda x: (x / maximum) * scale, otypes=[np.float64])
            sum_array = scaling(sum_array)

        return sum_array
