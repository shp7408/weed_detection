from PIL import *

import cv2, numpy as np

import matplotlib.pylab as plt

import glob

import requests

import json

import time

 

# 평균 해시로 변환

def tohash(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = cv2.resize(gray, (16,16))

    avg = gray.mean()

    bins = 1 * (gray > avg)

    return bins

 

# 해밍 거리 측정

def hamming(a,b):

    a = a.reshape(1, -1)

    b = b.reshape(1, -1)

    distance = (a != b).sum()

    return distance

 

 

while True:

    img1 = cv2.imread('/Users/aym/smartFarm/defalut.jpg')

    img2 = cv2.imread('/Users/aym/smartFarm/snapshot_defalut.jpg')

 

    # cv2.imshow('query', img1)

    imgs = [img1, img2]

    white = np.arange(2)

 

    # 녹색이 더 많은지 계산

    for i, img in enumerate(imgs) :

        #---① 각 이미지를 HSV로 변환

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, (36,0,0), (86,255,255))

        ## slice the green

        imask = mask>0

        green = np.zeros_like(img, np.uint8)    

        green[imask] = img[imask]

        # 마스크 색을 흰색으로 바꾸기

        coloured = green.copy()

        coloured[mask == 255] = (255, 255, 255)

        #흰 색인 픽셀의 개수를 세기

        white[i] = np.sum(coloured == 255)

 

    # 이미지의 해밍거리 계산

    img1_hash = tohash(img1)

    img2_hash = tohash(img2)

    dst = hamming(img1_hash, img2_hash)

    if dst/256 > 0.01 and white[0]<white[1] :

        print("잡초가 나타났습니다.")

        print("유사도 O","해밍거리 값",dst/256) # 해밍 거리 출력

        print(white)

        #FCM
#         serverToken = 'AAAArVqyUkk:APA91bHhS90vKQZ09y70Cm3FSDhCezwEdCI-I8ZhS-joS01clMUI22wCet0JeaH4hcOJfK281QRarz4INArpkZmkiEUbPSUK-8gFDcEZLKcyNsyNYSrgXu-NlLHI3n-m_G3C_caIdiI3'
#         deviceToken = 'fe6DJH9UQO2mM27WtIxeoG:APA91bFpCAzxzlViwgvYxac0rVjTbYdpadpsat6RIV9wu2G0gzXCots6vsZLdIpwr1AxqMfsuXvcjZQdG3YqWcybr1LHMblDQXgYk4OnsWx6bYWTXj--bcrVmD13UMW6hSE8tRmP_4Bp'

 
#         headers = {'Content-Type': 'application/json','Authorization': 'key=' + serverToken}

#         body = {'notification': {'title': 'SmartFarm','body': '잡초가 있습니다.'},'to': deviceToken, 'data': {'title': 'SmartFarm','body': '잡초가 있습니다.'}}

#         response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))

#         print(response.status_code)

    else :

        print("잡초가 없습니다")

        print("유사도 X","해밍거리 값",dst/256) 

        print(white)

    time.sleep(60)