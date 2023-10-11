import json
import random
import requests
import configparser
import bing
from tools import read_txt, write_txt



class Engine():

    def __init__(self, proxy):
        self.host = []
        self.conf = {}
        ip_port = random.choice(proxy)
        print(f"ip_port: {ip_port}")
        self.proxies = {
            'http': ip_port,
        }
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60"
        }
        config = configparser.ConfigParser()
        config.read("config.ini", encoding='utf-8')
        self.conf['sleep'] = int(config['config']['sleep'])
        self.conf['csv_path'] = config['config']['csv_path']
        self.conf['keyword'] = config['config']['keyword']
        self.conf['count'] = config['config']['count']
        self.conf['limit'] = config['config']['limit']
        self.conf['genuine_website'] = config['config']['genuine_website']
        self.conf['error_keyword'] = json.loads(config['config']['error_keyword'])
        resp =requests.get('https://cn.bing.com/', verify=False)
        self.cookie = resp.cookies  # 获取cookie bing在搜索时需要带上cookie

    def getBing(self, first):
        try:
            keyword = self.conf['keyword']
            # text = bing.Bing().search(keyword)
            # write_txt('content.html', text)
            # return text

            params = {
                'q': f'"{keyword}"',
                'first': first,
                'count': self.conf['count'],
            }
            r = requests.get('https://cn.bing.com/search', params=params, cookies=self.cookie, verify=False, headers=self.headers, proxies=self.proxies)
            r.encoding = r.apparent_encoding
            write_txt('content.html', r.text, 'w' if first == 1 else 'a')
            return r.text
            
        except Exception as e:
            print(f"Get Bing Failed:{e}")

            
