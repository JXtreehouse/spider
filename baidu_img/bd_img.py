#!/usr/bin/env python
"""
 Created by howie.hu at  17-10-12.
"""
import os
import uuid
import logging

from talonspider import Spider, Request
from talonspider.utils import get_random_user_agent
from pprint import pprint

headers = {
    "User-Agent": get_random_user_agent()
}

demo = "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&cl=2&lm=-1&ie=utf-8&oe=utf-8&word={word}&pn={pn}&rn={rn}"


class BaiduImgSpider(Spider):
    start_urls = []
    set_mul = True
    img_path = 'data/'
    headers = {
        "User-Agent": get_random_user_agent()
    }

    def start_request(self):
        for url in self.start_urls:
            yield Request(url=url,
                          request_config=getattr(self, 'request_config'),
                          headers=getattr(self, 'headers', None),
                          callback=self.parse, file_type="json")

    def parse(self, res):
        data = res.html['data']
        img_urls = []
        for each_data in data:
            if each_data.get('thumbURL'):
                img_urls.append(each_data.get('thumbURL'))
        for url in img_urls:
            yield Request(url, headers=self.headers, callback=self.save_img, file_type='bytes')

    def save_img(self, res):
        if not os.path.exists(self.img_path):
            os.makedirs(self.img_path)
        img_name = str(uuid.uuid1()) + "_" + res.url[-10:].replace('/', '-')
        with open(self.img_path + img_name, 'wb') as file:
            file.write(res.html)
            logging.info('Img downloaded successfully in {dir}'.format(dir=self.img_path + img_name))


if __name__ == '__main__':
    word = '刀剑乱舞表情包'
    pages = 3
    BaiduImgSpider.img_path = word + "/"
    BaiduImgSpider.start_urls = [demo.format(word=word, pn=30 * page, rn=30) for page in range(pages)]
    print(BaiduImgSpider.start_urls)
    BaiduImgSpider.start()
