from lightnimage.image import LightningImage


class AbstractVectorisationEngine:
    """

    CHANGELOG

    Added 05.11.2018

    """

    def __init__(self, lightning_image):
        """

        CHANGELOG

        Added 05.11.2018

        @param LightningImage lightning_image:
        """
        self.lightning_image = lightning_image
        self.array = self.lightning_image.array

    def __call__(self, *args, **kwargs):
        """

        CHANGELOG

        Added 05.11.2018

        @param args:
        @param kwargs:
        @return:
        """
        raise NotImplementedError()
