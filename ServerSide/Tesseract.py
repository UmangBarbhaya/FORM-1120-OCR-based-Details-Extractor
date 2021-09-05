from pytesseract import image_to_string


class Tesseract:
    def __init__(self, cropped):
        self.cropped = cropped

    def tesseract(self):
        cropped = self.cropped
        result = image_to_string(cropped, lang="eng")

        return result
