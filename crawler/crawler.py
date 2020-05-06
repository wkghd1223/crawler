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
import sys
import json

# url을 통해 mat형태의 이미지를 만들어내는 함수
def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    try:
        resp = urllib.request.urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        # return the image
        return image
    except HTTPError:
        return np.zeros(shape=[512, 512, 3], dtype=np.uint8)
    except URLError:
        return np.zeros(shape=[512, 512, 3], dtype=np.uint8)
    except http.client.RemoteDisconnected:
        return np.zeros(shape=[512, 512, 3], dtype=np.uint8)
    except TimeoutError:
        return np.zeros(shape=[512, 512, 3], dtype=np.uint8)


# url_name 배열을 통해 파일에 write한다.
def downLoadUrl(url_name):
    with open('img_list.txt', 'w') as f:
        for item in url_name:
            f.write("%s\n" % item)
        f.close()


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


def downLoadLog(downloadFolder):
    logpath = downloadFolder['log']
    if os.path.getsize(logpath) == 0:
        logs_array = []
        empty = True
    else:
        empty = False
    with open(logpath, 'r') as f:
        if empty:
            None
        else:
            logs_array = json.load(f)
        f.close()

    time_now = datetime.datetime.now()
    del downloadFolder['log']
    downloadFolder['timestamp'] = time_now

    logs_array.append(downloadFolder)
    with open(logpath, 'w') as f:
        json.dump(logs_array, f, default=default, indent=1)
        f.close()


# url_to_image()를 통해 이미지를 가져오고 보여준다.
# 그 후 저장한다.
def select(image_src, folders):
    img = url_to_image(image_src)
    # diff = cv2.subtract(img, np.zeros(shape=[512, 512, 3], dtype=np.uint8))
    # if diff == [0, 0, 0]:
    #     return 'e'
    try:
        resize_img = cv2.resize(img, (1000, 1000))
    except cv2.error as e:
        resize_img = np.zeros(shape=[512, 512, 3], dtype=np.uint8)
#     cv2.imshow('crawled', img)
    cv2.imshow('crawled', resize_img)

    while True:
        key = cv2.waitKey(0) & 0xFF
        if key == ord(folders['errorKey']) or key == ord(folders['errorKey'].upper()):
            return folders['errorKey']
        elif key == ord(folders['endKey']) or key == ord(folders['endKey'].upper()):
            return folders['endKey']
        else:
            for category in folders['category']:
                if key == ord(category['key']):
                    return category['key']


# url_name[] 리스트에 image_src url이 있다면 false를 리턴한다.
def checkDuplicate(logs, image_src):
    if os.path.getsize(logs) == 0:
        return False
    with open(logs, 'r') as f:
        try:
            data = json.load(f)
            for item in data:
                if image_src in item['src']:
                    return True
            f.close()
            return False
        except json.decoder.JSONDecodeError:
            return False


def downLoadImage(url_name, YTN, image_src, folders):
    downloadFolder = folders['errorKey']
    for item in folders['category']:
        if item['key'] == YTN:
            downloadFolder = item

    # 검색어로 폴더 생성
    if not (os.path.isdir(downloadFolder['folder'])):
        os.mkdir(os.path.join(downloadFolder['folder']))

    # 이미지 저장
    try:
        urllib.request.urlretrieve(image_src, downloadFolder['folder'] + "/" + downloadFolder['name'] + "-" + str(downloadFolder['idx']) + ".jpg")

        downLoadUrl(url_name)
        downloadFolder['log'] = folders['log']
        downloadFolder['src'] = image_src
        downLoadLog(downloadFolder)

    except HTTPError as e:
        print(e)
    except URLError as e:
        print(e)
    except http.client.RemoteDisconnected as e:
        print(e)
    except TimeoutError as e:
        print(e)


# yes, no 이미지들 저장하는 디렉토리의 주소를 받는다.(../test_img/yes,no) 그 안의 .jpg로 저장 된 사진들 수 확인 후 다음 인덱스 반환        
def next_Index(path):
    file_list = os.listdir(path)
    file_list_jpg = [file for file in file_list if file.endswith(".jpg")]
    matching = [s for s in file_list_jpg]
    return len(matching)


def _download(url_name, image_src, folders):
    if checkDuplicate(folders['log'], image_src):
        return True
    else:
        c = select(image_src, folders)
        if c == folders['endKey']:
            return False
        elif c == folders['errorKey']:
            error = {
                "src":image_src,
                "key":folders['errorKey'],
                "log": folders['log']
            }
            downLoadLog(error)
        else:
            downLoadImage(url_name, c, image_src, folders)
            for item in folders['category']:
                if c == item['key']:
                    item['idx'] += 1
    return True


