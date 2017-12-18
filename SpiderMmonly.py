
import requests
from bs4 import BeautifulSoup
import os

def getHTMLContent(url):#函数的主要功能就是抓取页面的内容，返回r.content
    try:
        kv = {'user-agent': 'Mozilla/5.0'}
        r = requests.get(url, headers = kv)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.content
    except:
        print('抓取失败')

def parsePage(list,html):#爬取整个网页（第一页）所有套图的链接
    try:
        soup = BeautifulSoup(html,'html.parser',from_encoding='gb18030')
        for links in soup.select('.title span'):
            url = links.select('a')[0]['href']
            list.append(url)
            # title = links.string
            # print(dirname)
        return list


    except:
        print("解析失败")

def downPict(path,url):
    try:
        with open(path, 'wb') as f:
            f.write(getHTMLContent(url))
    except:
        print('下载失败')

#解析具体一份套图的网页地址
def parserUrl(url):
    try:
        pattern_url = url.split('.ht')[0] + '_{}.html'#得到的是具体套图网页的通用网址
        #通过解析具体套图的第一张网页得到该套图的名称和总数
        content = getHTMLContent(url)
        soup = BeautifulSoup(content,'html.parser',from_encoding='gb18030')
        title = soup.select('.imgtitle h1')[0].text
        pictname = title.split('(')[0]#得到套图的名称
        picttotle = title.split('/')[-1].rstrip(')')#得到套图的总量
        first_url = soup.select('#big-pic img')[0]['src']#得到第一张图片的下载链接

        #创建下载路径
        root = 'D:/pict/'
        if not os.path.exists(root):
            os.mkdir(root)
        dirname = '【{}P】{}'.format(picttotle, pictname)
        path = root + dirname
        if not os.path.exists(path):
            os.mkdir(path)

        #创建完整下载名称(包含.jpg),并下载第一张图片
        first_filename = path + '/1.jpg'
        downPict(first_filename, first_url)
        print('正在下载%s套图的第1张图片' % dirname)

        #通过通用网址解析出同一套图每张图片所在的网址，并下载每张图片
        for i in range(2,int(picttotle)+1):
            post_url = pattern_url.format(i)
            bigsoup = BeautifulSoup(getHTMLContent(post_url), 'html.parser', from_encoding='gb18030')
            down_url = bigsoup.select('#big-pic img')[0]['src']
            filename = path + '/%s.jpg' %i
            downPict(filename,down_url)
            print('正在下载%s套图的第%s张图片' %(dirname,i))
        print('')

    except:
        print('获取真实下载地址失败')



if __name__ == '__main__':

    start_url = 'http://www.mmonly.cc/ktmh/dmmn/'
    infoList = []
    content = getHTMLContent(start_url)
    infoList = parsePage(infoList,content)
    for purl in infoList:
        parserUrl(purl)



