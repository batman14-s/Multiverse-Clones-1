import os
import random

# BEFORE DELETING
# folderName->
# 	folder1->
# 		file
# 		file
# 		file
# 		file
# 	folder2
# 		file
# 		file
# 		file

# AFTER DELETING
# folderName->
# 	folder1->
# 		file
# 		file
# 	folder2
# 		file


folderName = input("Enter Folder Name")
path = os.getcwd() + '/' + folderName + '/'
# print(path)
for folder in os.listdir(path):  # Go over each folder path
    files = os.listdir(path +'/'+folder+'/')  # Get filenames in current folder
    files = random.sample(files, 2800)  # Pick 900 random files
    for file in files:  # Go over each file name to be deleted
        f = os.path.join(path +'/'+folder+'/', file)  # Create valid path to file
        os.remove(f)  # Remove the file
