import tensorflow
import os
import mtcnn
from matplotlib import pyplot
import numpy as np
import cv2
import os
import logging
import Crop_photo_tool
import argparse
import create_folder
from datetime import datetime


parser = argparse.ArgumentParser()
parser.add_argument('-s','--src_path', required = True,type=str,help='the source path')
parser.add_argument('-d','--destination_path', required = True ,type = str, help='the destination path')
parser.add_argument('-k', '--scaling_parameter', required = True, type = float, help='the scaling parameter')
parser.add_argument('-c','--copy_original', action =  'store_true', help='copy the original photo if no face detected')
parser.add_argument('-l','--log_only', action =  'store_true', help='Only log the info without saving the cropped pics ')
args = parser.parse_args()
dest_dir, src_dir, k, copy_original,log_only = args.destination_path, args.src_path, args.scaling_parameter, args.copy_original,args.log_only
proj_dir = os.getcwd()
abs_in_dirs,abs_out_dirs = create_folder.create_dir(src_dir,dest_dir)

now = datetime.now()
current_time = now.strftime("%Y-%m-%d_%H-%M-%S")
f_name = os.path.join(proj_dir,'face_crop_'+current_time+'.txt')
logger = Crop_photo_tool.set_logger(proj_dir,f_name)

for i,in_dir in enumerate(abs_in_dirs):
    print("\n Current source directory is: " , in_dir)
    Crop_photo_tool.crop_photo(abs_out_dirs[i],in_dir,k,copy_original,log_only,logger)
Crop_photo_tool.log_stats(logger)
