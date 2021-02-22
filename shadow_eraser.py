import sys
import math
import numpy as np
import matplotlib.pyplot as plt
import random
import cv2


def sign(x_for_sign):
    return math.copysign(1, x_for_sign)


def get_approximate_color(i, j, gray_image, mask):
    max_side = max(0, min(i, j, mask.shape[0] - i - 1, mask.shape[1] - j - 1))
    side = 20
    for step in range(int(math.log2(max_side + 2))):
        i_new = i + random.randint(-side, side)
        j_new = j + random.randint(-side, side)
        if 0 <= i_new < mask.shape[0] and 0 <= j_new < mask.shape[1] and mask[i_new, j_new] == 0:
            return gray_image[i_new, j_new]
        if side * 2 < max_side:
            side = int(side * 1.5)
        else:
            side = max_side
    return 77


def get_f_color(shadow_color, current_color, global_average):
    x = float(shadow_color) - global_average
    y = float(current_color) - global_average
    return (x + y) / (abs((x - y) / 40) ** 2 + 2)


def get_shadow_distribution(gray_image, mask):
    ans_image = gray_image.copy()
    for i in range(ans_image.shape[0]):
        for j in range(ans_image.shape[1]):
            if mask[i, j] != 0:
                ans_image[i, j] = get_approximate_color(i, j, ans_image, mask)
    ans_image = cv2.blur(ans_image, (501, 501))
    global_average = int(np.average(ans_image))
    for i in range(ans_image.shape[0]):
        for j in range(ans_image.shape[1]):
            ans_image[i, j] = get_f_color(ans_image[i, j], gray_image[i, j], global_average)
    return ans_image


def get_mask_image(mask) -> np.ndarray:
    mask = cv2.adaptiveThreshold(mask,
                                 maxValue=255,
                                 adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 thresholdType=cv2.THRESH_BINARY_INV,
                                 blockSize=101,  # Parameter!
                                 C=0)  # Parameter!
    return mask


def save_ans(ans_image, in_file_name):
    dot_index = in_file_name.find('.')
    ans_file_name = in_file_name[:dot_index] + "_ans.png"
    try:
        cv2.imwrite(ans_file_name, ans_image)
    except OSError:
        raise Warning("Warning: Skipped file " + in_file)
        pass


def secure_minus(image, minus_image):
    ans_image = image
    for i in range(ans_image.shape[0]):
        for j in range(ans_image.shape[1]):
            ans_image[i, j, 0] = max(0, min(255, int(image[i, j, 0]) -
                                            (int(minus_image[i, j, 0]) - 255
                                             if minus_image[i, j, 0] > 128
                                             else int(minus_image[i, j, 0]))))
            ans_image[i, j, 1] = max(0, min(255, int(image[i, j, 1]) -
                                            (int(minus_image[i, j, 1]) - 255
                                             if minus_image[i, j, 1] > 128
                                             else int(minus_image[i, j, 1]))))
            ans_image[i, j, 2] = max(0, min(255, int(image[i, j, 2]) -
                                            (int(minus_image[i, j, 2]) - 255
                                             if minus_image[i, j, 2] > 128
                                             else int(minus_image[i, j, 2]))))
    return ans_image


def rid_of_shadow(image, in_file_name):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mask = get_mask_image(gray_image)
    gray_image = get_shadow_distribution(gray_image, mask)
    ans_image = secure_minus(image, cv2.cvtColor(gray_image, cv2.COLOR_GRAY2RGB))
    save_ans(ans_image, in_file_name)


if __name__ == '__main__':
    for in_file in sys.argv[1:]:
        try:
            rid_of_shadow(cv2.imread(in_file), in_file)
        except OSError:
            raise Warning("Warning: Skipped file " + in_file)
            pass
