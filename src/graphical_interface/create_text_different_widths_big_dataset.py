# https://note.nkmk.me/en/python-pillow-concat-images/

from PIL import Image
import math
import random
import os
from datetime import datetime


# This class concatenates images with letters creating an image representing a given text
class TextImageRenderAllDifferentWidths:
    def __init__(self, directory_path: str, width: int, height: int, font_size: int, text_to_render: str):
        self.directory_path = directory_path
        self.width = width
        self.height = height
        self.font_size = font_size
        self.font_width = math.floor(font_size / 2)
        self.line_capacity = math.floor(width / self.font_width)
        self.text_to_render = text_to_render
        self.line_height_cefficeint = math.floor(3 * font_size / 2)

    # This is a simple method for updating the processed text
    def update_text_to_render(self, new_text_to_render):
        self.text_to_render = new_text_to_render

    # Method which parses the given string and creates a image representing the text
    def create_image(self):
        result_image = Image.new('RGB', (self.width, self.height), (255, 255, 255))  # this example uses color images - one may use mode='L' for monochrome images
        counter = 0
        random.seed(datetime.now())
        for letter in self.text_to_render:
            letter_to_int = ord(letter)
            if letter_to_int != 32:
                if letter_to_int >= 97:
                    letter_path = self.directory_path + letter.upper() + '2/'
                else:
                    letter_path = self.directory_path + letter + '/'
                img = Image.open(letter_path + str(random.randint(0, len([name for name in os.listdir(letter_path)]) - 1)) + '.png')
            else:
                img = Image.new('RGB', (self.font_width, self.line_capacity), (255, 255, 255))
            self.concatenate_vertical(result_image, img, letter_to_int, counter)
            counter = counter + 1
        # result_image.show()
        return result_image

    # This method is used for determining the dimensions of a letter
    def get_size_coefficients(self, letter):
        # Top letters: [A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z, b, d, f, h, k, l, t]
        if any([letter < 97, letter == 98, letter == 100, letter == 102, letter == 104, letter == 107, letter == 108, letter == 116, letter == 32]):
            return 1

        # Bottom letters: [g, j, p, q, y]
        if any([letter == 103, letter == 106, letter == 112, letter == 113, letter == 121]):
            return 2

        return 3  # I assume all other signs are of type straightforward letters
        # Straightforward letters : [ a, c, e, i, m, n, o, p, r, s, u, v, x, z]

    # This method concatenates a new letter to a image representing some part of the given text
    def concatenate_vertical(self, result_image, letter_image, letter_to_int, counter):
        letter_type = self.get_size_coefficients(letter_to_int)
        # letter_image = letter_image.resize((self.font_size, self.font_size))
        line_height = math.floor(counter / self.line_capacity) * self.line_height_cefficeint
        line_width = (counter % self.line_capacity) * self.font_width
        if letter_type == 3:
            letter_image = letter_image.resize((self.font_width, self.font_width))
            result_image.paste(letter_image, (line_width, self.font_width + line_height))
        elif letter_type == 1:
            letter_image = letter_image.resize((self.font_width, self.font_size))
            result_image.paste(letter_image, (line_width, line_height))
        elif letter_type == 2:
            letter_image = letter_image.resize((self.font_width, self.font_size))
            result_image.paste(letter_image, (line_width, self.font_width + line_height))


if '__name__' == '__main__':
    directory_path = './letters_dataset/'
    width = 300
    height = 300
    font_size = 60
    text_to_render = 'Hey guys I am Martin and I am a student'
    text_renderer = TextImageRenderAllDifferentWidths(directory_path, width, height, font_size, text_to_render)
    text_renderer.create_image()
