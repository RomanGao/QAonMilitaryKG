#coding = utf-8
import os
from  urllib import request
from lxml import etree
import gzip
import pymongo
import datetime

class NewspaperSpider:
    def __init__(self):
        self.term_dict = {
            'aircraft': "飞行器",
            'warship': "舰船舰艇",
            'guns': "枪械与单兵",
            'tank': "坦克装甲车辆",
            'artillery': "火炮",
            'missile': "导弹武器",
            'spaceship': "太空装备",
            'explosive': "爆炸物",
                        }

        self.conn = pymongo.MongoClient()
        return

    '''get html '''
    def get_html(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'en-US,en;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Cookie':'Hm_lvt_1fc983b4c305d209e7e05d96e713939f=1552034977; Hm_lpvt_1fc983b4c305d209e7e05d96e713939f=1552036141',
            'Host':'weapon.huanqiu.com'
            }
        req = request.Request(url, headers=headers)
        page = request.urlopen(req).read()
        page = gzip.decompress(page).decode('utf-8')

        return page

    '''get_urllist'''
    def get_urllist(self, url):
        html = self.get_html(url)
        selector = etree.HTML(html)
        papers = ['http://weapon.huanqiu.com' + i for i in selector.xpath('//li/span[@class="pic"]/a/@href')]
        return list(set(papers))

    '''content parser'''
    def html_parser(self, url):
        html = self.get_html(url)
        selector = etree.HTML(html)
        title = selector.xpath('//title/text()')[0]
        attrs =selector.xpath('//div[@class="dataInfo"]/ul/li')
        contents = [html, title]
        for article in attrs:
            content = article.xpath('string(.)')
            contents.append(content)
        return contents

    '''modify data'''
    def modify_data(self):
        keys = []
        for item in self.conn['military']['kb'].find():
            body = item['contents']
            title = body[1].replace(' ','').replace('－','-').replace('（','(').replace('）',')')
            title = title.split('_')
            data = {}
            name = title[0]
            category = title[1]
            data['名称'] = name
            data['类别'] = category
            attrs = body[2:]
            html = body[0]
            selector = etree.HTML(html)
            country = selector.xpath('//span[@class="country"]/b/a/text()')[0]
            data['产国'] = country
            for attr in attrs:
                if len(attr.split('：')) < 2:
                    continue
                key = attr.split('：')[0].replace('（','(').replace(' ','').replace('\t','')
                if key.startswith('(') or len(key) > 6:
                    continue
                value = attr.split('：')[1]
                data[key] = value.replace('\t','').replace('\n','').replace(',','')
                keys.append(key)
            self.conn['military']['graph_data'].insert(data)
        return

    '''采集主函数'''
    def spider_main(self):
        big_cates = ['aircraft', 'warship',
                     'guns', 'tank',
                     'artillery', 'missile',
                     'spaceship', 'explosive'
                     ]
        for big_cate in big_cates:
            big_url = 'http://weapon.huanqiu.com/weaponlist/%s'%big_cate
            html = self.get_html(big_url)
            selector = etree.HTML(html)
            span = selector.xpath('//span[@class="list"]')[0]
            second_urls = ['http://weapon.huanqiu.com' + i for i in span.xpath('./a/@href')]
            second_cates = [i for i in span.xpath('./a/text()')]
            second_dict = {}
            for indx, second_cate in enumerate(second_cates):
                second_dict[second_cate] = second_urls[indx]
            for second_cate, second_url in second_dict.items():
                max_pages = self.get_maxpage(second_url)
                for page in range(1, max_pages+1):
                    url = second_url + '_0_0_%s'%page
                    seed_urls = self.get_urllist(url)
                    for seed in seed_urls:
                        self.get_info(seed, big_cate, second_cate)


    '''根据最大值，获取所有信息'''
    def get_info(self, url, big_cate, second_cate):
        content = self.html_parser(url)
        data = self.extract_data(content)
        data['大类'] = self.term_dict.get(big_cate)
        data['类型'] = second_cate
        if data:
            print(data)
            self.conn['military']['knowledge_base'].insert(data)
        return

    '''modify data'''
    def extract_data(self, content):
        title = content[1].replace(' ', '').replace('－', '-').replace('（', '(').replace('）', ')')
        title = title.split('_')
        data = {}
        name = title[0]
        data['名称'] = name
        attrs = content[2:]
        html = content[0]
        selector = etree.HTML(html)
        country = selector.xpath('//span[@class="country"]/b/a/text()')[0]
        image = selector.xpath('//div[@class="maxPic"]/img/@src')
        if not image:
            image = ''
        else:
            image = image[0]
        data['产国'] = country
        data['图片'] = image
        data['简介'] = ''.join(selector.xpath('//div[@class="module"]/p/text()')).replace('\xa0','').replace('\u3000', '').replace('\t', '')
        for attr in attrs:
            if len(attr.split('：')) < 2:
                continue
            key = attr.split('：')[0].replace('（', '(').replace(' ', '').replace('\t', '')
            if key.startswith('(') or len(key) > 6:
                continue
            value = attr.split('：')[1]
            data[key] = value.replace('\t', '').replace('\n', '').replace(',', '')
        return data

    '''获取最大值'''
    def get_maxpage(self, url):
        html = self.get_html(url)
        selector = etree.HTML(html)
        max_pages = selector.xpath('//div[@class="pages"]/a/text()')
        if not max_pages:
            max_page = 1
        else:
            max_page = int(max_pages[-2])

        return max_page


if __name__ == '__main__':
    handler = NewspaperSpider()
    handler.spider_main()