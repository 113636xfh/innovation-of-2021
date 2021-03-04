#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 23:51:49 2021

@author: xfh

"""

import sys
import numpy as np
import time
import os
#import cv2
from matplotlib import pyplot as plt
from PIL import Image

def my_time(fun):
    def f(*args):
        begin = time.time()
        fu = fun(*args)
        end = time.time()
        print(str(fun.__name__),'time:',1000*(end-begin),'ms')
        return fu
    return f

class Video:
    def __init__(self,dire,m,my_map):
        self.dire = dire
        self.max = m
        self.map = my_map
        
        if not os.path.isdir(self.dire):
            os.makedirs(self.dire)
    
    def rm_img(self):
        f_list = os.listdir(self.dire)
        if f_list:
            for i in f_list:
                i = os.path.join(self.dire,i)
                os.remove(i)
                
    def resize(self,mat):
        f_img = Image.fromarray(np.uint8(mat))
        i,j = f_img.size
        i,j = (1080,int(1080/i*j))  if i>j else (int(1080/j*i),1080)     
        f_img = f_img.resize((i,j))
        mat = np.array(f_img)
        return mat
    
    @my_time            
    def save_img(self,ls,funs):
        img_mat = np.zeros((*(self.map.shape),3))
        img_mat = self.map.reshape((*(self.map.shape),1)) + img_mat
        #img_mat = self.resize(img_mat)
        for j,fun in zip(ls,funs):
            img_mat = fun(j,img_mat)
        plt.imsave(self.dire+str(time.time())+'.png',img_mat)
    
    @my_time
    def setting(fun):
        def f(self,node_list,mat):
            for i in node_list:
                mat = fun(self,mat,i)
            return mat    
        return f
    
    @setting
    def red(self,mat,i):
        mat[(*i,0)] = self.max
        mat[(*i,1)] = 0
        mat[(*i,2)] = self.max
        return mat
    
    @setting
    def blue(self,mat,i):
        mat[(*i,0)] = 0
        mat[(*i,1)] = self.max
        mat[(*i,2)] = self.max
        return mat
    
    @setting    
    def green(self,mat,i):
        mat[(*i,0)] = self.max
        mat[(*i,1)] = self.max
        mat[(*i,2)] = 0
        return mat
    
# =============================================================================
#     @my_time     
#     def set_red(self,node_list,mat):
#         for i in node_list:
#             mat[(*i,0)] = self.max
#             mat[(*i,1)] = 0
#             mat[(*i,2)] = self.max
#         return mat
#     
#     @my_time        
#     def set_blue(self,node_list,mat):
#         for i in node_list:
#             mat[(*i,0)] = 0
#             mat[(*i,1)] = self.max
#             mat[(*i,2)] = self.max
#         return mat
#     
#     @my_time 
#     def set_green(self,node_list,mat):
#         for i in node_list:
#             mat[(*i,0)] = self.max
#             mat[(*i,1)] = self.max
#             mat[(*i,2)] = 0
#         return mat
# =============================================================================
    

        
# =============================================================================
#     def save_img2(self,li):
#         dic = 'picture/'
#         img_mat = np.zeros((*(self.map.shape),3))
#         img_mat = self.map.reshape((*(self.map.shape),1)) + img_mat
#         for i in self.open_list:
#             img_mat[(*i,2)] = 0
#         for i in self.close_list:
#             img_mat[(*i,0)] = 0
#         for i in li:
#             img_mat[(*i,1)] = 0
#         plt.imsave(dic+str(time.time())+'.png',img_mat) 
# 
# =============================================================================
class My_map:
    def __init__(self,img,rate):
        self.map = plt.imread(img)
        if self.map.shape[-1] > 1:
            self.map = self.map[:,:,0]
        self.father = np.zeros((*self.map.shape,2)).astype('int')
        self.g = np.zeros(self.map.shape)
        self.h = np.zeros(self.map.shape)
        self.f = self.g + self.h
        self.open_list = []
        self.close_list = []
        self.walkable = self.map.max()
        self.rate = rate
        
        self.vdieo = Video('picture/',self.walkable,self.map)
        self.vdieo.rm_img()
    
    def get_g(self,node):
        father = tuple(self.father[node[0],node[1],:])
        #print(father)
        if father[0] != node[0] and father[1] != node[1]:
            return 14 + self.g[father]
        else:
            return 10 + self.g[father]
    
    def get_h(self,node):
        dx = np.abs(self.end[0] - node[0])
        dy = np.abs(self.end[1] - node[1])
        d = min(dx,dy)*4 + max(dx,dy)*10
        return d*self.rate
    
    def get_f(self,node):
        return self.g[node] + self.h[node]
    
    def set_father(self,node,father):
        self.father[node[0],node[1],:] = father
    
    def update_open_list(self,node,nodes):
        for n in nodes:
            if not n in self.open_list:
                self.set_father(n,node)
                self.g[n] = self.get_g(n)
                self.h[n] = self.get_h(n)
                self.f[n] = self.get_f(n)
                self.open_list.append(n)
            else:
                father_old = tuple(self.father[n[0],n[1],:])
                self.set_father(n,node)
                new_g = self.get_g(n)
                if new_g < self.g[n]:
                    self.g[n] = new_g
                else:
                    self.set_father(n,father_old)
    
    def search(self,node):
        l = []
        for i in range(node[0]-1,node[0]+2):
            for j in range(node[1]-1,node[1]+2):
                if not(self.map.shape[0]>i>=0 and self.map.shape[1]>j>=0):
                    continue
                elif self.map[i,j] != self.walkable:
                    continue
                elif (i,j) in self.close_list:
                    continue
                else:
                    l.append((i,j))
        return l
    
    def return_way(self,node):
        l = [node]
        while tuple(self.father[node[0],node[1],:]) != self.begin:
            node = tuple(self.father[node[0],node[1],:])
            l.append(node)
            #self.save_img2(l)
            self.vdieo.save_img((l,),(self.vdieo.red,))
        return l
    
    def set_begin_end(self,begin,end):
        self.begin = begin
        self.end = end
        if self.map[begin] != self.walkable or self.map[end] != self.walkable:
            print('终点或起点不可抵达')
            sys.exit(1)
        else:
            self.open_list.append(begin)
            self.h[begin] = self.get_h(begin)
            self.f[begin] = self.get_f(begin)
    
    def ergodic_list(self):
        self.open_list.sort(key = lambda x:self.f[x])
        node = self.open_list.pop(0)
        self.close_list.append(node)
        return node
    
    
           
def a_star(map_path,begin,end):
    my_map = My_map(map_path,0.1)
    my_map.set_begin_end(begin,end)
    while not (my_map.end in my_map.open_list) and my_map.open_list:
        node = my_map.ergodic_list()
        neibors = my_map.search(node)
        my_map.update_open_list(node,neibors)
        #my_map.save_img()   
        my_map.vdieo.save_img((my_map.open_list,my_map.close_list),\
        (my_map.vdieo.green,my_map.vdieo.blue))
    return my_map.return_way(end)

if __name__ == '__main__':
    path = 'map4.png'
    begin = (49,0)
    end = (49,49)
    my_map = plt.imread(path)
    print(my_map[begin],my_map[end])
    way = a_star(path,begin,end)
    for node in way:
        my_map[(*node,1)] = 0
    
    plt.imshow(my_map)
    plt.show()
        