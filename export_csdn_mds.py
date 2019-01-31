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
    session = requests.Session()

    headers = {
        'User-Agent': 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
    response = requests.get(url, headers=headers, timeout=3)
    return response


def CrawlingItemBlog(base_url, id):
    second_url = base_url + 'article/details/'
    url = second_url + id
    # 发送request请求并接受返回值
    item_html = request_get(url)
    if item_html.status_code == 200:
        '''
        需要的信息：
        1：标题
        2：markdown内容
        3：发表日期
        4：标签
        5：类别
        
        '''

        # 利用BeautifulSoup解析返回的html
        soup = BeautifulSoup(item_html.text)
        c = soup.find(id="content_views")

        # 标题
        title_article = soup.find(attrs={'class': 'title-article'})
        # 这里是将标题作为最后存储的文件名
        file_name = title_article.get_text()
        title_article = title_article.prettify()

        # 设置hexo格式博客开头的格式（title）
        hexo_title = 'title: ' + file_name + '\n'

        # 文章的categories
        hexo_categories = ''

        # 有可能出现这篇文章没有categories的情况
        try:
            hexo_categories = soup.find(attrs={'class': 'tags-box space'}).find(attrs={'class': 'tag-link'}).get_text()
        except Exception:
            pass

        if hexo_categories == '':
            pass
        else:
            # 去除拿到的str中的'\t'
            hexo_categories = hexo_categories.replace('\t', '')
            hexo_categories = 'categories:\n' + '- ' + hexo_categories + '\n'

        # 发表时间
        time = soup.find(attrs={'class': 'time'}).get_text()
        s_time1 = time.split('年')
        year = s_time1[0]
        s_time2 = s_time1[1].split('月')
        month = s_time2[0]
        s_time3 = s_time2[1].split('日')
        day = s_time3[0]
        minite = s_time3[1].strip()

        hexo_date = 'date: ' + year + '-' + month + '-' + day + ' ' + minite + '\n'

        hexo_tags = ''

        # 获取tags
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
            hexo_tags = 'tags:\n'
            for tag in tags:
                if tag == '':
                    continue
                else:
                    hexo_tags = hexo_tags + '- ' + tag + '\n'

        # 将html转化为markdown
        text_maker = html2text.HTML2Text()
        text_maker.bypass_tables = False

        text = text_maker.handle(c.prettify())
        # 有的文章名字特殊，会新建文件失败
        try:
            # 写入文件
            f = codecs.open('./mds/' + file_name + '.md', 'w', encoding='utf-8')
            hexo_str = '---\n' + hexo_title + hexo_date + hexo_categories + hexo_tags + '\n---\n'

            f.write(hexo_str)
            f.write(text)
            f.close()
        except Exception:
            print(file_name)

        return True
    else:
        return False


def start_spider(username):
    # 把下面这个base_url换成你csdn的地址
    base_url = 'https://blog.csdn.net/' + username + '/'
    second_url = base_url + 'article/list/'
    # 从第一页开始爬取
    start_url = second_url + '1'

    number = 1
    count = 0

    # 开始爬取第一个article_list，返回信息在html中
    html = request_get(start_url)

    # 这个循环是对你博客的article_list页面的循环
    while html.status_code == 200:
        # 获取下一页的 url
        selector = etree.HTML(html.text)

        # cur_article_list_page[0]就是当前article_list页面中的文章的list
        cur_article_list_page = selector.xpath('//*[@id="mainBox"]/main/div[2]')
        d = cur_article_list_page[0].xpath('//*[@id="mainBox"]/main/div[2]/div[2]/h4/a')
        l = cur_article_list_page[0].findall('data-articleid')

        # 这个循环是对你每一个article_list中的那些文章的循环
        for elem in cur_article_list_page[0]:
            item_content = elem.attrib
            # 通过对比拿到的数据和网页中的有效数据发现返回每一个article_list中的list都有一两个多余元素，每个多余元素都有style属性，利用这一特点进行过滤
            if item_content.has_key('style'):
                continue
            else:
                if item_content.has_key('data-articleid'):
                    # 拿到文章对应的articleid
                    articleid = item_content['data-articleid']
                    # 用于打印进度
                    count += 1
                    print(count)
                    # 爬取单篇文章
                    CrawlingItemBlog(base_url, articleid)

        # 进行下一article_list的爬取
        number += 1
        next_url = second_url + str(number)
        html = request_get(next_url)


if __name__ == "__main__":
    username = 'qq_36982160'
    start_spider(username)
