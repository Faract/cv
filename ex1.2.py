# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 12:13:25 2021

@author: Faract
"""
img1 = load_image('img1.txt')
img2 = load_image('img2.txt')

def load(path):
    file = open(path)
    lines = file.readlines()
    file.close()
    return list(map(lambda l: list(filter(lambda d: d.isdigit(), l.split(' '))), lines[2:]))
 
 
def fp(img):
    for y in range(len(img)):
        for x in range(len(img[0])):
            if img[y][x] == '1':
                return y, x
 

img1_fp = fp(img1)
img2_fp = fp(img2)
 
print(img1_fp[0] - img2_fp[0], img1_fp[1] - img2_fp[1])