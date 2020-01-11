
import hashlib
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import time
import numpy as np
from tqdm import tqdm
import shutil
import csv
import os



def file_hash(filename):
    with open(filename, 'rb') as fp:
        return hashlib.md5(fp.read()).hexdigest()



path = 'H:\\Virtual Machines\\'
file_list=[os.path.join(r,file) for r,d,f in os.walk(path) for file in f]
print(len(file_list))


duplicates= []
hash_keys = dict()


for i in tqdm(file_list[10:]):
#for i in itertools.islice(file_list , 1, 5000):
    filehash = file_hash(i)
    if filehash not in hash_keys:
        hash_keys[filehash]= i
    else:
        duplicates.append((i, filehash))


# In[28]:


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


# In[29]:


#os.mkdir('duplicates')


# In[35]:



   # shutil.move(file_indexes[0],os.getcwd()+'/duplicates/'+hash_keys[file_indexes[1]])
with open('c:\\temp\\myduplist.csv', "w", newline='') as duplist:
    csvwriter = csv.writer(duplist,delimiter=',')
    csvwriter.writerow(['Duplicate File','Orginal File'])
    for file_indexes in duplicates:
        csvwriter.writerow([file_indexes[0],hash_keys[file_indexes[1]]])
    


