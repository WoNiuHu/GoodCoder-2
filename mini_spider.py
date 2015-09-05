#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import ConfigParser
import os
import re
import bs4
import time
import gzip
import StringIO

import log


class WebSpider(object):

    def __init__(self, url):
        self.url = url
        self.protocol = ''

    def get_html(self):
        if self.url is None or self.url == " ":
            return

        try:
            html = self.handle_gzip_file()
            print "gzipped file~"
        except:
            html = self.handle_utf8_page()
            print "not gzipped file~"

        # print html 
        return html

    def handle_utf8_page(self):
        #url = 'http://www.baidu.com'
        #有的网站禁止爬虫，不能抓取或者抓取一定数量后封ip, 解决：伪装成浏览器进行抓取，加入headers
        headers = {'Use-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        request = urllib2.Request(self.url, headers=headers)
        response = urllib2.urlopen(request)#打开url并返回类文件对象
        html = response.read()
        print "utf-8 page http_status:", response.getcode()
        print "实际的url:", response.geturl() #返回所返回的数据的实际url,但会考虑发生的重定向问题
        self.protocol = response.geturl().split(':')[0]
        return html

    def is_https(self):
        if self.protocol == 'https':
            return True
        else:
            return False

    def handle_gzip_file(self):
        headers = {'Use-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)
        print "gzip_file http_status: ", response.getcode()
        print "实际url:", response.geturl()
        self.protocol = response.geturl().split(':')[0]

        data = response.read()
        data = StringIO.StringIO(data)

        #现在很多网页为了提高浏览器端用户的访问速度，和搜索引擎爬虫抓取的速度，都在使用gzip压缩。
        gzip_file = gzip.GzipFile(fileobj=data)
        html = gzip_file.read()
        #fromEncoding 原网页的编码，当然也可以写一个自动获取网页编码传进来更好
        html = bs4.BeautifulSoup(html, from_encoding='GB18030') #gbk is also OK
        # print "内容是:", html
        # print "str(html)内容是:", str(html)
        print "gzipped page type is:", type(html)#<class 'bs4.BeautifulSoup'>
        return html

    #根据正则获取图片的url列表
    def get_img_list(self, html):
        # reg = config.get("spider", "target_url")
        # print reg, type(reg)
        # img_pattern = re.compile(r'".*\.(gif|png|jpg|bmp)"', re.I)
        #正则匹配默认是贪婪匹配,就是说匹配尽可能多的字符. ?: 表示无捕获组
        # img_pattern = re.compile(r'"((http://|https://|)[\w\.\-/]*?([\w\-]*\.(gif|png|jpg|bmp)))"', re.I | re.M) #将正则表达式的字符串形式编译为Pattern实例
        img_pattern = re.compile(r'"((http://|https://|)[\w\.\-/]*?([\w\-]*\.(gif|png|jpg|bmp)))"', re.I | re.M) #将正则表达式的字符串形式编译为Pattern实例
        print img_pattern
        print type(img_pattern) #str
        img_list = re.findall(img_pattern, html)
        print len(img_list)
        for img_tuple in img_list:
            print img_tuple

        # print img_list
        return img_list

    #获取图片
    def download_img(self, img_list):
        for img_url in img_list:
            if not img_url[1]:
                img_url = "http:" + img_url[0]
            else:
                img_url = img_url[0]
            print "图片链接: ", img_url
            file_name = img_url.split("/")[-1]
            output_dir = config.get("spider", "output_directory")
            output_path = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), output_dir, p))
            #新建目录存放爬取的图片
            child_dir = self.url.split('.')[1]
            output_sec_dir = output_path(child_dir) #/Users/will/Android/Python/good_coder/output/baidu
            print output_sec_dir
            if not os.path.exists(output_sec_dir):
                os.mkdir(output_sec_dir)
                print "新建文件夹~"

            if not os.path.exists(os.path.abspath(os.path.join(output_sec_dir, file_name))):
                #下载文件
                urllib.urlretrieve(img_url, os.path.abspath(os.path.join(output_sec_dir, file_name)))
            else:
                print file_name + " 已经存在了~"
            CRAWL_INTERVAL = config.get("spider", "crawl_interval")
            time.sleep(float(CRAWL_INTERVAL))


if __name__ == "__main__":
    CONFIGFILE = "spider.conf"
    config = ConfigParser.ConfigParser()
    config.read(CONFIGFILE)

    # o = config.options("spider")
    # print o
    # v = config.items("spider")
    # print type(v) #list
    # print "spider:", v
    # print type(v[0])  #tuple
    # print v[0][0], v[0][1]
    #获得种子文件内容
    seed_file_dir = config.get("spider", "url_list_file") #读取指定section 的option 信息
    # print seed_file_dir
    seed_path = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), seed_file_dir, p))
    seed_file = seed_path("url_list_file")
    # seed_file = os.path.abspath(os.path.join(os.path.dirname(__file__), seed_file_dir, "url_list_file"))
    print "种子文件: ", seed_file #/Users/will/Android/Python/good_coder/urls/url_list_file
    urls = open(seed_file, "r")
    url_arr = []
    for url in urls: #推荐读取方法，使用文件迭代器 , 每次只读取和显示一行，读取大文件时应该这样
        # print url
        url_arr.append(url)

    # log.init_log("./log/mini_spider")
    # logging.info("Start~")
    print url_arr[1]
    web_spider = WebSpider(url_arr[1])
    # html = web_spider.get_html()

    #如果为https请求就再请求一次
    count = 1
    while True:
        html = web_spider.get_html()
        print "till now, total request times:", count, "times"

        if not web_spider.is_https():
            break
        count += 1
    img_list = web_spider.get_img_list(str(html))
    web_spider.download_img(img_list)


