import os
import re
import threading
import urllib.request
from operator import index

import requests
from bs4 import BeautifulSoup

url = 'http://tp.wcctv.top/'
folderPath = "D:/柠檬下载/GlobalBeauty/"
proxies = {"http": "http://127.0.0.1:3585",
           "https": "http://127.0.0.1:3585", }
atlasCount = 0
picCount = 0


def ReadHome(homeUrl):
    response = requests.get(homeUrl, proxies=proxies)
    soup = BeautifulSoup(response.content, 'html.parser')
    curentPage = soup.find(attrs={'class': 'current'})
    print("当前页数:"+curentPage.a.string)

    items = soup.find_all(attrs={'class': 'item col-xs-6 col-sm-4 col-md-3'})
    print('共获取到%s个图集' % len(items))
    downThread = []

    for index, item in enumerate(items):
        th = threading.Thread(target=ReadPage, args=(
            item.img.get('alt'), item.div.a.get('href')))
        downThread.append(th)

    for i in downThread:
        i.start()
    for i in downThread:
        i.join()

    print('')
    nextPage = soup.find(attrs={'class': 'next'})
    if nextPage != None:
        ReadHome(nextPage.a.get('href'))


def ReadPage(title, pageUrl):
    global atlasCount, picCount

    savePath = folderPath+title+'/'
    if os.path.exists(savePath) == False:
        os.makedirs(savePath)

    atlasCount += 1

    response = requests.get(pageUrl, proxies=proxies)
    soup = BeautifulSoup(response.content, 'html.parser')
    allBeauty = soup.find_all(attrs={'class': 'post-item-img'})
    for index, item in enumerate(allBeauty):
        # 获取图片后缀
        result = re.findall('\.[^.\\/:*?"<>|\r\n]+$', item.get('src'))
        fileName = savePath+item.get('title')+result[0]

        img = requests.get(item.get('src'), proxies=proxies)
        fp = open(fileName, 'wb')
        fp.write(img.content)
        fp.close()

        picCount += 1

    print('{0:<60}\t{1}'.format(
        '图集:'+title+',', '共'+str(len(allBeauty))+'张'))


if __name__ == "__main__":

    if os.path.exists(folderPath) == False:
        os.makedirs(folderPath)

    ReadHome(url)

    print('美好图集:{0},美好图片:{1}'.format(atlasCount, picCount))

    print('世间美好止步于此')
