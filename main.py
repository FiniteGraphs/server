from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def import_Image():
    nameIm = input()
    img = Image.open(nameIm)
    return img


def to_black(img):
    return img.convert('L')


def to_array(img):
    img = np.array(img)
    return img


def print_array(arrayIm):
    print(arrayIm)


def main():
    img = import_Image()
    to_black(img)
    arrayIm = to_array(img)
    print_array(arrayIm)


if __name__ == '__main__':
    main()
