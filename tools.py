import os
import pandas
import requests
from lxml import etree

def read_txt(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = f.readlines()
        data = [i.strip('\n').strip() for i in data]
    return data

def write_txt(path, data, mode='w'):
    with open(path, mode, encoding='utf-8') as f:
        f.write(data)

def saveToCSV(f_keyword, title, caption_cite, csv_path):
    if not os.path.exists(csv_path):
        os.mkdir(csv_path)
    save_csv_path = csv_path + '/' + f'{f_keyword}.csv'
    DATA = {
        'title': title,
        'caption_cite': caption_cite,
    }
    col_names = ['title', 'caption_cite']
    save = pandas.DataFrame(DATA, columns=col_names)
    save.to_csv(save_csv_path)

def filterWebsite(title, caption_cite, genuine, err_words):
    qd_content = ''
    # qd_c_len = 0
    f_title = []
    f_caption_cite = []
    # 获取qidian
    for cite in caption_cite: 
        if cite.find(genuine) != -1:
            html_text = getHtml(cite)
            content_wrap = etree.HTML(html_text).xpath('//div[@class="read-content j_readContent"]//p')
            content = [i.xpath('string(.)').replace('\u3000', '') for i in content_wrap]
            qd_c_len = len(qd_content)
            print(f"qd_content：{qd_content}")
    for index in range(len(caption_cite)): 
        cite = caption_cite[index]
        if 'qidian.com' not in cite:
            html_text = getHtml(cite)
            # 页面数据错误：0 否 1 是
            err_page = 0
            for word in err_words:
                if word in html_text:
                    err_page = 1
            if not err_page and title[index] not in f_title:
                f_title.append(title[index])
                f_caption_cite.append(cite)
    return f_title, f_caption_cite
            
def getHtml(url):
    try:
        r = requests.get(url)
        r.encoding = r.apparent_encoding
        return r.text
    except Exception:
        print(f"Get Html Failed: {url}")  
        return '获取失败'      

def parseHTML(s, title, caption_cite):
    content = s.xpath('.//li[@class="b_algo"]')
    print("content_len:{}".format(len(content)))
    for each in content:
        t = [i.xpath('string(.)') for i in
             each.xpath('.//div[@class="tptt"]')]
        if t:
            title.extend(t)
        else:
            title.append('None')

        c = [i.xpath('string(.)') for i in
             each.xpath('.//cite')]
        if c:
            caption_cite.extend(c)
        else:
            caption_cite.append('None')
