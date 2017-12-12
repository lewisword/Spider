import requests
from bs4 import BeautifulSoup
import os

def getHTMLContent(url):
    try :
        kv = {'user-agent':'Mozilla/5.0'}
        res = requests.get(url,headers= kv)
        res.encoding = res.apparent_encoding
        return res.content
    except:
        print('抓取失败')

#解析的主要任务就是将得到的content放入汤中
def HTMLParser(content):
    try:
        soup = BeautifulSoup(content,'html.parser')
        for item in soup.select('.content center a'):
            if len(item) > 0:
                tag = item.select('img')[0]
                print(tag['src'])
        return tag['src']
    except:
        print("解析失败")

def Downloader(downUrl):
    root = "D:/pict/"
    path = root + downUrl.split('/')[-1]
    try:
        downContent = getHTMLContent(downUrl)
        if not os.path.exists(root):
            os.mkdir(root)
        if not os.path.exists(path):
            with open(path,'wb+') as f:
                f.write(downContent)
    except:
        print('下载失败')



if __name__ == '__main__':
    start_url = 'http://www.ligui.org/ligui/820{}_{}.html'
    list = []
    for i in range(4,10):
        for j in range(2,21):
            url = start_url.format(i,j)
            content = getHTMLContent(url)
            downUrl = HTMLParser(content)
            Downloader(downUrl)
            print('开始下载第%s套图的第%s张' %(i,j))