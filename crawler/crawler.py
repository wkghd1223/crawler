import urllib.request
from urllib.request import HTTPError, URLError
import http.client
from concurrent.futures import TimeoutError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import cv2
from selenium.common.exceptions import JavascriptException
import time
import os


def downLoadImage(image_src, img_save_url, keyword, idx):
    # 검색어로 폴더 생성

    if not (os.path.isdir(img_save_url)):
        os.mkdir(os.path.join(img_save_url))

    # 이미지 저장
    try:
        urllib.request.urlretrieve(image_src, img_save_url + "/" + keyword + "-" + str(idx) + ".jpg")
        print("이미지 저장 " + str(idx))
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


def getImage(keyword, limit):

    file = open('img_list.txt', 'r')
    url_name = file.readlines()

    print(url_name)


    # 1. 키워드를 넣고 webdriver 실행
    url = "https://google.com/search?q=" + keyword + "&tbm=isch"
    browser = webdriver.Chrome("C:\python_test\chromedriver\chromedriver.exe")
    browser.get(url)

    # 2. 구글 검색의 작은 이미지들의 공통 클래스를 찾음
    small_images = browser.find_elements_by_class_name("rg_i")

    # 3. 작은 이미지를 한번 클릭하여 우측에 상세창 (큰이미지)을 호출 -> url 변경됨
    small_images[0].click()

    # 3-1. 변경된 url
    current_url = browser.current_url

    # 3-2. 변경된 url로 재호출
    browser.get(current_url)

    isLastImage = False
    img_save_url = "../test_img/" + keyword
    idx = 1
    pre_image_src = ""

    try:
        # 4. n3VNCb 클래스를 찾을 때 까지 최대 10초 대기
        wait = WebDriverWait(browser, 10)
        # 다음 사진 화살표를 포함하는 클래스를 불러올 때 까지 최대 10초 대기
        wait.until(lambda browser: browser.find_element_by_css_selector(".CIF8af, .gvi3cf"))
        big_image = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'n3VNCb')))

        # 마지막 사진인지 클래스를 찾음
        last_image = browser.find_elements_by_css_selector(".gvi3cf.RDPZE")

        if len(last_image) > 0:
            # 마지막 사진일 때 사진 저장하고 끝

            # img src 가져옴
            image_src = big_image.get_attribute("src")

            # 이미지 저장
            downLoadImage(image_src, img_save_url, keyword, idx)
            print("*** 이미지 저장 완료 ***")

        else:
            # 마지막 이미지가 아닐 때 반복
            while isLastImage == False:
                if idx == 1:
                    next_arrow_class = "CIF8af"
                else:
                    next_arrow_class = "gvi3cf"

                # 마지막 이미지인지 클래스로 판별 (마지막 이미지의 오른쪽 화살표 클래스 확인)
                last_image = browser.find_elements_by_css_selector(".gvi3cf.RDPZE")

                if len(last_image) > 0:
                    # 마지막 이미지일 때

                    # img src 가져옴
                    image_src = big_image.get_attribute("src")

                    # 이미지 저장
                    downLoadImage(image_src, img_save_url, keyword, idx)
                    print("*** 이미지 저장 완료 ***")

                    isLastImage = True

                else:
                    # 마지막 이미지가 아닐 때

                    # img src 가져옴
                    image_src = big_image.get_attribute("src")
                    print(image_src)
                    if pre_image_src == image_src:
                        print("*** 중복 src 건너뜀 ***")

                        # pre_image_src = ""

                        # 다음 사진으로 이동
                        nextImageBtn = browser.find_elements_by_class_name(next_arrow_class)
                        nextImageBtn[1].click()

                        # 변경된 url
                        current_url_url = browser.current_url

                        # 변경된 url로 재호출
                        browser.get(current_url)
                        wait = WebDriverWait(browser, 10)
                        # 다음 사진 화살표를 포함하는 클래스를 불러올 때 까지 최대 10초 대기
                        wait.until(lambda browser: browser.find_element_by_css_selector(".CIF8af, .gvi3cf"))
                        big_image = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'n3VNCb')))

                        continue
                    else:
                        pre_image_src = image_src

                        # 이미지 저장
                        downLoadImage(image_src, img_save_url, keyword, idx)

                        if limit == idx:
                            break

                        # 다음 사진으로 이동
                        nextImageBtn = browser.find_elements_by_class_name(next_arrow_class)
                        nextImageBtn[1].click()

                        # 변경된 url
                        current_url = browser.current_url

                        # 변경된 url로 재호출
                        browser.get(current_url)
                        wait = WebDriverWait(browser, 10)
                        # 다음 사진 화살표를 포함하는 클래스를 불러올 때 까지 최대 10초 대기
                        wait.until(lambda browser: browser.find_element_by_css_selector(".CIF8af, .gvi3cf"))
                        big_image = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'n3VNCb')))

                        # index 1 증가
                        idx += 1

            browser.close()

    except TimeoutException:
        print("Time out")

getImage("receipt test", 1)

## 5works 어깨깡패 전현태 매니저 사진을 키워드에 넣어봤습니다.
