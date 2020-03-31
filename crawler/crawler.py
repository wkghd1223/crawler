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


def downLoadLog(url_name):
    with open('log', 'a') as f:
        time_now = datetime.datetime.now()
        time_now = time_now.strftime("[%Y.%m.%d %H:%M:%S]")
        f.write("%s %s\n" % (time_now, url_name))
        f.close()


# url_to_image()를 통해 이미지를 가져오고 보여준다.
# 그 후 저장한다.
def select(image_src):
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


# url_name[] 리스트에 image_src url이 있다면 false를 리턴한다.
def checkDuplicate(url_name, image_src):
    if image_src in url_name:
        print('중복')
        return True
    elif ('.gif' in image_src ):
        return True
    else:
        url_name.append(image_src)
        return False


def downLoadImage(url_name, YTN, image_src, img_save_url, keyword, yesIdx, noIdx, abroadIdx):
    if YTN == 'Y':
        idx = yesIdx
    elif YTN == 'T':
        idx = abroadIdx
    else:
        idx = noIdx

    # 검색어로 폴더 생성

    if not (os.path.isdir(img_save_url)):
        os.mkdir(os.path.join(img_save_url))

    # 이미지 저장
    try:
        urllib.request.urlretrieve(image_src, img_save_url + "/" + keyword + "-" + str(idx) + ".jpg")

        downLoadUrl(url_name)

        temp = YTN + str(idx) + "|" + image_src
        downLoadLog(temp)

    except HTTPError as e:
        print("*** " + str(idx) + "번 째 사진 저장 중 에러 : ")
        print(e)
    except URLError as e:
        print("*** " + str(idx) + "번 째 사진 저장 중 에러 : ")
        print(e)
    except http.client.RemoteDisconnected as e:
        print("*** " + str(idx) + "번 째 사진 저장 중 에러 : ")
        print(e)
    except TimeoutError as e:
        print("*** " + str(idx) + "번 째 사진 저장 중 에러 : ")
        print(e)

# yes, no 이미지들 저장하는 디렉토리의 주소를 받는다.(../test_img/yes,no) 그 안의 .jpg로 저장 된 사진들 수 확인 후 다음 인덱스 반환        
def next_Index(path):
    file_list = os.listdir(path)
    file_list_jpg = [file for file in file_list if file.endswith(".jpg")]
    matching = [s for s in file_list_jpg]
    return len(matching)


def getImage():
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

    # 1. 키워드를 넣고 webdriver 실행
    url = "https://www.google.com/search?hl=ko&tbs=simg:CAESiQEJZMqIHSk2Ci4afgsQsIynCBpiCmAIAxIo1gfVB-IH1wfYB_1EC8QfUB-8HgAjRNMc0wjThPbs0vT7PNNA0xDaONxoweEAbaHuJCyUlTCN_1JvDrk2hGN6MIT1ypwPhyBfbnFUhCDcg83NaCHKy2zg7cGxXRIAQMCxCOrv4IGgoKCAgBEgT412yEDA&q=%EB%A7%A4%EC%B6%9C+%EC%A0%84%ED%91%9C&tbm=isch&sa=X&ved=2ahUKEwift9e_7sHoAhXac3AKHWi0BUEQsw56BAgBEAE&biw=929&bih=888"
    # 상대경로 또는 txt파일 읽기
    browser = webdriver.Chrome("C:\python_test\chromedriver\chromedriver.exe")
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

    img_yes_url = r"..\test_img\yes"
    img_no_url = r"..\test_img\no"
    img_abroad_url = r"..\test_img\abroad"
    yesIdx = next_Index(img_yes_url)
    noIdx = next_Index(img_no_url)
    abroadIdx = next_Index(img_abroad_url)

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
            if checkDuplicate(url_name, image_src):
                None
            else:
                c = select(image_src)
                if c == 'y':
                    # 이미지 저장
                    downLoadImage(url_name, 'Y', image_src, img_yes_url, 'receipt', yesIdx, noIdx, abroadIdx)
                    print("*** 영수증 이미지 저장 완료 ***")
                    yesIdx += 1
                elif c == 'n':
                    # image 저장
                    print("*** 영수증아닌 이미지 저장 완료 ***")
                    downLoadImage(url_name, 'N', image_src, img_no_url, 'not_receipt', yesIdx, noIdx, abroadIdx)
                    noIdx += 1
                elif c == 't':
                    # image 저장
                    print("*** 외국 영수증 이미지 저장 완료 ***")
                    downLoadImage(url_name, 'T', image_src, img_abroad_url, 'abroad_receipt', yesIdx, noIdx, abroadIdx)
                    abroadIdx += 1
                elif c == 'e':
                    print("err")
                else:
                    print('종료합니다.')

        else:
            # 마지막 이미지가 아닐 때 반복
            while True:
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
                    if checkDuplicate(url_name, image_src):
                        None

                    else:
                        c = select(image_src)
                        if c == 'y':
                            # 이미지 저장
                            downLoadImage(url_name, 'Y', image_src, img_yes_url, 'receipt', yesIdx, noIdx, abroadIdx)
                            print("*** 영수증 이미지 저장 완료 ***")
                            yesIdx += 1
                        elif c == 't':
                            # image 저장
                            print("*** 외국 영수증 이미지 저장 완료 ***")
                            downLoadImage(url_name, 'T', image_src, img_abroad_url, 'abroad_receipt', yesIdx, noIdx, abroadIdx)
                            abroadIdx += 1  
                        elif c == 'n':
                            # image 저장
                            print("*** 영수증아닌 이미지 저장 완료 ***")
                            downLoadImage(url_name, 'N', image_src, img_no_url, 'not_receipt', yesIdx, noIdx, abroadIdx)
                            noIdx += 1
                        elif c == 'e':
                            print('err')
                        else:
                            print('종료')

                # 마지막 이미지가 아닐 때
                else:
                    # img src 가져옴
                    image_src = big_image.get_attribute("src")
                    print(image_src)

                    # url_name 배열에 image_src 있는 지 확인 및 아니라면 url_name 배열에 추가
                    if checkDuplicate(url_name, image_src):
                        None
                    else:
                        # image 확인
                        c = select(image_src)
                        if c == 'y':
                            # image 저장
                            downLoadImage(url_name, 'Y', image_src, img_yes_url, 'receipt', yesIdx, noIdx, abroadIdx)
                            print("*** 영수증 이미지 저장 완료 ***")
                            yesIdx += 1
                        elif c == 'n':
                            # image 저장
                            print("*** 영수증아닌 이미지 저장 완료 ***")
                            downLoadImage(url_name, 'N', image_src, img_no_url, 'not_receipt', yesIdx, noIdx, abroadIdx)
                            noIdx += 1
                        elif c == 't':
                            # image 저장
                            print("*** 외국 영수증 이미지 저장 완료 ***")
                            downLoadImage(url_name, 'T', image_src, img_abroad_url, 'abroad_receipt', yesIdx, noIdx, abroadIdx)
                            abroadIdx += 1
                        elif c == 'e':
                            print('err')
                        else:
                            print('종료')
                            break

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

            print(url_name)
            browser.close()

    except TimeoutException:
        print("Time out")


getImage()
