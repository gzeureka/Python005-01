#!/usr/bin/env python
# 使用 requests 库抓取知乎任意一个话题下排名前 15 条的答案内容(如果对前端熟悉请抓取所有答案)，并将内容保存到本地的一个文件

import requests
from lxml import etree
import sys


def get_page(url):
    print(f'Getting "{url}"')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    selector = etree.HTML(response.text)

    # //*[@id="QuestionAnswers-answers"]/div/div/div/div[2]/div/div[15]
    # //*[@id="QuestionAnswers-answers"]/div/div/div/div[2]/div/div[1]/div/div[2]/div[1]/span
    #QuestionAnswers-answers > div > div > div > div:nth-child(2) > div > div:nth-child(2) > div > div.RichContent.RichContent--unescapable > div.RichContent-inner > span
    # //*[@id="QuestionAnswers-answers"]/div/div/div/div[2]/div
    list = selector.xpath(
        '//*[@id="QuestionAnswers-answers"]/div/div/div/div[2]/div/div')
    print(list)


if __name__ == '__main__':
    # 检查命令行参数个数
    if len(sys.argv) < 2:
        url = 'https://www.zhihu.com/question/20484909'
    else:
        url = sys.argv[1]

    get_page(url)
