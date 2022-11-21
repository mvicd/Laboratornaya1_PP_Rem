from msilib.schema import Directory
import string
import cv2
import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
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
