from email.mime import image
from tkinter import image_names
from PIL import Image, ImageFilter
import numpy as np
from math import sqrt

#infile = 'imagem.jpg'

#imagem = Image.open(infile)

# print(imagem.getpixel((500,500)))


def triangulo(size):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    imagem = Image.new("RGB", (size, size), WHITE)

    for x in range(size):
        for y in range(size):
            if x < y:
                imagem.putpixel((x, y), BLACK)
    return imagem


def bandeira_franca(height):
    WHITE = (255, 255, 255)
    BLUE = (0, 85, 164)
    RED = (239, 65, 53)

    width = 3*height//2

    image = Image.new("RGB", (width, height), WHITE)

    offset = width//3
    for x in range(offset):
        for y in range(height):
            image.putpixel((x, y), BLUE)
            image.putpixel((x + 2*offset, y), RED)

    return image


def bandeira_japao(height):
    WHITE = (255, 255, 255)
    RED = (239, 65, 53)

    width = 3*height//2

    r = 3*height//10
    c = (width//2, height//2)

    imagem = Image.new("RGB", (width, height), WHITE)

    for x in range(c[0]-r, c[0]+r):
        for y in range(c[1]-r, c[1]+r):
            if (x-c[0])**2 + (y-c[1])**2 <= r**2:
                imagem.putpixel((x, y), RED)

    return imagem


def bandeira_brasil(height):
    GREEN = (0, 156, 59)
    YELLOW = (255, 223, 0)
    BLUE = (0, 39, 118)
    WHITE = (255, 255, 255)

    width = 10*height//7

    margem = 17*height//140
    r = height//4
    c = (width//2, height//2)

    imagem = Image.new("RGB", (width, height), GREEN)

    for x in range(margem, width-margem):
        for y in range(margem, width-margem):
            if x <= c[0] and y <= c[1] and (c[1]-y) <= 0.64*(x-margem):
                imagem.putpixel((x, y), YELLOW)
            if x <= c[0] and y > c[1] and (y-c[1]) <= 0.64*(x-margem):
                imagem.putpixel((x, y), YELLOW)
            if x > c[0] and y <= c[1] and (c[1]-y) <= -0.64*(x-c[0])+c[1]-margem:
                imagem.putpixel((x, y), YELLOW)
            if x > c[0] and y > c[1] and (y-c[1]) <= -0.64*(x-c[0])+c[1]-margem:
                imagem.putpixel((x, y), YELLOW)
    for x in range(c[0]-r, c[0]+r):
        for y in range(c[1]-r, c[1]+r):
            if x == width//2:
                imagem.putpixel((x, y), YELLOW)
            if (x-c[0])**2 + (y-c[1])**2 <= r**2:
                imagem.putpixel((x, y), BLUE)

    return imagem


def escala_cinza(colorida):
    a, l = colorida.size
    imagem = Image.new("RGB", (a, l))

    for x in range(a):
        for y in range(l):
            pxl = colorida.getpixel((x, y))
            lum = int(pxl[0]*0.3 + pxl[1]*0.59 + pxl[2]*0.11)
            imagem.putpixel((x, y), (lum, lum, lum))
    return imagem


def show_vertical(im1, im2):
    im = Image.fromarray(np.vstack((np.array(im1), np.array(im2))))
    im.show()


def show_horizontal(im1, im2):
    im = Image.fromarray(np.hstack((np.array(im1), np.array(im2))))
    im.show()


def borramento(imagem, raio):
    #original = Image.open(imagem)
    image = imagem.filter(ImageFilter.BoxBlur(raio))

    return image


def edges(imagem, direction='x', offset=0):
    original = imagem.convert("L")
    Xsobel = ImageFilter.Kernel(
        (3, 3),
        [-1, 0, 1,
         -2, 0, 2,
         -1, 0, 1],
        1,
        offset)
    Ysobel = ImageFilter.Kernel(
        (3, 3),
        [-1, -2, -1,
         0, 0, 0,
         1, 2, 1],
        1,
        offset)
    if direction == 'x':
        filtered = original.filter(Xsobel)
    elif direction == 'y':
        filtered = original.filter(Ysobel)
    else:
        vsobel = original.filter(Xsobel)
        hsobel = original.filter(Ysobel)
        w, h = original.size
        filtered = Image.new("L", (w, h))

        for i in range(w):
            for j in range(h):
                value = sqrt(vsobel.getpixel((i, j))**2 +
                             hsobel.getpixel((i, j))**2)
                value = int(min(value, 255))
                filtered.putpixel((i, j), value)
    filtered.show()


def greenmask(imagem):
    hsvimag = imagem.convert("HSV")
    hsvimag = np.array(hsvimag)
    canal = hsvimag[0, :, :]
    h = canal[1, :, :]
    s = canal[2, :, :]
    v = canal[3, :, :]


if __name__ == "__main__":
    image = Image.open("download.jpeg")
    edges(image, "j", 0)
    # show_horizontal(image,imagem)
