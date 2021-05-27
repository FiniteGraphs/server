from PIL import Image
import numpy as np

def import_Image():
    nameIm = "image.png"
    img = Image.open(nameIm)
    return img


def to_black(img):
    return img.convert('L')


def to_array(img):
    img = np.array(img)
    return img


def print_array(arrayIm):
    print('size:', arrayIm.shape)
    print(arrayIm)


def createArrayFromImage(img_path):
    img = Image.open(img_path)
    to_black(img)
    arrayIm = to_array(img)
    print(arrayIm)
    return arrayIm

if __name__ == '__main__':
    imgArray = createArrayFromImage()
