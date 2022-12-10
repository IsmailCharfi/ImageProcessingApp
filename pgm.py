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

    def create_file(self, filename):
        img = int32(self.data).tolist()
        image = open(filename + ".pgm", 'w')
        image.write(self.magic_number + '\n')
        image.write(str(self.columns) + ' ' + str(self.lines) + '\n')
        image.write(str(self.max_value))
        for i in range(self.lines):
            for j in range(self.columns):
                image.write(str(img[i][j]) + ' ')
            if (i != self.lines - 1):
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

    def apply_filter(self, filter):
        n = filter.shape[0]
        new_im = np.zeros((self.lines, self.columns))
        for i in range(0, self.lines):
            for j in range(0, self.columns):
                if i < n // 2 or j < n // 2 or i > self.lines - n // 2 - 1 or j > self.columns - n // 2 - 1:
                    new_im[i, j] = self.data[i, j]
                else:
                    window = self.data[i - n // 2: i + n // 2 + 1, j - n // 2: j + n // 2 + 1]
                    output = np.sum(window * filter)
                    new_im[i, j] = output
        return Pgm(self.magic_number, self.comment, self.columns, self.lines, self.max_value, new_im.astype(np.uint8))

    def apply_average_filter(self, n):
        filter = np.zeros((n, n))
        for i in range(0, n):
            for j in range(0, n):
                filter[i][j] = 1.0 / n
        return self.apply_filter(filter)

    @staticmethod
    def create_from_file(file_data):
        words = file_data[2].split()
        columns = int(words[0])
        lines = int(words[1])
        magic_number = file_data[0]
        comment = file_data[1]
        max_value = file_data[3]
        data = [[0 for x in range(columns)] for y in range(lines)]
        for i in range(4, len(file_data)):
            ll = file_data[i].split()
            for j in range(0, len(ll)):
                data[i - 4][j] = int(ll[j])
        return Pgm(magic_number, comment, columns, lines, max_value, data)

    def display_image(self):
        plt.imshow(self.data, cmap='gray')
        plt.show()
