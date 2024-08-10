import os
import numpy as np
import logging
from datetime import datetime
def set_logger(f_name):
    logger = logging.getLogger(__name__)
    fh = logging.FileHandler(f_name)
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)
    return logger


origin_path = r'C:\Users\yiyao.tang\Desktop\Fake_photo\fake_using_phone'
fake_path = r'C:\Users\yiyao.tang\Desktop\Origin3'

now = datetime.now()
current_time = now.strftime("%Y-%m-%d_%H-%M-%S")
f_name = os.path.join('Rename'+current_time+'.txt')
logger = set_logger(f_name)
old_origin_names = os.listdir(origin_path)
old_fake_names = os.listdir(fake_path)
print(len(old_fake_names),len(old_origin_names))
print(old_origin_names,old_fake_names)
for i,name in enumerate(old_origin_names):
    logger.warning(i)
    logger.warning(name)

os.chdir(fake_path)
# fake_names = os.listdir(fake_path)
for i,name in enumerate(old_fake_names):
    os.rename(name,old_origin_names[i])
