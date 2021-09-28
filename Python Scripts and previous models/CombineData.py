import os
import random
import shutil

count = 0
for personName in os.listdir(os.getcwd()):
    personNamePath = os.path.join(os.getcwd(), personName)
    if os.path.isdir(personNamePath)==True and personName!='data':
        for handSignName in os.listdir(personNamePath):
            imageFolderPath = os.path.join(personNamePath, handSignName)
            for imageName in os.listdir(imageFolderPath):
                imagePath = os.path.join(imageFolderPath, imageName)
                destination = os.getcwd()+'/data/'+handSignName+'/'+str(count)+'.jpg'
                print(imagePath, destination)
                count += 1
                shutil.copy2(imagePath,destination)