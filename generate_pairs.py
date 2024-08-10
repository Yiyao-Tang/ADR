import os
import numpy as np
import shutil
from datetime import datetime
import logging
import argparse
def read_names(root_dir):
    all_paths = [x for x in os.walk(root_dir)]
    folder_names  = all_paths[0][1]
    return folder_names

def set_logger(proj_dir,f_name):
    logger = logging.getLogger(__name__)
    fh = logging.FileHandler(f_name)
    fh.setLevel(logging.WARNING)
    logger.addHandler(fh)
    return logger

def read_photo(root_dir):
    all_photos = []
    photo_paths = []
    all_paths = [x for x in os.walk(root_dir)]
    for i,one_path in enumerate(all_paths):
        all_photos.append(one_path[-1])
        photo_paths.append(os.path.split(one_path[0])[1])
    print(all_paths)
    #print(all_photos[1:])
    return all_photos[1:],photo_paths[1:]

def create_match(i,one_person_photos,logger,folder_names):
    for id_1,photo1 in enumerate(one_person_photos) :
        for id_2,photo2 in enumerate(one_person_photos[id_1+1:]) :
            # print(folder_names[i],photo1+' '+photo2+' '+str(1))
            # logger.warning(photo1+' '+photo2+' '+str(1))
            print(os.path.join(folder_names[i],photo1)+' '+os.path.join(folder_names[i],photo2)+' '+str(1))
            logger.warning(os.path.join(folder_names[i],photo1)+' '+os.path.join(folder_names[i],photo2)+' '+str(1))
            #print(photo1,photo2,1)

def pair_generate(root_dir,logger):
    all_photo,photo_paths = read_photo(root_dir)
    folder_names = read_names(root_dir)
    print(np.shape(folder_names))
    print(np.shape(all_photo[0]))
    for i,one_person_photos in enumerate(all_photo):
        #print('The size of ',i, ' is ',np.shape(one_person_photos))
        create_match(i,one_person_photos,logger,photo_paths)
        create_unmatch(one_person_photos,i,all_photo,logger,photo_paths)

def create_unmatch(one_person_photos,i,all_photos,logger,folder_names):
    for m,photo1 in enumerate(one_person_photos):
        #print(one_person_photos)
        for k,photos in enumerate([x for id,x in enumerate(all_photos) if id>i]):
             for j,photo2 in enumerate(photos):
                 #print(i,m,photo1,k+i+1,j,photo2,0)
                 print(os.path.join(folder_names[i],photo1)+' '+os.path.join(folder_names[k+i+1],photo2)+' '+str(0))
                 logger.warning(os.path.join(folder_names[i],photo1)+' '+os.path.join(folder_names[k+i+1],photo2)+' '+str(0))

def combine_folders(root_dir,label_dir):
    folder_names = read_names(root_dir)
    #print(folder_names)
    userinfo_names = os.listdir(label_dir)
    userinfo_id = [x[:-4] for x in userinfo_names]
    for x in userinfo_names:
        oldfile = os.path.join(label_dir,x)
        newfile = os.path.join(root_dir,x[:-4])
        shutil.copy(oldfile,newfile)
        os.remove(oldfile)
    mask_photos = [x for x in folder_names if x.endswith('M')]
    for x in mask_photos :
        scr = os.path.join(root_dir,x)
        dest = os.path.join(root_dir,x[:-1])

        mask_photo_names = os.listdir(scr)
        for photo in mask_photo_names:
            shutil.copy(os.path.join(root_dir,x,photo),dest)
            os.remove(os.path.join(root_dir,x,photo))
    #print()
            #print(os.path.join(root_dir,x,photo),dest)

                #print(photo1,photo2,0)
parser = argparse.ArgumentParser()
parser.add_argument('-r','--root_dir', required = True,type=str,help='the root directory')
parser.add_argument('-l','--label_dir', required = True ,type = str, help='the userinfo directory')
args = parser.parse_args()
root_dir,label_dir = args.root_dir,args.label_dir
proj_dir = os.getcwd()
now = datetime.now()
current_time = now.strftime("%Y-%m-%d_%H-%M-%S")
f_name = os.path.join(proj_dir,'pairs'+current_time+'.txt')
logger = set_logger(proj_dir,f_name)

combine_folders(root_dir,label_dir)
pair_generate(root_dir,logger)
