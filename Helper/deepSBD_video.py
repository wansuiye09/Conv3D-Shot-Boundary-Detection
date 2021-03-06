#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import os
import glob
import pandas as pd

root_deepSBD = 'directory to the deepSBD folder'

output_folder='output tv2007d2' #'output tv2007t'

top_folder = "tv2007d/synthetic/sharps" #"tv2007t/synthetic/sharps"
top_children = os.path.join(root_deepSBD,top_folder)
top_dirs = [entry.path for entry in os.scandir(top_children) if entry.is_dir()]

#extract all shots with at least 10 frames from the deepSBD dataset
def vids_10():
    count = 0  
    for folders in top_dirs:
        dirs = [entry.path for entry in os.scandir(folders) if entry.is_dir()] 
        
        #loop over shots to create the 16 frame videos
        for shot in dirs:
            #get image index of cut from alpha.py
            meta_data = pd.read_csv(os.path.join(shot, 'alpha.py'))
            cut = int(meta_data.columns[0])
            if cut > 9:
  
                #create mpv video
                img_array = []
                #only take the snipetes without a cut
                for filename in glob.glob(shot + '/*.jpg')[:cut]:
                    img = cv2.imread(filename)
                    height, width, layers = img.shape
                    size = (width,height)
                    img_array.append(img)
                 
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                output = output_folder + '/vd_{}.mp4'.format(count)
                print(output)
                writer = cv2.VideoWriter(output,fourcc, 15, size)
                 
                for i in range(len(img_array)):
                    writer.write(img_array[i])
                writer.release()
                count +=1
        
vids_10()