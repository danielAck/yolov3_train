# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
	

def convert_annotation(out_file, file_path, image_id):
	in_file = open('Annotations/%s.xml'%(image_id))
	tree=ET.parse(in_file)
	root = tree.getroot()
	size = root.find('size')
	w = int(size.find('width').text)
	h = int(size.find('height').text)

	out_file.write(file_path)

	for obj in root.iter('object'):
		difficult = obj.find('difficult').text
		cls = obj.find('name').text
		if cls not in classes or int(difficult) == 1:
			continue
		cls_id = classes.index(cls)
		xmlbox = obj.find('bndbox')
		b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
		out_file.write(" " + ",".join([str(a) for a in b]) + "," + str(cls_id))

	out_file.write('\n')

if __name__ == '__main__':

	classes = ['bottle']
	filelist = os.listdir('./img')
	out_file = open('train.txt', 'w')
	wd = getcwd()
	
	for file in filelist:
		image_id = file.split('.')[0]
		file_path = wd + '\\img\\' + file
		convert_annotation(out_file, file_path, image_id)
