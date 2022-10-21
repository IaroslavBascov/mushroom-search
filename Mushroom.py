import random
import numpy as np
import cv2
import sys
import math
import os
os.chdir(os.path.dirname(sys.argv[0]))
img = cv2.imread("img/image.jpg")
real =cv2.imread("img/image.jpg")
cv2.imshow("image2", cv2.resize(img,(200,200)))
r=1/3
g=1/3
b=1/3
clear = lambda: os.system('cls')
def learnc(array1,array2,c,n,r,g,b):
    red=np.array(array1)[:,:,n]
    ar2=np.array(array2)[:,:,0]
    c+=red*(ar2-(r+g+b)*255)/50000
    c=np.average(c)
    return c

def learna(array1,array2,nevro,r,g,b):
    lla=len(array1)/4
    llb=len(array1[0])/4
    for ii in range(math.floor(len(array1)/4)):
        for jj in range(math.floor(len(array1[0])/4)):
            for ax in range(0,4):
                for bx in range(0,4):
                    if isinstance(array2[ii*4+ax][jj*4+bx],int)==True:
                        ar=array2[ii*4+ax][jj*4+bx]
                    else:
                        ar=int(array2[ii*4+ax][jj*4+bx][0])
                    if isinstance(array1[ii*4+ax][jj*4+bx],int)==False:
                        red=array1[ii*4+ax][jj*4+bx][0]*b+array1[ii*4+ax][jj*4+bx][1]*g+array1[ii*4+ax][jj*4+bx][2]*r
                    else:
                        red=array1[ii*4+ax][jj*4+bx]
                    nevro[ax][bx]-=(ar-red)/10000/len(array1)**2
        print("learning arrays:",math.floor((ii*llb+jj)/(lla*llb)*100), "% complete")
    return nevro

def use(neuro,array):
    thisvariable=isinstance(array[0][0],int) or isinstance(array[0][0],float)
    unknow=0
    neuu=np.array(neuro)
    neuu=np.repeat(neuu, math.floor(len(array)/4) ,axis=0)
    neuu=np.repeat(neuu, math.floor(len(array[0])/4) ,axis=1)
    ar=np.array(array)
    if thisvariable==False:
        unknow+=(ar[:,:,0]*b + ar[:,:,1]*g + ar[:,:,2]*r)*neuu
    else:
        unknow+=(ar[:,:])*neuu
    #a=np.array(range(0,math.floor(len(array)/4)))
    #unknow=np.average(unknow,[a*4,a*4+4])
    #b=np.array(range(0,math.floor(len(array)/4)))
    #unknow[a]=np.average(unknow[a],[b*4,b*4+4])
    return unknow
Neu=[[1/16,1/16,1/16,1/16],[1/16,1/16,1/16,1/16],[1/16,1/16,1/16,1],[1/16,1/16,1/16,1/16]]
Neu2=[[1/16,1/16,1/16,1/16],[1/16,1/16,1/16,1/16],[1/16,1/16,1/16,1],[1/16,1/16,1/16,1/16]]
Neu3=[[1/16,1/16,1/16,1/16],[1/16,1/16,1/16,1/16],[1/16,1/16,1/16,1],[1/16,1/16,1/16,1/16]]
r=learnc(img,real,r,2,r,g,b)
g=learnc(img,real,g,1,r,g,b)
b=learnc(img,real,b,0,r,g,b)
result=use(Neu,img)
result=use(Neu2,result)
cv2.imshow("image1", cv2.resize(np.array(result, dtype=np.uint8),(200,200)))
while True:
    cv2.waitKey(0) 
    clear()
    r=learnc(img,real,r,2,r,g,b)
    g=learnc(img,real,g,1,r,g,b)
    b=learnc(img,real,b,0,r,g,b)
    Neu=learna(img,real,Neu,r,g,b)
    le=use(Neu,img)
    le2=use(Neu,real)
    Neu2=learna(le,le2,Neu2,r,g,b)
    result=le
    result=use(Neu2,result)
    cv2.imshow("image1", cv2.resize(np.array(result, dtype=np.uint8),(200,200)))
    print("OK")