def getImage(arg):
    # txt 가져오기
    if not os.path.exists('img_list.txt'):
        url_name = []
    else:
        file = open('img_list.txt', 'r')
        url_name = file.readlines()
        file.close()
        i = 0
        while i < len(url_name):
            url_name[i] = url_name[i].strip()
            i += 1

    with open('config.json') as jf:
        data = json.load(jf)


        # 1. 키워드를 넣고 webdriver 실행
        url = arg
        # 상대경로 또는 txt파일 읽기
        browser = webdriver.Chrome(data['chrome'])
        browser.get(url)

        wait = WebDriverWait(browser, 10)
        # 2. 구글 검색의 작은 이미지들의 공통 클래스를 찾음
        small_images = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'rg_i')))
        small_images.click()
        # small_images = browser.find_elements_by_class_name("rg_i")

        # 3. 작은 이미지를 한번 클릭하여 우측에 상세창 (큰이미지)을 호출 -> url 변경됨
        # small_images[0].click()

        # 3-1. 변경된 url
        current_url = browser.current_url

        # 3-2. 변경된 url로 재호출
        browser.get(current_url)
        
        # 폴더 가져오기
        downloadSrc = data['downloadSrc']
        folders = {
                "log" : data['log'],
                "errorKey":data['errorKey'],
                "endKey":data['endKey'],
                "category":[]
            }
        for item in data['category']:
            idx = next_Index(downloadSrc+'/'+item['folder'])
            folders['category'].append({
                "idx" : idx,
                "key" : item['key'],
                "folder" : downloadSrc+'/'+item['folder'],
                "name" : item['name']
            })

        try:
            # 4. n3VNCb 클래스를 찾을 때 까지 최대 10초 대기
            wait = WebDriverWait(browser, 10)
            # 다음 사진 화살표를 포함하는 클래스를 불러올 때 까지 최대 10초 대기
            wait.until(lambda browsers: browser.find_element_by_css_selector(".CIF8af, .gvi3cf"))
            big_image = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'n3VNCb')))

            # 마지막 사진인지 클래스를 찾음
            last_image = browser.find_elements_by_css_selector(".gvi3cf.RDPZE")

            if len(last_image) > 0:
                # 마지막 사진일 때 사진 저장하고 끝

                # img src 가져옴
                image_src = big_image.get_attribute("src")

                # url_name 배열에 image_src 있는 지 확인 및 아니라면 url_name 배열에 추가
                _download(url_name, image_src, folders)

            else:
                checkEnd = True
                # 마지막 이미지가 아닐 때 반복
                while checkEnd:
                    # if yesIdx & noIdx:
                    #     next_arrow_class = "CIF8af"
                    # else:
                    next_arrow_class = "gvi3cf"

                    # 마지막 이미지인지 클래스로 판별 (마지막 이미지의 오른쪽 화살표 클래스 확인)
                    last_image = browser.find_elements_by_css_selector(".gvi3cf.RDPZE")

                    if len(last_image) > 0:
                        # 마지막 이미지일 때

                        # img src 가져옴
                        image_src = big_image.get_attribute("src")

                        # url_name 배열에 image_src 있는 지 확인 및 아니라면 url_name 배열에 추가
                        checkEnd = _download(url_name, image_src, folders)

                    # 마지막 이미지가 아닐 때
                    else:
                        # img src 가져옴
                        image_src = big_image.get_attribute("src")
                        # print(image_src)

                        # url_name 배열에 image_src 있는 지 확인 및 아니라면 url_name 배열에 추가
                        checkEnd = _download(url_name, image_src, folders)

                        # 다음 사진으로 이동
                        nextImageBtn = browser.find_elements_by_class_name(next_arrow_class)
                        browser.execute_script("arguments[0].click();", nextImageBtn[1])

                        # 변경된 url
                        current_url = browser.current_url

                        # 변경된 url 로 재호출
                        browser.get(current_url)
                        # 다음 사진 화살표를 포함하는 클래스를 불러올 때 까지 최대 10초 대기
                        wait.until(lambda browsers: browser.find_element_by_css_selector(".CIF8af, .gvi3cf"))
                        big_image = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'n3VNCb')))

                browser.close()
        
        except TimeoutException:
            print("Time out")
# src = "https://www.google.com/search?hl=ko&tbs=simg:CAESiQEJB1zSE_1RJseQafgsQsIynCBpiCmAIAxIo1gfxB4AI4AXVB5gB4geXE98C_1gfqNuk2syivKJU07Sf4NNU96zbHNBow_1R6SXhCL4HGLmCMzPh_198yCr-IRFtEitjreG9_1v8_1ZafpwvDgPiipvx5zA10LvvTIAQMCxCOrv4IGgoKCAgBEgTxYBY7DA&sxsrf=ALeKk02Bb9oG2RpnMC-cVImEXCaMOWGUEA:1585879917434&q=%EC%8B%A0%EC%9A%A9+%EC%B9%B4%EB%93%9C+%EC%98%81%EC%88%98%EC%A6%9D&tbm=isch&sa=X&ved=2ahUKEwif9YmJl8voAhW6wosBHUfoB_gQsw56BAgBEAE&biw=1185&bih=761"

if sys.argv[1]:
    getImage(sys.argv[1])
# getImage(src)