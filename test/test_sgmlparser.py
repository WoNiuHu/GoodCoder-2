#coding:utf-8

import urllib2
from sgmllib import SGMLParser

class ListName(SGMLParser):

	def __init__(self):
		SGMLParser.__init__(self)
		self.is_h4 = ""
		self.name = []

	def start_h4(self, attrs):
		self.is_h4 = 1

	def end_h4(self):
		self.is_h4 = ""

	def handle_data(self, text):
		if self.is_h4 == 1:
			self.name.append(text)

content = urllib2.urlopen('http://list.taobao.com/browse/cat-0.htm').read()
listname = ListName()
listname.feed(content)
for item in listname.name:
    # print item #中文乱码
	print item.decode('gbk').encode('utf8') #如果有乱码，可能是与网页编码不一致，需要替换最后一句 deconde() 的参数