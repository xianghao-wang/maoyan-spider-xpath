import requests
import os
import json
from lxml import etree

def get_one_page(url):
    """
        爬取具体一页 sample: url=https://maoyan.com/board/4?offset=0
        @param url: 要抓取页面的url
        @return: 网页的html文本
    """

    headers = {
        'User-Agent': os.getenv('USER_AGENT'),
        'Cookie': os.getenv('COOKIE')
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        return None

def parse_one_page(text):
    """
        解析html文本
        @param text: 要被解析的html文本
        @return: generator[{
            'index', 'image', 'title', 'actor', 'time', 'score'
        }]
    """

    html = etree.HTML(text)
    results = {
        'index': None,
        'image': None,
        'title': None,
        'actor': None,
        'time': None,
        'integer': None,
        'fraction': None
    }

    results['index'] = html.xpath('//dd/i[contains(@class, "board-index")]/text()')
    results['image'] = html.xpath('//dd/a[@class="image-link"]/img[2]/@data-src')
    results['title'] = html.xpath('//dd//p[@class="name"]/a/text()')
    results['actor'] = html.xpath('//dd//p[@class="star"]/text()')
    results['time'] = html.xpath('//dd//p[@class="releasetime"]/text()')
    results['integer'] = html.xpath('//dd//i[@class="integer"]/text()')
    results['fraction'] = html.xpath('//dd//i[@class="fraction"]/text()')

    for i in range(10):
        yield {
            'index': results['index'][i].strip(),
            'image': results['image'][i].strip(),
            'title': results['title'][i].strip(),
            'actor': results['actor'][i].strip()[3:] if len(results['actor'][i]) > 3 else '',
            'time': results['time'][i].strip()[5:] if len(results['time'][i]) > 5 else '',
            'score': results['integer'][i].strip() + results['fraction'][i].strip()
        }

def write_to_file(content):
    with open(os.getenv('RESULT_FILE'), 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')