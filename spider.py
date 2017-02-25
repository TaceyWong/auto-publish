# coding:utf-8

import re
import requests

class SpiderBase(object):

    HEADERS = {
        "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36"
    }

    def __init__(self):
        pass

    def get_html(self,url):
        content = None
        count = 0
        while True and count < 3:
            try:
                resp = requests.get(url,headers=self.HEADERS,timeout=20)
                content = resp.content
                break
            except Exception as e:
                count += 1
                print e
        return content

    def get_list(self,url=None):
        pass

    def get_detail(self,url):
        pass

    def build_doc(self):
        pass

class Shouyihuo(SpiderBase):
    list_url = "http://www.shouyihuo.com/creative/"

    list_re = re.compile(r'<a href="(.*?)" title="(.*?)" target="_blank"><img src="(.*?)" alt="(.*?)"/>')
    article_re = re.compile(r'<article class="article-content">(.*?)</article>',re.S)
    item_re = re.compile(r'<p(.*?)</p>',re.S)
    image_re = re.compile(r'src="(.*?)" />',re.S)
    def get_list(self,url=None):
        content = self.get_html(self.list_url)
        article_list = []
        for num ,item in enumerate(self.list_re.findall(content)):
            # print item
            article_list.append([i for i in item[:3] ])
        return article_list
    def get_detail(self,url=None):
        content = self.get_html(url)
        article = []
        article_content = self.article_re.findall(content)
        if article_content == []:return list()
        for num,item in enumerate(self.item_re.findall(article_content[0])):
            if "img alt" in item:
                a_item = {
                    "type":"img",
                    "content":self.image_re.findall(item)[0]
                }
            else:
                a_item = {
                    "type":"text",
                    "content":item[item.index(">")+1:]
                }
            article.append(a_item)
        return article
    def get_once(self):
        article_list = self.get_list()
        result = []
        for i in article_list:
            article = self.get_detail(i[0])
            item = {
                "ori_url":i[0],
                "title":i[1].replace(" ",":").replace(" ",":"),
                "top_pic":i[2],
                "article":article
            }
            result.append(item)
        return result


if __name__ == "__main__":
    result = Shouyihuo().get_once()
    for num ,i in enumerate(result):
        print num,i