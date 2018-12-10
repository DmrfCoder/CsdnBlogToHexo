#!/usr/bin/env python2
# coding=utf-8
import random
from lxml import etree
# responsible for printing
import requests
import html2text

from bs4 import BeautifulSoup
import codecs


def request_get(url):
    UserAgent_List = [
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36",
    ]

    header = {
        'User-agent': random.choice(UserAgent_List),
        'Host': ' blog.csdn.net',
        'Accept-Language': ' en-US,en;q=0.9,zh-CN;q=0.8,zh;q = 0.7',
        'Referer': 'https://movie.douban.com/subject/24773958/?from=showing',
    }

    session = requests.Session()

    headers = {
        'User-Agent': 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
    # req = urllib2.Request(url, headers=headers)
    # html_doc = urllib2.urlopen(req).read()
    response = requests.get(url, headers=headers, timeout=3)
    return response


def CrawlingItemBlog(base_url, id):
    second_url = base_url + 'article/details/'
    url = second_url + id
    item_html = request_get(url)
    if item_html.status_code == 200:
        selector = etree.HTML(item_html.text, parser=etree.HTMLParser(encoding='utf-8'))
        '''
        需要的信息：
        1：标题
        2：markdown内容
        3：发表日期
        4：标签
        5：类别
        
        '''
        categories = ''
        str_tag = ''

        soup = BeautifulSoup(item_html.text)
        c = soup.find(id="content_views")
        m = html2text.html2text(c.prettify())

        title = soup.find(attrs={'class': 'title-article'})
        filename = title.get_text()
        title = title.prettify()

        str_title = 'title: ' + filename + '\n'
        label = ''

        # 有可能出现这篇文章没有label的情况
        try:
            label = soup.find(attrs={'class': 'tags-box space'}).find(attrs={'class': 'tag-link'}).get_text()
        except Exception:
            pass

        if label == '':
            pass
        else:
            label = label.replace('\t', '')
            categories = 'categories:\n' + '- ' + label + '\n'

        time = soup.find(attrs={'class': 'time'}).get_text()
        s_time1 = time.split('年')
        year = s_time1[0]
        s_time2 = s_time1[1].split('月')
        month = s_time2[0]
        s_time3 = s_time2[1].split('日')
        day = s_time3[0]
        minite = s_time3[1].strip()
        str_date = 'date: ' + year + '-' + month + '-' + day + ' ' + minite + '\n'

        tags = ''
        try:
            tags = soup.find(attrs={'class': 'tags-box artic-tag-box'}).get_text()
        except Exception:
            pass

        if tags == '':
            pass
        else:
            tags = tags.split('\n')
            tags = tags[2]

            tags = tags.replace('\t', ' ')
            tags = tags.split(' ')
            str_tag = 'tags:\n'
            for tag in tags:
                if tag == '':
                    continue
                else:
                    str_tag = str_tag + '- ' + tag + '\n'

        text_maker = html2text.HTML2Text()
        text_maker.bypass_tables = False

        text = text_maker.handle(c.prettify())
        #有的文章名字特殊，会新建文件失败
        try:
            f = codecs.open('./mds/' + filename + '.md', 'w', encoding='utf-8')
            hexo_str = '---\n' + str_title + str_date + categories + str_tag + '\n---\n'

            f.write(hexo_str)
            f.write(text)
            f.close()
        except Exception:
            print(filename)

        return True
    else:
        return False


def start_spider():
    base_url = 'https://blog.csdn.net/qq_36982160/'
    second_url = base_url + 'article/list/'
    start_url = second_url + '1'

    number = 1
    html = request_get(start_url)
    count = 0

    while html.status_code == 200:
        # 获取下一页的 url
        selector = etree.HTML(html.text)
        number += 1
        next_url = second_url + str(number)
        cur_page = selector.xpath('//*[@id="mainBox"]/main/div[2]')
        d = cur_page[0].xpath('//*[@id="mainBox"]/main/div[2]/div[2]/h4/a')
        l = cur_page[0].findall('data-articleid')

        for elem in cur_page[0]:
            item_content = elem.attrib
            if item_content.has_key('style'):
                continue
            else:
                if item_content.has_key('data-articleid'):
                    id = item_content['data-articleid']
                    count += 1
                    print(count)

                    CrawlingItemBlog(base_url, id)

        html = request_get(next_url)


if __name__ == "__main__":
    start_spider()
