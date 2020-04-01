import urllib.request
from urllib.request import HTTPError, URLError
import http.client
from concurrent.futures import TimeoutError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import numpy as np
import cv2
from selenium.common.exceptions import JavascriptException
import time
import datetime
import os


def scanf():
    while True:
        key = input()
        if key == 'n' or key == 'N':
            return 'n'
        elif key == 'y' or key == 'Y':
            return 'y'
        elif key == 'q' or key == 'Q':
            return 'q'
        elif key == 't' or key == 'T':
            return 't'
        elif key == 'e' or key == 'E':
            return 'e'
        else:
            print('e, t, n, y, q 중 하나 선택')


def move_img(filename, filename_frame, judgement):

    old_dir = os.getcwd()
    img = cv2.imread(filename)
    idx_list = []

    if judgement == 'y':
        new_name = 'receipt'
        os.chdir(r"..\yes")
    elif judgement == 'n':
        new_name = 'not_receipt'
        os.chdir(r"..\no")
    else:
        new_name = 'abroad_receipt'
        os.chdir(r"..\abroad")

    i = len(os.listdir('.'))

    cv2.imwrite(new_name+"-"+ str(i) +".jpg", img)

    os.chdir(old_dir)

    # readme파일 포함
    i = len(os.listdir('.')) - 2

    os.remove(filename)
    os.rename(filename_frame + "-"+ str(i) +".jpg", filename)

def select_img(filename):
    img = cv2.imread(filename)
    # diff = cv2.subtract(img, np.zeros(shape=[512, 512, 3], dtype=np.uint8))
    # if diff == [0, 0, 0]:
    #     return 'e'
    try:
        resize_img = cv2.resize(img, (1000, 1000))
    except cv2.error as e:
        resize_img = np.zeros(shape=[512, 512, 3], dtype=np.uint8)
        return 'e'
#     cv2.imshow('crawled', img)
#     cv2.imshow(filename, resize_img)
    cv2.imshow('crawled', resize_img)
    while True:
        key = cv2.waitKey(0) & 0xFF
        if key == ord('n') or key == ord('N'):
            return 'n'
        elif key == ord('y') or key == ord('Y'):
            return 'y'
        elif key == ord('q') or key == ord('Q'):
            return 'q'
        elif key == ord('t') or key == ord('T'):
            return 't'
        elif key == ord('e') or key == ord('E'):
            return 'e'
        else:
            print('e, t, n, y, q 중 하나 선택')

# yes, no 이미지들 저장하는 디렉토리의 주소를 받는다.(../test_img/yes,no) 그 안의 .jpg로 저장 된 사진들 수 확인 후 다음 인덱스 반환
def next_Index(path):
    file_list = os.listdir(path)
    file_list_jpg = [file for file in file_list if file.endswith(".jpg")]
    matching = [s for s in file_list_jpg]
    return len(matching)


def getImage():

    print('which folder do you want to classify?')
    print('y: yes\tn: no\tt: abroad')
    key = scanf()
    if key == 'y':
        url = r"..\test_img\yes"
    elif key =='n':
        url = r"..\test_img\no"
    else:
        url= r"..\test_img\abroad"


    n = next_Index(url) - 1
    i = 0
    filename_frame = key == 'y' and 'receipt' or key == 'n' and 'not_receipt' or 'abroad_receipt'

    os.chdir(url)

    try:
        while n > i:

            filename = filename_frame+ '-'+ str(i) + '.jpg'
            key = select_img(filename)
            if key == 'q':
                break
            elif key == 'e':
                None
            else:
                move_img(filename, filename_frame, key)

            print(filename)
            i += 1

    except TimeoutException:
        print("Time out")

getImage()