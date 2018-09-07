'''
Created on Feb 20, 2017
@author: jumabek
'''
# -*- coding: utf-8 -*-
from os import listdir
from os.path import isfile, join
import argparse
import numpy as np
import sys
import os
import shutil
import random 
import math

width_in_cfg_file = 416.
height_in_cfg_file = 416.

def IOU(x,centroids):
    similarities = []
    k = len(centroids)
    for centroid in centroids:
        c_w,c_h = centroid
        w,h = x
        if c_w>=w and c_h>=h:
            similarity = w*h/(c_w*c_h)
        elif c_w>=w and c_h<=h:
            similarity = w*c_h/(w*h + (c_w-w)*c_h)
        elif c_w<=w and c_h>=h:
            similarity = c_w*h/(w*h + c_w*(c_h-h))
        else: #means both w,h are bigger than c_w and c_h respectively
            similarity = (c_w*c_h)/(w*h)
        similarities.append(similarity) # will become (k,) shape
    return np.array(similarities) 

def avg_IOU(X,centroids):
    n,d = X.shape
    sum = 0.
    for i in range(X.shape[0]):
        #note IOU() will return array which contains IoU for each centroid and X[i] // slightly ineffective, but I am too lazy
        sum+= max(IOU(X[i],centroids)) 
    return sum/n

def write_anchors_to_file(centroids,X,anchor_file):
    f = open(anchor_file,'w')
    
    anchors = centroids.copy()
    print(anchors.shape)

    for i in range(anchors.shape[0]):
        anchors[i][0]*=width_in_cfg_file
        anchors[i][1]*=height_in_cfg_file
         

    widths = anchors[:,0]
    sorted_indices = np.argsort(widths)

    print('Anchors = ', anchors[sorted_indices])
        
    for i in sorted_indices[:-1]:
        f.write('%d,%d, '%(anchors[i,0],anchors[i,1]))

    #there should not be comma after last anchor, that's why
    f.write('%d,%d\n'%(anchors[sorted_indices[-1:],0],anchors[sorted_indices[-1:],1]))
    
    f.write('%f\n'%(avg_IOU(X,centroids)))
    print()

def kmeans(X,centroids,eps,anchor_file):
    
    N = X.shape[0]
    iterations = 0
    k,dim = centroids.shape
    prev_assignments = np.ones(N)*(-1)    
    iter = 0
    old_D = np.zeros((N,k))

    while True:
        D = [] 
        iter+=1           
        for i in range(N):
            d = 1 - IOU(X[i],centroids)
            D.append(d)
        D = np.array(D) # D.shape = (N,k)
        
        print("iter {}: dists = {}".format(iter,np.sum(np.abs(old_D-D))))
            
        #assign samples to centroids 
        assignments = np.argmin(D,axis=1)
        
        if (assignments == prev_assignments).all() :
            print("Centroids = ",centroids)
            write_anchors_to_file(centroids,X,anchor_file)
            return

        #calculate new centroids
        centroid_sums=np.zeros((k,dim),np.float)
        for i in range(N):
            centroid_sums[assignments[i]]+=X[i]        
        for j in range(k):            
            centroids[j] = centroid_sums[j]/(np.sum(assignments==j))
        
        prev_assignments = assignments.copy()     
        old_D = D.copy()  

def main(argv):
	parser = argparse.ArgumentParser()
	wd = os.getcwd()
	default_output_dir = wd + '\\model_data\\'
	
	parser.add_argument('-output_dir', default = default_output_dir, type = str, 
						help='Output anchor directory\n' )  
	parser.add_argument('-num_clusters', default = 9, type = int,  # change default number of cluster from 0 to 9
						help='number of clusters\n' )


	args = parser.parse_args()

	if not os.path.exists(args.output_dir):
		os.mkdir(args.output_dir)
	
	lines = os.listdir('./labels')

	annotation_dims = []
	path_prefix = './labels/'

	for line in lines:
		print(path_prefix + line)
		f2 = open(path_prefix + line)
		for line in f2.readlines():		# format of line：pic_id x y w h
			line = line.rstrip('\n')
			w,h = line.split(' ')[3:]   # 从 line 中获取 w h (都是比例)           
			annotation_dims.append(tuple(map(float,(w,h))))
	annotation_dims = np.array(annotation_dims)

	eps = 0.005

	if args.num_clusters == 0:
		for num_clusters in range(1,11): #we make 1 through 10 clusters 
			anchor_file = join( args.output_dir,'my_anchors.txt')

			# 从图片集中随机找出 num_clusters 个图片作为 k-means 的初始化中心
			indices = [ random.randrange(annotation_dims.shape[0]) for i in range(num_clusters)]
			centroids = annotation_dims[indices]
			
			kmeans(annotation_dims,centroids,eps,anchor_file)
			print('centroids.shape', centroids.shape)
	else:
		anchor_file = join( args.output_dir,'anchors%d.txt'%(args.num_clusters))
		indices = [ random.randrange(annotation_dims.shape[0]) for i in range(args.num_clusters)]
		centroids = annotation_dims[indices]
		kmeans(annotation_dims,centroids,eps,anchor_file)
		print('centroids.shape', centroids.shape)

if __name__=="__main__":
    main(sys.argv)