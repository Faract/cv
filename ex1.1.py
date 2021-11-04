# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 11:44:37 2021

@author: Faract
"""

for i in range(6):
    figure = open('figure' + str(i + 1) + '.txt')
    lines = figure.readlines()
    MM = float(lines[0])
    hp = len(list(filter(lambda l: l.isdigit(), lines[2].split(' '))))
    res = MM / hp
    print('figure' + str(i + 1) + '-' + str(res))