
import numpy as np
import cv2
import sys
import math
import os
import numbers
os.chdir(os.path.dirname(sys.argv[0]))
img = cv2.imread("img/image.jpg")
real =cv2.imread("img/real.jpg")
cv2.imshow("image2", cv2.resize(img,(200,200)))
cv2.namedWindow("image2", cv2.WINDOW_NORMAL)  
cv2.namedWindow("image1", cv2.WINDOW_NORMAL)  
r=1/3
g=1/3
b=1/3
clear = lambda: os.system('cls')
def learnc(array1,array2,c,n,r,g,b):
    red=np.array(array1)[:,:,n]
    ar2=np.array(array2)[:,:,0]
    c+=red*(ar2-(r+g+b)*255)/500000
    c=np.average(c)
    return c

def rebin(a, shape):
    sh = shape[0],a.shape[0]//shape[0],shape[1],a.shape[1]//shape[1]
    a=a.reshape(sh).tolist()
    a=np.array(a).mean(-1).mean(1)
    return a

def learna(array1,array2,nevro,r,g,b):
    array1=np.array(array1,dtype=np.uint8)
    array2=np.array(array2,dtype=np.uint8)
    la40=math.floor(len(array1)/4)
    la41=math.floor(len(array1[0])/4)
    array1=np.array(cv2.resize(array1,(la40*4,la41*4)))
    array2=np.array(cv2.resize(array2,(la40*4,la41*4)))
    neuu=np.repeat([nevro], la40 ,axis=0)
    neuu=neuu.reshape(la40*4,4)
    neuu=np.repeat([neuu], la41 ,axis=1)
    neuu=neuu.reshape(len(array1),len(array1[0]))
    if isinstance(array1[0][0],numbers.Number)==False:
        red=array1[:,:,0]*b+array1[:,:,1]*g+array1[:,:,2]*r
    else:
        red=array1
    if isinstance(array2[0][0],numbers.Number)==False:
        red2=array2[:,:,0]*b+array2[:,:,1]*g+array2[:,:,2]*r
    else:
        red2=array2
    neuu+=(red2-red-neuu.mean(0).mean(0)*255)/100000
    neuu=neuu.reshape(la40,la41,4,4).mean(0).mean(0)
    return neuu.tolist()

def use(neuro,array,r,g,b):
    array=np.array(array,dtype=np.uint8)
    la40=math.floor(len(array)/4)
    la41=math.floor(len(array[0])/4)
    array=cv2.resize(array,(la41*4,la40*4))
    array=array.tolist()
    unknow=0
    neuu=np.array(neuro)
    neuu=np.repeat([neuu], la40 ,axis=0)
    neuu=neuu.reshape(la40*4,4)
    neuu=np.repeat([neuu], la41 ,axis=1)
    neuu=neuu.reshape(len(array),len(array[0]))
    ar=np.array(array)
    if isinstance(array[0][0],numbers.Number)==False:
        unknow+=(ar[:,:,0]*b + ar[:,:,1]*g + ar[:,:,2]*r)*neuu
    else:
        unknow+=(ar[:,:])*neuu
    unknow*=16
    unknow=np.where(unknow>255,255,unknow)
    unknow=np.where(unknow<0,0,unknow)
    unknow=rebin(unknow,(la40,la41))
    return unknow
Neu=[[1/16,1/16,1/16,1/16]
    ,[1/16,1/16,1/16,1/16]
    ,[1/16,1/16,1/16,1/16]
    ,[1/16,1/16,1/16,1/16]]
Neu2=[[1/16,1/16,1/16,1/16]
    ,[1/16,1/16,1/16,1/16]
    ,[1/16,1/16,1/16,1/16]
    ,[1/16,1/16,1/16,1/16]]
Neu3=[[1/16,1/16,1/16,1/16]
    ,[1/16,1/16,1/16,1/16]
    ,[1/16,1/16,1/16,1/16]
    ,[1/16,1/16,1/16,1/16]]
result=use(Neu,img,r,g,b)
result=use(Neu2,result,r,g,b)
result=use(Neu3,result,r,g,b)
cv2.imshow("image1", cv2.resize(np.array(result, dtype=np.uint8),(200,200),interpolation=cv2.INTER_AREA))

while True:
    cv2.waitKey(0) 
    clear()
    print("0%")
    r=learnc(img,real,r,2,r,g,b)
    g=learnc(img,real,g,1,r,g,b)
    b=learnc(img,real,b,0,r,g,b)
    Neu=learna(img,real,Neu,r,g,b)
    clear()
    print("20%")
    le=use(Neu,img,r,g,b)
    clear()
    print("40%")
    le2=use(Neu,real,r,g,b)
    clear()
    print("60%")
    Neu2=learna(le,le2,Neu2,r,g,b)
    clear()
    print("80%")
    Neu3=learna(use(Neu2,le,r,g,b),use(Neu2,le2,r,g,b),Neu2,r,g,b)
    result=le
    result=use(Neu2,result,r,g,b)
    clear()
    print("100%")
    result=use(Neu3,result,r,g,b)
    cv2.imshow("image1", cv2.resize(np.array(result, dtype=np.uint8),(200,200),interpolation=cv2.INTER_AREA))
    print("OK")
