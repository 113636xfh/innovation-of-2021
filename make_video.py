#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 03:31:12 2021

@author: xfh
"""

import moviepy.video.io.ImageSequenceClip as mp
import os
import time
import numpy as np
from PIL import Image

f_dir = 'picture/'
fps = 20
f_list = os.listdir(f_dir)
f_list = list(map(lambda x: os.path.join(f_dir,x),f_list))
f_list.sort()

def return_mat(f_list):
    f_mats = []
    for f in f_list:
        f_img = Image.open(f)
        f_img = f_img.resize((x*3 for x in f_img.size))
        f_mat = np.array(f_img)
        f_mats.append(f_mat)
    return f_mats


clip = mp.ImageSequenceClip(return_mat(f_list),fps=fps)
clip.write_videofile(time.strftime('video/'+"%Y-%m-%d_%H:%M:%S", time.localtime())+'.mp4')

