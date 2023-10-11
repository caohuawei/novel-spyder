import time
import urllib3
from lxml import etree
import search_engine
from tools import saveToCSV, parseHTML, read_txt, filterWebsite
from free_proxy import getProxy, testProxy

urllib3.disable_warnings()


def HTML(api):
    f_keyword = api.conf['keyword'].replace(' ', '+')
    title = []
    caption_cite = []
    first = 1
    while first < int(api.conf['limit']):
        time.sleep(api.conf['sleep'])
        html = api.getBing(first)
        parseHTML(etree.HTML(html), title, caption_cite)
        first += int(api.conf['count'])
    # 搜索结果
    saveToCSV(f_keyword, title, caption_cite, api.conf['csv_path'])
    f_title, f_caption_cite = filterWebsite(title, caption_cite, api.conf['genuine_website'], api.conf['error_keyword'])
    # 筛选结果
    saveToCSV(f"{f_keyword}_filter", f_title, f_caption_cite, api.conf['csv_path'])


if __name__ == '__main__':
    #是否免费代理ip
    verify = 0
    proxy = read_txt('ip_port.txt')
    if proxy and verify:
        proxy = testProxy(proxy)
    elif not proxy:
        getProxy()
        proxy = testProxy(proxy)
    api = search_engine.Engine(proxy)
    HTML(api)



