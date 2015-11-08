#python
#
#获取相册页面，分析获取分页的url
#根据抓取的url分别做处理：将url页面中的真实图片名称获取
#将上一步的名称替换到指定的图片地址格式中，开始下载图片
#
import re
import os
import urllib.request
import bs4
from bs4 import BeautifulSoup
def getSoup(str_doc):
    '''根据传入的html文本生成soup对象'''
    soup = BeautifulSoup(str_doc,from_encoding='gbk')
    return soup
def getHtml(url):
    '''根据url获取html文本'''
    html = urllib.request.urlopen(url).read()
    return html
def filterForFileName(string):
    #\/?*<>:"| can't be filename in windows
    # \n \r may be avoided
    #http:... is not useful
    string = string.strip()
    regex = r"http:.*"
    string = re.sub(regex, "", string) #因为看到有些描述还加了网址的东西影响文件名命名过滤掉了
    string = string.replace('\n','').replace('\r','')
    return fileNameFilter(string)
def fileNameFilter(string):
    #windows下命名的禁止字符
    string = string.replace('/','').replace('*','').replace('?','').replace('<','').replace('>','').replace('\\','').replace('|','').replace(':','').replace('"','')
    return string
def pullImage(img_unit_list,direct):
    '''img_unit img对象'''
    direct = filterForFileName(direct)
    os.mkdir(direct)#根据direct生成目录，还没加是否已存在目录的判断
    x=0#计数用
    #大图是.../photo/large/...
    #小图是.../phtoo/photo/...
    #主要是有些相册是没大图的
    #img_1_str = "http://img3.douban.com/view/photo/large/public/"
    img_1_str = "http://img3.douban.com/view/photo/photo/public/"
    img_3_str = ".jpg"
    for img_unit in img_unit_list:
        img_src = img_unit.img_src
        slash_index = img_src.rfind('/')
        point_index = img_src.rfind('.')
        img_name = img_src[slash_index+1:point_index]
        img_url = img_1_str + img_name + img_3_str
        img_file_name = filterForFileName(img_unit.img_name)
        #下面是抓取第一个参数imgurl的文件，并以第二个参数命名文件
        urllib.request.urlretrieve(img_url,direct+'/%s-'%x +img_file_name+'.jpg')
        x+=1
    print("总共%s张图片"%x)
   
class imgunit(object):
    #存图片的路径和描述 -- 临时想到的映射方式
    img_src=''
    img_name=''
    def __init__(self,imgObj,aObj):
        #print(imgObj['src'])
        self.img_src = imgObj['src']
        self.img_name = aObj['title']
       
#first_page_url = "http://www.douban.com/photos/album/85320662/?start=0"
#"http://www.douban.com/photos/album/85320662/"
#first_page_url = 'http://www.douban.com/photos/album/85320662/'
#替换下列链接即可：相册链接
first_page_url = 'http://www.douban.com/photos/album/41149992/?start=0'
album_html=getHtml(first_page_url)
album_soup = getSoup(album_html)
#分页的链接
album_pages_url = []
album_pages_url.append(first_page_url)
#用作目录名
directory = album_soup.find('title').get_text()
#获取paginator id的div内容获取所有的a标签的 href
if album_soup.find('div','paginator')!=None:
    albums_a = album_soup.find('div','paginator').find_all("a")
    for page_a in albums_a:
        album_pages_url.append(page_a['href'])
        #print(album_pages_url)
        #由于取的是翻页部分的代码，因此需要将由于后页多余的一页的元素给移除
    album_pages_url.pop()
#存储 图片相关数据
img_units = []
for page_url in album_pages_url:
    print(page_url)
    page_html = getHtml(page_url)
    page_soup = getSoup(page_html)
    img_wrap_divs = page_soup.find_all('div','photo_wrap')
    y=0
    for img_wrap_div in img_wrap_divs:
        y+=1
        #print(y)
        img_units.append(imgunit(img_wrap_div.find('img'),img_wrap_div.find('a')))
print(len(img_units))
pullImage(img_units, directory)
   
   

