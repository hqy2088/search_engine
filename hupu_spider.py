import time
import requests
from pyquery import PyQuery as pq
from fake_useragent import UserAgent

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.51", }

# 获取步行街前6页链接（约600多个）
def get_link():
    # 步行街主干道链接
    # f = open('url.txt', 'w+', encoding='utf-8')
    url = 'https://bbs.hupu.com/bxj-'
    # 获取1-6页的链接
    for i in range(1, 7):
        url_temp = url + str(i)
        html = requests.get(url_temp, headers=headers)
        doc = pq(html.text)
        # print(doc)
        # class属性为for-list的ul标签 下面的li标签
        # 因为要分别取出每个li标签的内容，所以要加上items方法方便遍历
        info = doc('ul.for-list li').items()
        # print(info)
        # 对每个li标签，提取它嵌套的class属性为truetit的a标签的内容
        # 获取文本用text方法
        for j in info:
            # 获取文章题目
            title = j('a.truetit').text()
            # 获取作者名字
            author = j('a.aulink').text()
            # 获取帖子链接
            post_link = j('a.truetit').attr('href')
            link = 'https://bbs.hupu.com' + post_link
            print('标题：' + title + '  作者：' + author + '  链接：' + link)
            #f.write(link + '\n')
        print('步行街第' + str(i) + '页链接获取完成\n')
        # time.sleep(1)
    #f.close()


# 抓取每个链接的内容
def get_each_page():
    f = open('url.txt', 'r', encoding='utf-8')
    # 读取所有链接
    url_list = f.readlines()
    f.close()
    for i in range(0, len(url_list)):
        # 去除链接后的回车符
        url_temp = url_list[i].strip('\n')
        # print(url_temp)
        # 随机请求头
        ua = UserAgent()
        headers_ran={'user-agent': ua.random}
        html = requests.get(url_temp, headers=headers_ran)
        # 链接正常
        if html.status_code != 200:
            continue
        else:
            doc = pq(html.text)
            info = doc.find('.bbs-hd-h1 h1')
            # 标题
            title = '标题：' + info.attr('data-title')
            # 板块
            fidname = '板块：' + info.attr('fidname')
            # 作者
            author_pos = doc('.post-owner').parent()
            author = '作者：' + author_pos('.u').eq(0).text()
            content = '内容：' + doc('.quote-content p').text()
            print(title+' '+author+' '+fidname+' '+content)
            file = open('CrawlerSourceTxtC/BBS_' + str(i + 1) + '_Org.txt', 'a', encoding='utf-8')
            file.write('\n'.join([title, author, fidname, content]))
            file.write('\n')
            print('BBS ' + str(i + 1) + ' has downloaded !')
            file.close()
            time.sleep(2)


if __name__ == '__main__':
    # 获取页面链接
    get_link()
    # 获取每一页的内容
    #get_each_page()
