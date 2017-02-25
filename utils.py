# coding:utf-8

import json
import hashlib
import urllib
import random
import requests
from config import BAIDU_FANYI
from config import YOUDAO_FANYI


def baidu_transe(text):
    appid = BAIDU_FANYI.get("appid")
    secretKey = BAIDU_FANYI.get("key")
    fromLang = 'auto'
    toLang = 'en'
    api_url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    salt = random.randint(32768, 65536)
    sign = appid + text + str(salt) + secretKey
    m2 = hashlib.md5()
    m2.update(sign)
    sign = m2.hexdigest()
    url = api_url + '?appid=' + appid + '&q=' + urllib.quote(text) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign
    result = None
    try:
        resp = requests.get(url)
        result = json.loads(resp.content).get("trans_result")
        if result and len(result) > 0:
            result = result[0].get("dst")
    except Exception, e:
        print e
    finally:
        if resp:resp.close()
        return result


def youdao_transe(text):
    key  = YOUDAO_FANYI.get("apikey","")
    keyfrom = YOUDAO_FANYI.get("keyfrom","")
    api_url = "http://fanyi.youdao.com/openapi.do?keyfrom={keyfrom}&key={key}&type=data&doctype=json&version=1.1&q={text}"
    text = urllib.quote(text)
    url = api_url.format(key=key,keyfrom=keyfrom,text=text)
    result = None
    try:
        resp = requests.get(url)
        result = json.loads(resp.content)

    except Exception, e:
        print e
    finally:
        if resp:resp.close()
        return result



if __name__ == "__main__":
    print youdao_transe("我是中国人，我爱中国")