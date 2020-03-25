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


# url을 통해 mat형태의 이미지를 만들어내는 함수
def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    # return the image
    return image


# url_name 배열을 통해 파일에 write한다.
def downLoadUrl(url_name, yesIdx, noIdx):
    with open('img_list.txt', 'w') as f:
        for item in url_name:
            f.write("%s\n" % item)
        f.close()
    saveYesOrNo(yesIdx, noIdx)


# url_to_image()를 통해 이미지를 가져오고 보여준다.
# 그 후 저장한다.
def select(image_src):
    img = url_to_image(image_src)
    cv2.imshow('crawled', img)
    key = cv2.waitKey(0) & 0xFF 
    if key == ord('d'): # d 누르면 사진 저장 안 함 건너뜀.
        return False;
    else: # d 제외 아무 키나 누르면 저장 후 넘어감.
        return True;


# url_name[] 리스트에 image_src url이 있다면 false를 리턴한다.
def checkDuplicate(url_name, image_src):
    if image_src in url_name:
        print('중복')
        return True
    else:
        url_name.append(image_src)
        return False


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


# yes && no의 각각의 인덱스 저장 필수
def saveYesOrNo(yes, no):
    if not (os.path.isdir('yesorno.txt')):
        os.mkdir(os.path.join('yesorno.txt'))
    file = open('yesorno.txt', 'w')
    line = [yes, no]
    file.writelines(line)
    file.close()


def getImage(keyword, limit):

    # txt 가져오기
    if not os.path.isdir('/img_list.txt'):
        os.mkdir(os.path.join('img_list.txt'))
    file = open('img_list.txt', 'r')
    url_name = file.readlines()
    file.close()

    # 1. 키워드를 넣고 webdriver 실행
    url = "https://www.google.com/search?sa=G&hl=ko&tbs=simg:CAESlAIJgYPO5GpeA_1EaiAILELCMpwgaYQpfCAMSJ-MH1gfxAuQH4geiE98HgQiACFGAPtg0yT2-NMM0vTTcNLs05j2VJxowGn5EtIaKdQKzfscIX7kX2uipNqtuHeFfE64UxgswmpnF-8ponJjXJh2-LlC_1SOp6IAQMCxCOrv4IGgoKCAgBEgSY8YtqDAsQne3BCRqBAQoWCgR3b29k2qWI9gMKCggvbS8wODN2dAoYCgZudW1iZXLapYj2AwoKCC9tLzA1ZndiChUKA2lua9qliPYDCgoIL20vMDN5aGsKGgoGdGlja2V02qWI9gMMCgovbS8wMnB5MzUxChoKB3JlY2VpcHTapYj2AwsKCS9tLzA0Z2NsOQw&sxsrf=ALeKk02tN6a7ee2VYscAuj5EH2-axS-Orw:1585042036739&q=%EC%8B%A0%EC%9A%A9+%EC%B9%B4%EB%93%9C+%EC%A0%84%ED%91%9C+%EC%98%81%EC%88%98%EC%A6%9D&tbm=isch&ved=2ahUKEwiS3bbc5bLoAhXCdd4KHQqsCBQQsw56BAgBEAE&biw=1536&bih=722"
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
    img_yes_url = "../test_img/yes"
    img_no_url = "../test_img/no"
    # yesIdx = 1
    # noIdx = 1

    # txt 가져오기
    if not (os.path.isdir('yesorno.txt')):
        yesIdx = 1
        noIdx = 1
    else:
        file = open('yesorno.txt', 'r')
        line = file.readlines()
        yesIdx = int(line[0])
        noIdx = int(line[1])
        file.close()

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
                if select(image_src):
                    # 이미지 저장
                    downLoadImage(image_src, img_yes_url, keyword, yesIdx)
                    print("*** 이미지 저장 완료 ***")
                    yesIdx += 1
                else:
                    # image 저장
                    downLoadImage(image_src, img_no_url, keyword, noIdx)
                    noIdx += 1

            # URL 저장
            downLoadUrl(url_name, yesIdx)
            print("*** URL 저장 완료 ***")

        else:
            # 마지막 이미지가 아닐 때 반복
            while not isLastImage:
                if yesIdx == 1 & noIdx == 1:
                    next_arrow_class = "CIF8af"
                else:
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
                        if select(image_src):
                            # 이미지 저장
                            downLoadImage(image_src, img_yes_url, keyword, yesIdx)
                            print("*** 이미지 저장 완료 ***")
                            yesIdx += 1
                        else:
                            # image 저장
                            downLoadImage(image_src, img_no_url, keyword, noIdx)
                            noIdx += 1

                    isLastImage = True
                    # URL 저장
                    downLoadUrl(url_name, yesIdx)
                    print("*** URL 저장 완료 ***")
                    # 마지막 이미지가 아닐 때

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
                        if select(image_src):
                            # image 저장
                            downLoadImage(image_src, img_yes_url, keyword, yesIdx)
                            yesIdx += 1
                        else:
                            # image 저장
                            downLoadImage(image_src, img_no_url, keyword, noIdx)
                            noIdx += 1
                        if limit == yesIdx:
                            break

                    # 다음 사진으로 이동
                    nextImageBtn = browser.find_elements_by_class_name(next_arrow_class)
                    nextImageBtn[1].click()

                    # 변경된 url
                    current_url = browser.current_url

                    # 변경된 url 로 재호출
                    browser.get(current_url)
                    wait = WebDriverWait(browser, 10)
                    # 다음 사진 화살표를 포함하는 클래스를 불러올 때 까지 최대 10초 대기
                    wait.until(lambda browsers: browser.find_element_by_css_selector(".CIF8af, .gvi3cf"))
                    big_image = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'n3VNCb')))

            print(url_name)
            browser.close()

    except TimeoutException:
        print("Time out")


getImage("test1", 10)
