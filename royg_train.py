import math, random, time, pygame, sys
from pygame.locals import *
from PIL import Image
import numpy as np
import json

print("i tried")

def random_select(distribution, color, iteration):
    random_r = int(np.random.normal(color[0], distribution[0] * 60 / (20*(iteration+1))))
    random_g = int(np.random.normal(color[1], distribution[1] * 60 / (20*(iteration+1))))
    random_b = int(np.random.normal(color[2], distribution[2] * 60 / (20*(iteration+1))))
    if (random_r  > 255):
        random_r = 255
    if (random_g  > 255):
        random_g = 255
    if (random_b  > 255):
        random_b  = 255
    if (random_r  < 0):
        random_r = 0
    if (random_g  < 0):
        random_g = 0
    if (random_b  < 0):
        random_b  = 0
    return (random_r, random_g, random_b)

def generate_color(input_key, input_color, iteration):
	return (random_select(color_model[input_key], input_color, iteration))

def generate_key(input_color):
    key = int(input_color[0]/32+1)*100 + int(input_color[1]/32+1)*10 + int(input_color[2]/32+1)
    return (key)

window_size = 1024
num_iterations = 2
valid_input = False
grid_colors = []

if __name__ == "__main__":
    if (len(sys.argv) == 2):
        training_image = sys.argv[1]

        im = Image.open(training_image)
        pix = im.load()

        rgb_values = []
        color_model = {}

        for x in range(im.size[0]):
            these_rgbs = []
            for y in range(im.size[1]):
                these_rgbs.append(pix[x,y])
            rgb_values.append(these_rgbs)

        for x in range(im.size[0] / 2):
            for y in range(im.size[1] / 2):
                rgb_mean = []
                rgb_mean.append(sum([rgb_values[x*2][y*2][0], rgb_values[x*2][y*2+1][0], rgb_values[x*2+1][y*2][0], rgb_values[x*2+1][y*2+1][0]]) / 4)
                rgb_mean.append(sum([rgb_values[x*2][y*2][1], rgb_values[x*2][y*2+1][1], rgb_values[x*2+1][y*2][1], rgb_values[x*2+1][y*2+1][1]]) / 4)
                rgb_mean.append(sum([rgb_values[x*2][y*2][2], rgb_values[x*2][y*2+1][2], rgb_values[x*2+1][y*2][2], rgb_values[x*2+1][y*2+1][2]]) / 4)

                rgb_std = []
                rgb_std.append(int(np.std([rgb_values[x*2][y*2][0], rgb_values[x*2][y*2+1][0], rgb_values[x*2+1][y*2][0], rgb_values[x*2+1][y*2+1][0]])))
                rgb_std.append(int(np.std([rgb_values[x*2][y*2][1], rgb_values[x*2][y*2+1][1], rgb_values[x*2+1][y*2][1], rgb_values[x*2+1][y*2+1][1]])))
                rgb_std.append(int(np.std([rgb_values[x*2][y*2][2], rgb_values[x*2][y*2+1][2], rgb_values[x*2+1][y*2][2], rgb_values[x*2+1][y*2+1][2]])))

                key = int(rgb_mean[0]/32+1)*100 + int(rgb_mean[1]/32+1)*10 + int(rgb_mean[2]/32+1)

                if (key not in color_model.keys()):
                    color_model[key] = [rgb_std[0], rgb_std[1], rgb_std[2], 1]

                else:
                    color_model[key] = [(color_model[key][0]*color_model[key][3]+rgb_std[0])/(color_model[key][3]+1), (color_model[key][1]*color_model[key][3]+rgb_std[1])/(color_model[key][3]+1), (color_model[key][2]*color_model[key][3]+rgb_std[2])/(color_model[key][3]+1), color_model[key][3]+1]

        for x in range(8):
            for y in range(8):
                for z in range(8):
                    key = (x+1)*100 + (y+1)*10 + (z+1)
                    if (key not in color_model.keys()):
                        color_model[key] = [int(random.uniform(8, 15)), int(random.uniform(8, 15)), int(random.uniform(8, 15)), 1]
                    if (color_model[key][0] < 6):
                        color_model[key][0] = int(random.uniform(8, 15))
                    if (color_model[key][1] < 6):
                        color_model[key][1] = int(random.uniform(8, 15))
                    if (color_model[key][2] < 6):
                        color_model[key][2] = int(random.uniform(8, 15))

        valid_input = True

        if(valid_input):
            for i in range(im.size[0]):
                    row_colors = []
                    for j in range(im.size[1]):
                            row_colors.append(pix[i,j])
                    grid_colors.append(row_colors)

            for i in range(num_iterations):
                    new_grid_colors = []
                    grid_colors_list = []
                    for j in range(len(grid_colors[0]) * 2):
                            row_colors = []
                            for k in range(len(grid_colors) * 2):
                                    row_colors.append(generate_color(generate_key(grid_colors[k/2][j/2]) ,grid_colors[k/2][j/2], i))
                                    grid_colors_list.append(generate_color(generate_key(grid_colors[k/2][j/2]) ,grid_colors[k/2][j/2], i))
                            new_grid_colors.append(row_colors)
                    grid_colors = new_grid_colors
            # img = Image.fromarray(grid_colors, 'RGB')
            im2 = Image.new('RGB',(len(grid_colors[0]),len(grid_colors)))
            im2.putdata(grid_colors_list)
            im2.save("up20.jpg")
