
from hashlib import md5
import numpy as np
from tqdm import tqdm
from csv import writer
import os
import sys



if len (sys.argv) != 2 :
    print ("Usage: python DeDup.py <root_dir> or DeDup.exe <root dir> ")
    sys.exit (1)


def file_hash(filename):
    with open(filename, 'rb') as fp:
        return md5(fp.read()).hexdigest()



path = str(sys.argv[1])
file_list=[os.path.join(r,file) for r,d,f in os.walk(path) for file in f]
print("Files in path: ",len(file_list),"\n")


duplicates= []
hash_keys = dict()


for i in tqdm(file_list):
    filehash = file_hash(i)
    if filehash not in hash_keys:
        hash_keys[filehash]= i
    else:
        duplicates.append((i, filehash))

try:
    duplist= open(os.path.join(path,'DuplicatesList.csv'), "w", newline='')
except Exception as e:
    print(e)
    exit(-1)

totalfilesize=0

with duplist:
    csvwriter = writer(duplist,delimiter=',')
    csvwriter.writerow(['Original File','Duplicate File','File Size (KB)'])
    for file_indexes in duplicates:
        filesize = os.stat(file_indexes[0]).st_size   ## Get file size in bytes
        totalfilesize+=filesize
        csvwriter.writerow([hash_keys[file_indexes[1]],file_indexes[0],filesize>>10])

print("Duplicate Files Identified:",len(duplicates),"\n")
print("Total size of duplicates(MB): ", totalfilesize>>20,"\n")    

if(str.lower(input("Validate the compare file. Press Y to proceed with delete "))=='y'):
   for k,v in duplicates:
        try:
            os.remove(k)
        except Exception as e:
            print(e)
   print('Duplicates Deleted','\n')
else:
    print("No changes made",'\n')    

