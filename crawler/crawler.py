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

def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    # return the image
    return imagedef downLoadURl(image_src, img_save_url, keyword, idx):
    link=np.array()
    try:
    except:
    link=np.append(img.get_attribute('src')
                   
        
    file=("img_list.txt",link)     
    print("URL 저장"+str(idx))
def downLoadUrl(url_name):
    with open('img_list.txt', 'w') as f:
        for item in url_name:
            f.write("%s\n" % item)

    
def select(image_src):
    img = url_to_image(image_src)
    cv2.imshow('crawled',img)
    key = cv2.waitKey(0) & 0xFF 
    if key == ord('d'): # d 누르면 사진 저장 안 함 건너뜀.
        return False;
    else: # d 제외 아무 키나 누르면 저장 후 넘어감.
        return True;
    
    cv2.destroyAllWindow();

def checkDuplicate(url_name, image_src):
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

            # url_name 배열에 image_src 있는 지 확인 및 아니라면 url_name 배열에 추가
            if checkDuplicate(url_name, image_src):
                return
            #URL 저장
            downLoadUrl(url_name)
            print("*** URL 저장 완료 ***")

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

                    # url_name 배열에 image_src 있는 지 확인 및 아니라면 url_name 배열에 추가
                    if checkDuplicate(url_name, image_src):
                        isLastImage = True
                        continue
                    # URL 저장
                    downLoadUrl(url_name)
                    print("*** URL 저장 완료 ***")

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

                        # 이미지 저장                        pre_image_src = image_src
                        if select(image_src):
                            # 이미지 저장
                            downLoadImage(image_src, img_save_url, keyword, idx);

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


def point(path_of_img):
    img = cv2.imread(path_of_img)
    src = img.copy()
    # point = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    size = 800.0
    r = size / img.shape[0]
    dim = (int(img.shape[1] * r), int(size))
    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (1, 1), 7)
    edged = cv2.Canny(gray, 75, 200)
    cv2.imshow("edge", edged)
    cv2.waitKey(0)

    (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    print(cnts)
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            screenCnt = approx
            break

    cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 2)
    cv2.imshow("asf", img)
    cv2.waitKey(0)

    rect = order_point(screenCnt.reshape(4, 2) / r)
    (topLeft, topRight, bottomRight, bottomLeft) = rect

    v1 = abs(bottomRight[0] - bottomLeft[0])
    v2 = abs(topRight[0] - topLeft[0])
    h1 = abs(topRight[1] - bottomRight[1])
    h2 = abs(topLeft[1] - bottomLeft[1])
    minWidth = min([v1, v2])
    minHeight = min([h1, h2])

    dst = np.float32([[0, 0], [minWidth - 1, 0], [minWidth - 1, minHeight - 1], [0, minHeight - 1]])

    N = cv2.getPerspectiveTransform(rect, dst)

    warped = cv2.warpPerspective(img, N, (int(minWidth), int(minHeight)))

    cv2.imshow("asdff", warped)
    cv2.waitKey(0)


def order_point(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)

    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect


# src = cv2.imread('img/adffg.jpg')
# point('img/adfewr.jpg')
getImage("대한민국", 10)
