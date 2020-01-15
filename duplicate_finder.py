
import hashlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import time
import numpy as np
from tqdm import tqdm
import shutil
import csv
import os, sys


if len (sys.argv) != 2 :
    print ("Usage: python duplicate_finder.py <root_dir> ")
    sys.exit (1)


def file_hash(filename):
    with open(filename, 'rb') as fp:
        return hashlib.md5(fp.read()).hexdigest()



path = str(sys.argv[1])
file_list=[os.path.join(r,file) for r,d,f in os.walk(path) for file in f]
print("Files in path: "len(file_list))


duplicates= []
hash_keys = dict()


for i in tqdm(file_list):
    filehash = file_hash(i)
    if filehash not in hash_keys:
        hash_keys[filehash]= i
    else:
        duplicates.append((i, filehash))


# # for file_indexes in duplicates:
#     try:
#         plt.subplot(121),plt.imshow(Image.open(file_indexes[0]))
#         dupfilename = file_indexes[0]
#         plt.title(dupfilename[6:11]+ ' duplicate')
#         plt.subplot(122),plt.imshow(Image.open(hash_keys[file_indexes[1]]))
#         orgfilename=str(hash_keys[file_indexes[1]])
#         plt.title(orgfilename[6:11])
#         plt.show()
#     except OSError as e:
#         continue
try:
    duplist= open(os.path.join(path,'DuplicatesList.csv'), "w", newline='')
except Exception as e:
    print(e)
    exit(-1)

totalfilesize=0

with duplist:
    csvwriter = csv.writer(duplist,delimiter=',')
    csvwriter.writerow(['Original File','Duplicate File','File Size (KB)'])
    for file_indexes in duplicates:
        filesize = os.stat(file_indexes[0]).st_size   ## Get file size in bytes
        totalfilesize+=filesize
        csvwriter.writerow([hash_keys[file_indexes[1]],file_indexes[0],filesize>>10])

print("Duplicate Files Identified:",len(duplicates),"\n")
print("Total size of duplicates: ", totalfilesize,"\n")    
if(str.lower(input("Validate the compare file. Press Y to proceed with delete "))=='y'):
   for k,v in duplicates:
        try:
            os.remove(k)
        except Exception as e:
            print(e)
print("Duplicates Deleted","\n")