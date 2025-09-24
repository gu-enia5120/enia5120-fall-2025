import glob
import os
list1=glob.glob('*.png')
# print(list1)

with open('../slides.ipynb', 'r') as file:
    text = file.read() 

for filename in list1: 
    if filename not in text:
        print("not found (removing)", filename)
        os. remove(filename)
    # else:
    #     print("found",filename)
