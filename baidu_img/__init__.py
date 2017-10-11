#!/usr/bin/env python
"""
 Created by howie.hu at  17-10-11.
"""
from urllib.parse import urljoin
from talonspider import Spider, Item, TextField, AttrField, Request
from talonspider.utils import get_random_user_agent


class BaiduImgItem(Item):
    """
    定义继承自item的Item类
    """
    pass


class BaiduImgSpider(Spider):
    start_urls = ['https://tieba.baidu.com/p/5276894332']

    def parse(self, res):
        # 将html转化为etree
        etree = self.e_html(res.html)
        # 提取目标值生成新的url
        # 提取目标值生成新的url
        pages = list(set(i.get('href') for i in etree.cssselect('li.pb_list_pager>a')))
        headers = {
            "User-Agent": get_random_user_agent()
        }
        pages.append(self.start_urls[0])
        if pages:
            for page in pages:
                url = urljoin(self.start_urls[0], page)
                yield Request(url, headers=headers, callback=self.parse_item)
        else:
            self.parse(res)

    def parse_item(self, res):
        # items_data = BaiduImgItem.get_items(html=res.html)
        pass


if __name__ == '__main__':
    BaiduImgSpider.start()
