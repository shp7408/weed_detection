from PIL import *
import cv2, numpy as np
import matplotlib.pylab as plt
import glob
import requests
import json
import time
import os


print("===== start ===== ")

 



# 평균 해시로 변환 method
def tohash(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = cv2.resize(gray, (64,64))

    avg = gray.mean()

    bins = 1 * (gray > avg)

    return bins

 

# 해밍 거리 측정 method
def hamming(a,b):

    a = a.reshape(1, -1)

    b = b.reshape(1, -1)

    distance = (a != b).sum()

    return distance


                
 

while True:
    
    
    # take a picture first
    #os.system('wget http://192.168.0.96:8091/?action=snapshot -O 0204_image_first.jpg')
    #print("take a picture first  //  file list : ")
    #print(os.listdir(os.getcwd()))

    #60second delay
    #time.sleep(10)
    
    print("")
    
    print("===== while start ===== ")
    
    print("5 second later take a picture")
    time.sleep(1)
    
    print("4 second later take a picture")
    time.sleep(1)
    
    print("3 second later take a picture")
    time.sleep(1)
    
    print("2 second later take a picture")
    time.sleep(1)
    
    print("1 second later take a picture")
    time.sleep(1)


    # take a picture second
    os.system('wget http://192.168.0.2:8091/?action=snapshot -O 0204_image_second.jpg')
    print("take a picture first  //  file list : ")
    print(os.listdir(os.getcwd()))
    
        
    #comparing fist and second 
    img1 = cv2.imread('/home/pi/fdCam/0204_image_first.jpg')
    img2 = cv2.imread('/home/pi/fdCam/0204_image_second.jpg')


    imgs = [img1, img2]

    white = np.arange(2)






    # 이미지의 해밍거리 계산

    img1_hash = tohash(img1)

    img2_hash = tohash(img2)

    dst = hamming(img1_hash, img2_hash)

    if dst/256 > 0.3 :
        #smilarity higer than 10% and white(green) pixels increase !! 
        #in case of a litle change, : 0.10546875 
        print("== 1. image changed ")
        print("no same picture : ","해밍거리 값 : ",dst/256) # 해밍 거리 출력

        
        # hand or plant
        if dst/256 > 0.9 :
            print("== 1(1). hand in")
            
            
        else :
            print("== 1(2). plant in")
            
            white = np.arange(2)

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

                

            if(white[1]-white[0]>6000) :

                print("1(2)-1 잡초가 나타났습니다.")
                print("no same picture : ","해밍거리 값 : ",dst/256) # 해밍 거리 출력
                print("how many white pixels : ",white)        
                print("white[1] - white[0] :", white[1] - white[0] )
                
                #FCM
                serverToken = 'AAAArVqyUkk:APA91bHhS90vKQZ09y70Cm3FSDhCezwEdCI-I8ZhS-joS01clMUI22wCet0JeaH4hcOJfK281QRarz4INArpkZmkiEUbPSUK-8gFDcEZLKcyNsyNYSrgXu-NlLHI3n-m_G3C_caIdiI3'

                deviceToken = 'fe6DJH9UQO2mM27WtIxeoG:APA91bFpCAzxzlViwgvYxac0rVjTbYdpadpsat6RIV9wu2G0gzXCots6vsZLdIpwr1AxqMfsuXvcjZQdG3YqWcybr1LHMblDQXgYk4OnsWx6bYWTXj--bcrVmD13UMW6hSE8tRmP_4Bp'

                headers = {'Content-Type': 'application/json','Authorization': 'key=' + serverToken}

                body = {'notification': {'title': 'SmartFarm','body': '잡초가 있습니다.'},'to': deviceToken, 'data': {'title': 'SmartFarm','body': '잡초가 있습니다.'}}

                response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))

                print(response.status_code)
                
            else :
                print("1(2)-1 잡초 X")
                print("no same picture : ","해밍거리 값 : ",dst/256) # 해밍 거리 출력
                print("how many white pixels : ",white)        
                print("white[1] - white[0] :", white[1] - white[0] )
                
                # change file name second -> first


           

    
            
        
    else :

        print("== 2. image unchanged ")

        print("해밍거리 값 : ",dst/256)
        print("해밍거리 값 bigger 10%: ",dst/256 > 0.06)

        
        

    os.rename('/home/pi/fdCam/0204_image_second.jpg', '/home/pi/fdCam/0204_image_first.jpg')
    print("file name second -> first  //  file list : ")
    print(os.listdir(os.getcwd()))


    print("===== while end ===== ")




print("===== end ===== ")

