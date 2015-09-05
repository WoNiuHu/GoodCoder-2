#coding:utf-8
#this way is good.
# http://www.sina.com.cn的网页能显示出来了.

import gzip
import StringIO
import urllib2
import bs4  #抓取网页中的中文乱码

# url = "http://www.sina.com.cn"
url = "http://www.baidu.com"
headers = {'Use-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}

request = urllib2.Request(url, headers=headers)
response = urllib2.urlopen(request)
data = response.read()
data = StringIO.StringIO(data)

#其实，现在很多网页为了提高浏览器端用户的访问速度，和搜索引擎爬虫抓取的速度，都在使用gzip压缩。
gzip_file = gzip.GzipFile(fileobj=data)
try:
    html = gzip_file.read()
    #fromEncoding 原网页的编码，当然也可以写一个自动获取网页编码传进来更好
    page = bs4.BeautifulSoup(html, from_encoding='gbk')
except Exception, e:
    print "有异常:", e



print type(page) #<class 'bs4.BeautifulSoup'>
#折打tag,里面是排好的网页源代码
print page