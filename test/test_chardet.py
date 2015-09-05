#coding:utf-8
#this way is not good.
import chardet
import urllib2

html = urllib2.urlopen("http://www.sina.com.hk").read()  #{'confidence': 0.99, 'encoding': 'utf-8'}j
#html = urllib2.urlopen("http://www.sina.com.cn").read() #not OK
charset = chardet.detect(html)
print charset

encode = charset['encoding']
if encode == 'utf-8' or encode == 'UTF-8':
    html = html.decode('utf-8', 'ignore').encode('utf-8')
    print html# 正常显示,繁体字也正常
else:
    html = html.decode('gb2312', 'ignore').encode('utf-8')
    print html