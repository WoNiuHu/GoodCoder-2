#coding:utf-8
#this way is good.
# http://www.sina.com.cn的网页能显示出来了. 解决了中文乱码

import gzip
import StringIO
import urllib2
import bs4  #抓取网页中的中文乱码
import re


class Queue(object):
    def __init__(self, tmp_list=[]):
        self.queue = tmp_list

    #入队
    def push(self, v):
        self.queue.append(v)
        print "enqueue:", v

    #出队
    def pop(self):
        return self.queue.pop(0) #pop method returns the removed object from the list.

    def is_empty(self):
        return len(self.queue) == 0

    def get_length(self):
        return len(self.queue)

    def is_exist(self, url):
        if url in self.queue:
            return True
        else:
            return False


class LinkQueue(object):
    def __init__(self, tmp_list=[]):
        self.visited = Queue()
        self.unvisited = Queue(tmp_list)

    def get_visited_url(self):
        return self.visited

    def get_unvisited_url(self):
        return self.unvisited

    #添加到访问过的url队列中
    def add_visited_url(self, url):
        self.visited.push(url)

    #为什么要删除访问过的url呢??
    def remove_visited_url(self, url):
        self.visited.remove(url)

    def add_unvisited_url(self, url):
        #添加到未访问队列,确保每个url只能被访问一次
        if url != " " and not self.visited.is_exist(url) and not self.unvisited.is_exist(url):
            # self.unvisited.insert(0, url)
            self.unvisited.push(url)

    def get_visited_url_length(self):
        return self.visited.get_length()

    def get_unvisited_url_length(self):
        return self.unvisited.get_length()

    def is_unvisited_url_empty(self):
        if self.unvisited.is_empty():
            return True
        else:
            return False


def get_page_source(url):
    # url = "http://www.sina.com.cn"
    # url = "http://www.baidu.com"  #not a gizpped file~
    headers = {'Use-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)

    try:
        data = response.read()
        data = StringIO.StringIO(data)
        #其实，现在很多网页为了提高浏览器端用户的访问速度，和搜索引擎爬虫抓取的速度，都在使用gzip压缩。
        gzip_file = gzip.GzipFile(fileobj=data)
        html = gzip_file.read()
        #fromEncoding 原网页的编码，当然也可以写一个自动获取网页编码传进来更好
        page = bs4.BeautifulSoup(html, from_encoding='gbk')
        print type(page) #<class 'bs4.BeautifulSoup'>
        #折打tag,里面是排好的网页源代码
        # print page
    except Exception, e:
        print e
        # request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)
        page = response.read()
        # print page

    return ["OK", page]


def get_hyperlinks(url):
    data = get_page_source(url)
    if data[0] == "OK":
        # print type(data[1])
        # print data[1]
        soup = bs4.BeautifulSoup(str(data[1]))
        urls = []
        for link in soup.find_all('a'):
            # print link
            try:
                if str(link.get('href')).find("http://") != -1:
                    urls.append(link.get('href'))
                    # print link.get('href')
            except Exception, err:
                print type(err),
                print err #'ascii' codec can't encode characters in position 33-34: ordinal not in range(128)

        print "超链接长度: ", len(urls)
        return urls

if __name__ == "__main__":
    seeds = ["http://www.baidu.com", "http://www.sina.com.cn"]
    # get_page_source(urls[0])

    #用种子初始化unvisited队列
    link_queue = LinkQueue(seeds)
    for seed in seeds:
        urls = get_hyperlinks(seed)
        for url in urls:
            link_queue.add_unvisited_url(url)

        print "till now", link_queue.get_unvisited_url_length()


