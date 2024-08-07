import cv2
import numpy as np
import os
import pickle

pieces={}
for i in os.listdir(os.getcwd()+'\\pieces'):
    pieces[i.split(".")[0]]=cv2.resize(cv2.cvtColor(cv2.imread(os.getcwd()+f'\\pieces\\{i}'),cv2.COLOR_BGR2GRAY),(100,100))

im=cv2.imread('pieces.png')
height,width=int(im.shape[0]/2),int(im.shape[1]/8)
c=0
last=None
masks={}
for yy in range(0,im.shape[0],height):
    if im.shape[0]-yy>0.5*height:
        for xx in range(0,im.shape[1],width):
            if im.shape[1]-xx>0.5*width:
                i=im[yy:yy+height,xx:xx+width]
                x=list(i)
                lower=np.array([210]*3)
                upper=np.array([255]*3)
                mask=cv2.inRange(i,lower,upper)
                mask=cv2.resize(mask,(100,100))
                cv2.imshow('m',mask)
                cv2.waitKey(0)
                name=input("piece name: ")
                masks[name]=mask
pickle.dump(masks,open("whitepieces.pkl","wb"))
                
#40->130
#210->255
#magic formula d=cv2.subtract(cv2.bitwise_or(last,mask),cv2.bitwise_and(last,mask))