import tensorflow
import os
import mtcnn
from matplotlib import pyplot
import numpy as np
import cv2
import os
import logging
from datetime import datetime


multiple_count = 0
one_count = 0
zero_count = 0
out_count = 0

def crop_photo(write_path,read_path,k,copy_original,log_only,logger):
    image_names,imgs = read_images(read_path)
    faces = detector(imgs)
    if log_only == 1:
        only_log_imgs(faces,imgs,image_names,read_path,k,logger)
    else:
        save_imgs(faces,imgs,image_names,write_path,read_path,k,copy_original,logger)
    # print("Exceeds the max size after scaling:",out_count)
    # print("One face detected in the image:",one_count)
    # print("Not detected:",zero_count)
    # print("Multiple face detected:",multiple_count,'\n')

def log_stats(logger):
    global multiple_count
    global one_count
    global zero_count
    global out_count
    logger.warning("\nExceeds the max size after scaling: %d"%out_count)
    logger.warning("Photos of one face detected: %d"%one_count)
    logger.warning("Photos of no face detected: %d"%zero_count)
    logger.warning("Photos of multiple face detected:%d "%multiple_count)
    logger.warning("Successful cropped photos: %d"%(one_count+multiple_count-out_count))
    logger.warning("Total number of faces in the source directory: %d"%(one_count+zero_count+multiple_count))
def max_img(face):
    product = []
    for i,face_i in enumerate(face):
        product.append(np.prod(face_i["box"][2:]))
        max_prod = max(product)
        max_idx = [i for i, prod in enumerate(product) if prod == max_prod][0]
    return (face[max_idx]["box"])

def set_logger(f_name):
    logger = logging.getLogger(__name__)
    fh = logging.FileHandler(f_name)
    fh.setLevel(logging.WARNING)
    logger.addHandler(fh)
    return logger

def read_images(read_path):
    format = ('png','PNG','jpg','JPG','jpeg','JPEG','gif','GIF','jfif','JFIF')
    os.chdir(read_path)
    files = os.listdir(read_path)
    image_names = []
    for f in files:
        if (f.endswith(format) ):
            image_names.append(f)
    imgs = []
    for img_name in image_names:
        n = cv2.imread(img_name,1)
        imgs.append(n)
    return image_names,imgs

def detector(imgs):
    detector = mtcnn.MTCNN()
    faces=[]
    #imgs = tensorflow.convert_to_tensor(imgs)
    for img in (imgs):
        faces.append(detector.detect_faces(img))
    return faces

def save_imgs(faces,imgs,image_names,write_path,read_path,k,copy_original,logger):
    global multiple_count
    global one_count
    global zero_count
    os.chdir(write_path)
    for i,face in enumerate(faces):
            if (np.shape(face)[0] > 1):
                multiple_face(i,face,imgs,image_names,read_path,k,logger)
                multiple_count +=1
            elif(np.shape(face)[0] == 1):
                one_face(i,face,imgs,image_names,read_path,k,logger)
                one_count+=1
            else:
                no_face(i,imgs,image_names,read_path,copy_original,logger)
                zero_count+=1

def one_face(i,face,imgs,image_names,read_path,k,logger):
    out_boundary = 0
    x,y,w,h = face[0]["box"]
    out_boundary = ((int(x-0.5*(k-1)*w)<0)|(int(x+w+0.5*(k-1)*w)>(np.shape(imgs[i])[1])))
    if (out_boundary==1):
        logger.warning(os.path.join(read_path,str(image_names[i]))+", exceeds the boundary")
        cv2.imwrite(image_names[i],imgs[i])
    #     out_count += 1
    else:
        cropped_img = imgs[i][:,int(x-0.5*(k-1)*w):int(x+w+0.5*(k-1)*w)]
        cv2.imwrite(image_names[i],cropped_img)

def no_face(i,imgs,image_names,read_path,copy_original,logger):
    logger.warning(os.path.join(read_path,str(image_names[i]))+", no face detected")
    if copy_original==True:
        cv2.imwrite(image_names[i],imgs[i])

def multiple_face(i,face,imgs,image_names,read_path,k,logger):
    out_boundary = 0
    x,y,w,h = max_img(face)
    out_boundary = ((int(x-0.5*(k-1)*w)<0)|(int(x+w+0.5*(k-1)*w)>(np.shape(imgs[i])[1])))
    if (out_boundary==1):
        logger.warning(os.path.join(read_path,str(image_names[i]))+", exceeds the boundary")
        cv2.imwrite(image_names[i],imgs[i])
    #     global out_count
    #     out_count += 1
    else:
        cropped_img = imgs[i][:,int(x-0.5*(k-1)*w):int(x+w+0.5*(k-1)*w)]
        cv2.imwrite(image_names[i],cropped_img)

def only_log_imgs(faces,imgs,image_names,read_path,k,logger):
    for i,face in enumerate(faces):
            if (np.shape(face)[0] > 1):
                out_boundary = 0
                x,y,w,h = max_img(face)
                out_boundary = ((int(x-0.5*(k-1)*w)<0)|(int(x+w+0.5*(k-1)*w)>(np.shape(imgs[i])[1])))
                if (out_boundary==1):
                    logger.warning(os.path.join(read_path,str(image_names[i]))+", exceeds the boundary")
                    global out_count
                    out_count += 1
                global multiple_count
                multiple_count +=1
            elif(np.shape(face)[0] == 1):
                out_boundary = 0
                x,y,w,h = face[0]["box"]
                out_boundary = (int((y-0.5*(k-1)*h)<0)|(int((y+0.5*(k-1)*h+h))>(np.shape(imgs[i])[0]))|(int(x-0.5*(k-1)*w)<0)|(int(x+w+0.5*(k-1)*w)>(np.shape(imgs[i])[1])))
                if (out_boundary==1):
                    logger.warning(os.path.join(read_path,str(image_names[i]))+", exceeds the boundary")
                    out_count += 1
                global one_count
                one_count+=1
            else:
                logger.warning(os.path.join(read_path,str(image_names[i]))+", no face detected")
                global zero_count
                zero_count+=1


now = datetime.now()
current_time = now.strftime("%Y-%m-%d_%H-%M-%S")
f_name = os.path.join('Rename'+current_time+'.txt')

write_path = r'C:\Users\yiyao.tang\Desktop\Renamed'
read_path = r'C:\Users\yiyao.tang\Desktop\Origin4'
k = 3.4
copy_original= True
log_only = False
logger = set_logger(f_name)
crop_photo(write_path,read_path,k,copy_original,log_only,logger)
