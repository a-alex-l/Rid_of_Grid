import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def dist(x, y):
    return math.sqrt(x * x + y * y)


def get_border_grid_and_ink(dists_from_white):
    dists = set()
    for distance in dists_from_white:
        dists.add(int(distance))
    dists_from = []
    for i in dists:
        dists_from.append((i, np.searchsorted(dists_from_white, i, side='right')))
    return (dists_from_white[len(dists_from_white) - 1] +
            dists_from_white[len(dists_from_white) // 2]) / 2


def plot_hist(dists_from_white, in_file_name):
    plt.suptitle(in_file_name)
    plt.hist(dists_from_white, 100)
    plt.show()


def plot_sorted(dists_from_white, in_file_name):
    plt.plot(dists_from_white)
    plt.suptitle(in_file_name)
    border = get_border_grid_and_ink(dists_from_white)
    plt.axhline(y=border, color='r', linestyle='-')
    plt.show()


def get_dists_from_white(image):
    dists_from_white = []
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            dists_from_white.append(dist(255 - image.getpixel((i, j))[2],
                                         image.getpixel((i, j))[1]))
    dists_from_white = np.array(dists_from_white)
    dists_from_white.sort()
    return dists_from_white


def get_ans_image(image, border):
    ans_image = image
    for i in range(ans_image.size[0]):
        for j in range(ans_image.size[1]):
            if dist(255 - ans_image.getpixel((i, j))[2],
                    ans_image.getpixel((i, j))[1]) < border:
                ans_image.putpixel((i, j), (0, 0, 255))
    return ans_image


def save_ans(ans_image, in_file_name):
    dot_index = in_file_name.find('.')
    ans_file_name = in_file_name[:dot_index] + "_ans.png"
    ans_image = ans_image.convert('RGB')
    try:
        ans_image.save(ans_file_name, "PNG")
    except OSError:
        raise Warning("Warning: Skipped file " + in_file)
        pass


def rid_of_shadows(in_file_name):
    os.system('python shadow_eraser.py ' + in_file_name)
    dot_index = in_file.find('.')
    shadow_free_file_name = in_file[:dot_index] + "_ans.png"
    try:
        shadow_free_image = Image.open(shadow_free_file_name)
        return shadow_free_image
    except OSError:
        raise Warning("Warning: Skipped file " + in_file)
        pass


def rid_of_grid(in_file_name):
    in_image = rid_of_shadows(in_file)
    image = in_image.convert('HSV')
    dists_from_white = get_dists_from_white(image)
    border = get_border_grid_and_ink(dists_from_white)
    plot_hist(dists_from_white, in_file_name)
    ans_image = get_ans_image(image, border)
    save_ans(ans_image, in_file_name)


if __name__ == '__main__':
    for in_file in sys.argv[1:]:
        try:
            rid_of_grid(in_file)
        except OSError:
            raise Warning("Warning: Skipped file " + in_file)
            pass
