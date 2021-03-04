#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 02:36:37 2021

@author: xfh
"""

from PIL import Image
import numpy as np

f_img = Image.open('OIP.jpg').convert('L')
f_mat = np.array(f_img)
for i in range(f_mat.shape[0]):
    for j in range(f_mat.shape[1]):
        if f_mat[i,j] < 180:
            f_mat[i,j] = 0
        else:
            f_mat[i,j] = 255
            
new_img = Image.fromarray(f_mat).convert('RGBA')
new_img.save('map2.png')