import unittest
import os
from PIL import Image

inaccuracy = 0.9  # jpg loss = 0.02 = 2% = 5/256


def compare_images(infile, outfile):
    while not os.path.exists(infile):
        pass
    difference = 0
    image_ans = Image.open(infile)
    image_out = Image.open(outfile)
    for i in range(image_ans.size[0]):
        for j in range(image_ans.size[1]):
            difference += abs(image_ans.getpixel((i, j))[0] - image_out.getpixel((i, j))[0])
            difference += abs(image_ans.getpixel((i, j))[1] - image_out.getpixel((i, j))[1])
            difference += abs(image_ans.getpixel((i, j))[2] - image_out.getpixel((i, j))[2])
    image_ans.close()
    image_out.close()
    return difference / 3 / 255 / image_ans.size[0] / image_ans.size[1]


class MyTestCase(unittest.TestCase):
    def test_all(self):
        argv = ""
        for i in range(1, 29):
            argv += " assets/cleaner/test_input_" + str(i) + ".png"
        os.system('python cleaner.py' + argv)
        for i in range(1, 29):
            score = compare_images("assets/cleaner/test_input_" + str(i) + "_ans.png",
                                   "assets/cleaner/test_output_" + str(i) + ".png")
            print(i, "=>", score, end='    ')
            if i % 5 == 0:
                print(flush=True)
            self.assertTrue(score <= inaccuracy)


if __name__ == '__main__':
    unittest.main()
