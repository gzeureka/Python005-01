
#!/usr/bin/env python
# 使用 requests 库抓取知乎任意一个话题下排名前 15 条的答案内容(如果对前端熟悉请抓取所有答案)，并将内容保存到本地的一个文件

import requests
from lxml import etree
import sys


def get_page(url):
    '''获取答案内容，返回文本的list'''
    print(f'Getting "{url}"')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    selector = etree.HTML(response.text)

    list = []

    answers = selector.xpath(
        '//*[@id="QuestionAnswers-answers"]/div/div/div/div[2]/div')
    for a in answers:
        contents = a.xpath('//*[@class="RichContent-inner"]/span')
        for c in contents:
            text = c.text
            if not text is None:
                list.append(c.text)

    return list


def save_to_file(list, file_name):
    '''写入文件'''
    with open(file_name, mode='w') as f:
        for i in list:
            f.write(i)
    
    print(f'{file_name} saved')


if __name__ == '__main__':
    # 检查命令行参数个数
    if len(sys.argv) < 2:
        url = 'https://www.zhihu.com/question/20484909'
    else:
        url = sys.argv[1]

    save_to_file(get_page(url), 'answer.txt')

