import random
import numpy as np
import cv2
import math
import os
img = cv2.imread("img/image.jpg")
real =cv2.imread("img/image.jpg")
cv2.imshow("image2", cv2.resize(img,(100,100)))
r=1/3
g=1/3
b=1/3
clear = lambda: os.system('cls')
def change(array,x):
    newarray=[]
    for element in array:
        if type(element)==list:
            newarray.append(change(element,x))
        else:
            newarray.append(element+(random.random()-0.5)*x)
    return newarray
def learnc(array1,array2,c,n,r,g,b):
    lla=len(array1)
    llb=len(array1[0])
    for ii in range(len(array1)):
        for jj in range(len(array1[0])):
            red=array1[ii][jj][n]
            c+=red*(array2[ii][jj][0]-(r+g+b)*255)/100000/len(array1)**2
        print("learn:",math.floor((ii*llb+jj)/(lla*llb)*100), "% complete")
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
                    nevro[ax][bx]-=(ar-red)/100000/len(array1)**2
        print("learn:",math.floor((ii*llb+jj)/(lla*llb)*100), "% complete")
    return nevro

def use(neuro,array):
    output=[]
    lla=len(array)/4
    llb=len(array[0])/4
    for ii in range(math.floor(len(array)/4)):
        output.append([])
        for jj in range(math.floor(len(array[0])/4)):
            unknow=0
            for ax in range(0,4):
                for bx in range(0,4):
                    neuu=neuro[ax][bx]
                    if isinstance(array[ii*4+ax][jj*4+bx],int)==False:
                        unknow+=(array[ii*4+ax][jj*4+bx][0]*b + array[ii*4+ax][jj*4+bx][1]*g + array[ii*4+ax][jj*4+bx][2]*r)*neuu
                    else:
                        unknow+=(array[ii*4+ax][jj*4+bx])*neuu
            unknow=math.floor(unknow)
            if unknow>255:
                unknow=255
            if unknow<0:
                unknow=0
            output[ii].append(unknow)
        print("vizualize:",math.floor((ii*llb+jj)/(lla*llb)*100), "% complete")
    return output
Neu=[[1/16,1/16,1/16,1/16],[1/16,1/16,1/16,1/16],[1/16,1/16,1/16,1],[1/16,1/16,1/16,1/16]]
Neu2=[[1/16,1/16,1/16,1/16],[1/16,1/16,1/16,1/16],[1/16,1/16,1/16,1],[1/16,1/16,1/16,1/16]]
Neu3=[[1/16,1/16,1/16,1/16],[1/16,1/16,1/16,1/16],[1/16,1/16,1/16,1],[1/16,1/16,1/16,1/16]]
result=use(Neu,img)
result=use(Neu2,result)
#result=use(Neu3,result)
cv2.imshow("image1", cv2.resize(np.array(result, dtype=np.uint8),(100,100)))
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
    #Neu3=learna(use(Neu2,le),use(Neu2,le2),Neu3,r,g,b)
    result=le
    result=use(Neu2,result)
    #result=use(Neu3,result)
    cv2.imshow("image1", cv2.resize(np.array(result, dtype=np.uint8),(100,100)))
    print("OK")
