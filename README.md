# crawler
## crawler.py
실행방법 :
```bash
python crawler "${url_name}"
```
url 이름에 &가 껴있으면 백그라운드 실행이 되어 ""로 감싸줘야한다.

## crawler.sh
파일 실행권한 추가 필요하다면.
```bash
~$ chmod 755 crawler.sh
```

## classify_img.sh
실행방법:
```bash
python classify_img.py
```
_config.json_ 파일에 설정된 값으로 크롤링한다.

config.json
```json
{
    "chrome": "C:/python_test/chromedriver/chromedriver.exe",
    "log"   : "log.json",
    "downloadSrc":"./test_img",
    "category":[
        {
            "folder":"vietnam",
            "key":"t",
            "name":"vietnam"
        },
        {
            "folder":"vietnam-neutral",
            "key":"r",
            "name":"vietnam-neutral"
        },
        {
            "folder":"vietnam-diff",
            "key":"w",
            "name":"vietnam-diff"
        }
    ],
    "errorKey":"e",
    "endKey":"q"
}
```
|key|value|
|---|---|
|chrome|크롬드라이버의 위치를 나타낸다. 
|log|log파일의 파일 명을 적어준다. 파일 경로는 crawler.py와 같다.|
|downloadSrc| 이미지가 다운로드 되는 경로를 나타낸다.|
|category| value로 배열을 갖는다. 배열의 각 요소는 folder, key, name 값을 가져야 한다.
|├ folder| 카테고리 별로 이미지를 분류할 수 있게 했다. 
|├ key | 키보드 입력 키이다. 해당 키로 이미지를 분류 할 수 있다.
|└ name | 분류된 이미지의 파일 명이다. 파일명은 0부터 차례로 늘어난다. 단 중간의 인덱스가 끊겼을 때를 확인 할 수 없다.
|errorKey| 권한 문제라던지 여러 문제의 경우 표시되는 이미지를 검은 화면으로 대체했다. 그 경우 해당 키를 누르면 pass 한다. 에러가 아니더라도 pass하고 싶다면 이용해도 된다.
|endKey| 프로그램을 종료한다.

## 판별기준
__YES__
* 상품 가격부분 또는 메타데이터(매장명, 주소, ...)가 있다.
* 글씨를 육안으로 식별이 가능하다.