import time
import requests
from pyquery import PyQuery as pq
from fake_useragent import UserAgent


# 抓取每个链接的内容
def get_each_page():
    url = 'https://www.wuxiaworld.com/novel/dragon-prince-yuan/yz-chapter-'
    # 读取所有链接
    for i in range(1, 601):
        url_temp = url + str(i)
        ua = UserAgent()
        # 随机请求头
        headers_ran = {'user-agent': ua.random}
        html = requests.get(url_temp, headers=headers_ran)
        # 链接正常
        if html.status_code != 200:
            continue
        else:
            # 保存源文件
            file = open('CrawlerSourceTxtE/Chapter_' + str(i) + '_Org.txt', 'a', encoding='utf-8')
            doc = pq(html.text)
            # print(doc)
            # 获取标题
            title = doc('.caption.clearfix').find('h4').eq(0).text()
            file.write(title + '\n')
            # 获取每一段的内容
            info = doc('#chapter-content p').items()
            print(info)
            for par in info:
                content = par('span').text()
                print(content)
                file.write(content + '\n')
            file.write('\n')
            file.close()
            time.sleep(5)
        # 一章下载完毕
        print('Chapter ' + str(i) + ' has downloaded !')


if __name__ == '__main__':
    # 获取每一页的内容
    get_each_page()
