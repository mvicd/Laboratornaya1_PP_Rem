from datetime import time
from msilib.schema import Directory
import string
from random import random

import cv2
import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
from urllib.parse import urljoin, urlparse

directory_dataset = "D:\VS Code project\Images.py\dataset"
directory_rose = "D:\VS Code project\Images.py\dataset\rose"
directory_tulip = "D:\VS Code project\Images.py\dataset\tulip"


def directory():
    if not os.path.isdir("dataset"):
        os.mkdir(directory_dataset)
    if not os.path.isdir("rose"):
        os.mkdir(directory_rose)
    if not os.path.isdir("tulip"):
        os.mkdir(directory_tulip)


url = "https://yandex.ru/images/search?text=rose"


def valid(url):
    parse = urlparse(url)
    return bool(parse.scheme) and bool(parse.netloc)


name = string.ascii_lowercase
str = ''.join(random.sample(name, 15))
rand_user = {'User-Agent': str}

html_text = requests.get(url, headers=rand_user).text

soup = bs(html_text, 'html.parser')
img = soup.find_all('img', class_="serp-item__thumb justifier__thumb")

url_src = []

for i in img:
    url_src.append(i.get("src"))


def rose_load():
    directory()
    count = 1
    s = 0
    so = 1

    for i in range(1, 51):
        url = "https://yandex.ru/images/search?p=%d&text=rose&lr=51&rpt=image&uinfo=sw-1920-sh-1080-ww-1872-wh-932-pd-1-wp-16x9_1920x1080" % s

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

        for k in tqdm(url_src):
            url_absolut = "https:" + k
            r = requests.get(url_absolut).content
            fp = open(directory_rose + '/' + f"{so:05}" + '.jpg', "wb")
            fp.write(r)
            so += 1
            time.sleep(0.25)
            print(count, "/50")
            count += 1


rose_load()
