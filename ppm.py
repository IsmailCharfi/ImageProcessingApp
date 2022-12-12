from math import floor

import numpy as np
from matplotlib import image as mpimg, pyplot as plt
from numpy import random, int32, copy


class Ppm:
    def __init__(self, magic_number, comment, columns, lines, max_value, data):
        self.magic_number = magic_number
        self.comment = comment
        self.columns = columns
        self.lines = lines
        self.max_value = max_value
        self.data = data

    def create_file(self, filename):
        image = open(filename + ".ppm", 'w')
        image.write(self.magic_number + '\n')
        image.write(str(self.columns) + ' ' + str(self.lines) + '\n')
        image.write(str(self.max_value))
        count = 1
        for i in range(len(self.data)):
            for j in range(0, 3):
                image.write(str(self.data[i][j]) + ' ')
            if count >= self.columns:
                image.write('\n')
                count = 1
            else:
                count += 1

        image.close()

    def threshold(self, r, g, b):
        new_data = copy(self.data)
        for i in range(0, len(new_data)):
            if int(self.data[i][0]) < int(r):
                new_data[i] = tuple((0, new_data[i][1], new_data[i][2]))
            else:
                new_data[i] = tuple((255, new_data[i][1], new_data[i][2]))
            if int(new_data[i][1]) < g:
                new_data[i] = tuple((new_data[i][0], 0, new_data[i][2]))
            else:
                new_data[i] = tuple((new_data[i][0], 255, new_data[i][2]))
            if int(new_data[i][2]) < b:
                new_data[i] = tuple((new_data[i][0], new_data[i][1], 0))
            else:
                new_data[i] = tuple((new_data[i][0], new_data[i][1], 255))

        return Ppm(self.magic_number, self.comment, self.columns, self.lines, self.max_value, new_data)

    def and_threshold(self, r, g, b):
        new_data = copy(self.data)
        for i in range(0, len(self.data)):
            if not (int(self.data[i][0]) > int(r) and int(self.data[i][1]) > int(g) and int(self.data[i][2]) > int(b)):
                new_data[i] = tuple((0, 0, 0))
            else:
                new_data[i] = tuple((255, 255, 255))
        return Ppm(self.magic_number, self.comment, self.columns, self.lines, self.max_value, new_data)

    def or_threshold(self, r, g, b):
        new_data = copy(self.data)
        for i in range(0, len(self.data)):
            if not (int(self.data[i][0]) > int(r) or int(self.data[i][1]) > g or int(self.data[i][2]) > b):
                new_data[i] = tuple((0, 0, 0))
            else:
                new_data[i] = tuple((255, 255, 255))

        return Ppm(self.magic_number, self.comment, self.columns, self.lines, self.max_value, new_data)

    @staticmethod
    def create_from_file(file_data):
        words = file_data[2].split()
        columns = int(words[0])
        lines = int(words[1])
        magic_number = file_data[0]
        comment = file_data[1]
        max_value = file_data[3]
        array_values = []

        for i in range(4, len(file_data)):
            values = file_data[i].split()
            array_values = array_values + values
        matrix = [tuple(array_values[i:i + 3]) for i in range(0, len(array_values), 3)]

        return Ppm(magic_number, comment, columns, lines, max_value, matrix)

    @staticmethod
    def display_image(filename):
        img_read = mpimg.imread(filename + ".ppm")
        plt.imshow(img_read)
        plt.show()
