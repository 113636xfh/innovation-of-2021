#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 15:30:35 2021

@author: xfh
"""

import numpy as np
#import cv2
from matplotlib import pyplot as plt

class A_stay:
    def __init__(self,map_path,begin,end):
        self.map_path = map_path
        self.map = np.zeros((*self.read_map().shape,4))
        self.map[:,:,0] = self.read_map()
        self.open_list = []
        self.close_list = []
        if (self.map[(*begin,0)] == 1 and self.map[(*begin,0)] == 1):
            self.begin = begin
            self.end = end
        else:
            print('终点或起点不可抵达')
        
# =============================================================================
#     def load_img(self):
#         img = cv2.imread(self.map_path)
#         img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         ret, img_b = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
#         my_map = np.zeros((*(img_b.shape),4))
#         my_map[:,:,0] = img_b
#         self.map = my_map
# =============================================================================
        
    def read_map(self):
        #self.map = cv2.imread(self.map_path)
        return plt.imread(self.map_path)[:,:,0]
    
    def get_g(self,node):
# =============================================================================
#         1   2   3
#         4   5   6
#         7   8   9
# =============================================================================
        p = self.map[(*node,1)]
        x,y = (p-1)%3-1,(p-1)//3-1
        if p in [1,3,7,9]:
            distance = 14 + self.map(node[0] + x,node[1] + y,2)
        elif p in [2,4,6,8]:
            distance = 10 + self.map(node[0] + x,node[1] + y,2)
        elif p == 5:
            distance = 0
        else:
            raise Exception("路径指向错误")
        #self.map[(*node,2)] = distance
        return distance
    
    def get_h(self):
        distance = np.abs(np.array(self.begin) - np.array(self.end))
        distance = min(distance) * 0.4 + max(distance) 
        distance *= 10
        return distance
    
    def search(self):
        self.open_list.sort(key = lambda x: self.map[(*x,2)] + self.map[(*x,3)])
        p_tu = self.open_list.pop(0)
        self.close_list.append(p_tu)
        for i in range(p_tu[0]-1,p_tu[0]+2):
            for j in range(p_tu[1]-1,p_tu[1]+2):
                try:
                    if (i < 0 or j < 0) or (i == 0 and j == 0):
                        continue
                    if self.map[i,j,0] == 1 and not((i,j) in self.open_list) and \
                        not ((i,j) in self.close_list):
                        self.open_list.append((i,j))
                        self.map[i,j,2] = self.get_g(p_tu)
                        self.map[i,j,3] = self.get_h()
                    elif self.map[i,j,0] == 1 and (i,j) in self.open_list:
                        old_p = self.map[i,j,1]
                        old_g = self.map[i,j,2]
                        self.map[i,j,1] = 5 - (3*(i - p_tu[0]) + (j - p_tu[1]))
                        new_g = self.get_g(p_tu)
                        if old_g < new_g:
                            self.map[i,j,1] = old_p
                    
                except IndexError:
                    pass
    
    def return_path(self):
        way = []
        way.append(self.end)
        i,j = self.end
        while not((i,j) == self.begin):
            i += (self.map[i,j,1]-1)//3-1
            j += (self.map[i,j,1]-1)%3-1
            way.append(i,j)
        return way
   
    def main(self):
        self.open_list.append(self.begin)
        #self.map[(*self.begin,2)] = self.get_g(self.begin)
        self.read_map()
        while not (self.end in self.open_list):
            self.search()
        return self.return_path()
            
a = A_stay('map1.png',(0,0),(49,49))
a.main()
        
        
    
