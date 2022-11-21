import os
import random
import string
import time
from urllib.parse import urlparse
import cv2
import requests
from bs4 import BeautifulSoup as bs
import tqdm


def directory():
    if not os.path.isdir("rose"):
        os.makedirs(directory_rose)
    if not os.path.isdir("tulip"):
        os.makedirs(directory_tulip)


url = "https://yandex.ru/images/search?text=rose"


def valid(url):
    parse = urlparse(url)
    return bool(parse.scheme) and bool(parse.netloc)


def load_img(url_obj, directory_obj):
    try:
        if not valid(url_obj):
            raise TypeError
    except TypeError:
        print("URL is not valid")

    directory()
    count = 1
    s = 0
    so = 1

    for i in range(1, 41):
        url = url_obj % s
        print(url)
        s += 1

        name = string.ascii_lowercase
        str1 = ''.join(random.sample(name, 15))
        rand_user = {'User-Agent': str1}

        html_text = requests.get(url, headers=rand_user).text
        soup = bs(html_text, 'html.parser')
        img = soup.find_all('img', class_="serp-item__thumb justifier__thumb")

        url_src = []

        for j in img:
            url_src.append(j.get("src"))

        for k in tqdm.tqdm((url_src)):
            url_absolut = "https:" + k
            r = requests.get(url_absolut).content
            fp = open(directory_obj + '\\' + f"{so:04}" + '.jpg', "wb")
            fp.write(r)
            so += 1
            time.sleep(0.25)
        print(count, "/40")
        count += 1


def calc_image_hash(filename):
    image = cv2.imread(filename)  # Прочитаем картинку
    resized = cv2.resize(image, (12, 12), interpolation=cv2.INTER_AREA)  # Уменьшим картинку
    gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)  # Переведем в черно-белый формат
    avg = gray_image.mean()  # Среднее значение пикселя
    ret, threshold_image = cv2.threshold(gray_image, avg, 255, 0)  # Бинаризация по порогу

    _hash = ""
    for x in range(12):
        for y in range(12):
            val = threshold_image[x, y]
            if val == 255:
                _hash = _hash + "1"
            else:
                _hash = _hash + "0"

    return _hash


def comparison(directory):
    list_hash = []
    for i in range(1, 1201):
        img = directory + '/' + f"{i:04}" + '.jpg'
        hash = calc_image_hash(img)
        list_hash.append(hash)

    print(len(list_hash))
    equal = []
    for i in range(0, 1200):
        for j in range(i + 1, 1200):
            if list_hash[i] == list_hash[j]:
                equal.append(j + 1)
    print(equal)
    equal = list(set(equal))
    equal.sort()
    print(equal)

    count = 0
    for i in equal:
        del_img = directory + '/' + f"{i:04}" + '.jpg'
        os.remove(del_img)

    x = 1200
    j = 0
    count = 0
    list_last = []
    while (j < len(equal)):
        if os.path.isfile(directory + '/' + f"{x - count:04}" + '.jpg'):
            list_last.append(x)
            x -= 1
            j += 1
        else:
            x -= 1
    print(list_last)

    equal_1 = []
    for y in equal:
        if y < list_last[0]:
            equal_1.append(y)

    for y in range(0, len(equal_1)):
        img_1 = directory + '/' + f"{equal_1[y]:04}" + '.jpg'
        img_2 = directory + '/' + f"{list_last[y]:04}" + '.jpg'
        os.rename(img_2, img_1)


directory_rose = "D:\VS Code project\Images.py\dataset\ rose"
directory_tulip = "D:\VS Code project\Images.py\dataset\ tulip"


url = "https://yandex.ru/images/search?p=%d&text=rose&lr=51&rpt=image&uinfo=sw-1920-sh-1080-ww-1872-wh-932-pd-1-wp-16x9_1920x1080"
load_img(url, directory_rose)
comparison(directory_rose)


url = "https://yandex.ru/images/search?p=%d&text=tulip&from=tabbar&uinfo=sw-1920-sh-1080-ww-1872-wh-932-pd-1-wp-16x9_1920x1080&lr=101134&rpt=image"
load_img(url, directory_tulip)
comparison(directory_tulip)
