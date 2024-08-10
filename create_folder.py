import os

def create_dir(src_dir,dest_dir):
    out_loop_count = 0
    root = src_dir
    rel_paths = [(x[0].replace(src_dir,'')) for x in os.walk(src_dir)]
    abs_in_paths = [(src_dir+x) for x in rel_paths]
    abs_out_paths = [(dest_dir+x) for x in rel_paths]
    files = [[x[2] for x in os.walk(src_dir)]]
    for folder in abs_out_paths:
        try:
            os.makedirs(folder)
        except FileExistsError:
            print ("Directory %s already exists" % folder)
        else:
            print ("Successfully created the directory %s" % folder)
    return abs_in_paths, abs_out_paths


# src_dir = r'C:\Users\yiyao.tang\Desktop\root_folder'
# dest_dir = r'C:\Users\yiyao.tang\Desktop\dest_dir'
# create_folders(src_dir,dest_dir)
