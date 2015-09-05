#!/usr/bin/env python
# -*- coding: utf-8 -*-


from HTMLParser import HTMLParser
import urllib
import sys


#定义HTML解析器
class Parselinks(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.data = []
        self.href_flag = 0  #遇到开始a标签的href就标记为1,关闭a标签时候就为0
        self.link_content = ''
        self.urls = []

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            for name, value in attrs:
                if name == 'src':
                    print value
                    self.getImage("http:" + value)

        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    self.urls.append(value)#把html中的所有连接（<a>标签）中的地址（href属性的值）提取出来，放到一个list里面
                    self.href_flag = 1

    def handle_data(self, data):#这里的data为上面tag标签包含的内容
        if self.href_flag:
            self.link_content += data

    # def handle_entityref(self, name):
    #     if name == "&nbsp":
    #         pass

    def handle_endtag(self, tag):
        if tag == 'a':
            self.link_content = ''.join(self.link_content.split()) #join连接字符串,split拆分字符串
            self.link_content = self.link_content.strip() #默认删除开头,结尾处的空白符（包括'\n', '\r',  '\t',  ' ')
            if self.link_content:
                self.data.append(self.link_content)
            self.link_content = ''
            self.href_flag = 0

    def getresult(self):
        print len(self.urls)
        for url in self.urls:
            print url

        print len(self.data)
        for value in self.data:
            print value

    def getImage(self, addr):
        u = urllib.urlopen(addr)
        data = u.read()
        split_path = addr.split("/")
        print split_path
        # print type(split_path) # list
        file_name = split_path.pop()
        f = open(file_name, "wb")
        f.write(data)
        f.close()


if __name__ == "__main__":
    myParser = Parselinks()
    myParser.feed(urllib.urlopen("http://www.sina.com.cn").read())#需要注意，如果传给HTMLParser的feed()函数的数据不完整的话，
                                                                # 那么不完整的标签会保存下来，并在下一次调用feed()函数时进行解析。
                                                                # 当HTML文件很大，需要分段发送给解析器的时候，这个功能就会 有用武之地了
    # myParser.decode('gbk').encode('utf8')
    # myParser.getresult()
    myParser.close()

