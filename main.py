# coding:utf-8
import time
import os
import copy
import requests
from spider import Shouyihuo
from utils import baidu_trans,youdao_trans,get_db
from publisher import BloggerPublisher
import copy
def main():
    articles = Shouyihuo().get_once()[::-1]
    for i in articles:
        en_doc = copy.deepcopy(i)
        en_doc["title"] = baidu_trans(en_doc["title"]).title()
        for num,item in enumerate(i["article"]):
            if item["type"] == "text":
                en_doc["article"][num]["content"] = baidu_trans(item["content"])
            else:
                en_doc["article"][num]["content"] = copy.deepcopy(requests.get(item["content"]).content)
        BloggerPublisher(en_doc).publish()
        time.sleep(2*60)



if __name__ == "__main__":
    main()

