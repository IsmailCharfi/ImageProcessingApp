from math import floor

import numpy as np
from matplotlib import image as mpimg, pyplot as plt
from numpy import random, int32, copy


class Pgm:
    def __init__(self, magic_number, comment, columns, lines, max_value, data):
        self.magic_number = magic_number
        self.comment = comment
        self.columns = columns
        self.lines = lines
        self.max_value = max_value
        self.data = data

    def create_pgm_file(self, filename):
        img = int32(self.data).tolist()
        image = open(filename + ".pgm", 'w')
        file = open(filename + ".txt", "w+")
        content = str(img)
        file.write(content)
        file.close()
        width = 0
        height = 0
        for row in img:
            height = height + 1
            width = len(row)
        image.write(self.magic_number + '\n')
        image.write(str(width) + ' ' + str(height) + '\n')
        image.write(str(self.max_value) + '\n')
        for i in range(height):
            count = 1
            for j in range(width):
                image.write(str(img[i][j]) + ' ')
                if count >= 17:
                    # No line should contain gt 70 chars (17*4=68)
                    # Max three chars for pixel plus one space
                    count = 1
                    image.write('\n')
                else:
                    count = count + 1
            image.write('\n')
        image.close()

    def average_gris(self):
        somme = 0
        for i in range(0, self.data.shape[0]):
            for j in range(0, self.data.shape[1]):
                somme += self.data[i][j]

        return somme / (self.data.shape[0] * self.data.shape[1])

    # l’écart type d’une image en niveaux de gris
    def standard_deviation_gris(self):
        somme = 0
        moy = self.average_gris()
        for i in range(0, self.data.shape[0]):
            for j in range(0, self.data.shape[1]):
                somme += (self.data[i][j] - moy) ** 2
        return np.sqrt(somme / (self.data.shape[0] * self.data.shape[1]))

    # l’histogramme de niveaux de gris
    def histogram(self):
        arr = np.zeros(256)
        for el in self.data:
            for num in el:
                arr[num] += 1
        return arr

    # cumulated histogram
    def histogram_cumulated(self):
        arr = self.histogram()
        arr_cumulated = np.zeros(256)
        amount = 0
        for i, el in enumerate(arr):
            amount += el
            arr_cumulated[i] = amount
        return arr_cumulated

    # cumulated probability
    def pc(self):
        arr = np.zeros(256)
        hc = self.histogram_cumulated()
        resolution = self.columns * self.lines
        for index, el in enumerate(hc):
            arr[index] = el / resolution
        return arr

    def get_n1(self):
        arr_pc = self.pc()
        arr_n1 = np.zeros(256)
        for i, el in enumerate(arr_pc):
            arr_n1[i] = floor(255 * el)
        return arr_n1

    def equalizer(self):
        histogram_arr = self.histogram()
        n1 = self.get_n1()
        arr_eq = np.zeros(256)
        k = 0
        for i, el in enumerate(histogram_arr):
            while k < 256 and n1[k] == i:
                arr_eq[i] += histogram_arr[k]
                k += 1
        return arr_eq

    def equalize_image(self):
        data = np.zeros((self.lines, self.columns))
        n1 = self.get_n1()
        for i in range(self.lines):
            for j in range(self.columns):
                index = self.data[i][j]
                data[i][j] = n1[index]

        return Pgm(self.magic_number, self.comment, self.columns, self.lines, self.max_value, data)

    # creating function that add noise to the given image
    def noisify_image(self):
        data = copy(self.data)
        for i in range(self.lines):
            for j in range(self.columns):
                value = random.randint(0, 20)
                if value == 0:
                    data[i][j] = 0
                if value == 20:
                    data[i][j] = 255

        return Pgm(self.magic_number, self.comment, self.columns, self.lines, self.max_value, data)
