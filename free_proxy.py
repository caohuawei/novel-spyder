import json
import requests
from tools import write_txt

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60"
}
proxy = []

def getProxy():
        url = "http://proxylist.fatezero.org/proxy.list"
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
        ##使用split即将每一条ip都变成一个列表的一个元素
            lists = r.text.split('\n')
            for i in lists:
                try:
                    li = json.loads(i, strict=False)
                    ##提取高匿http代理
                    if str(li['anonymity']) == 'high_anonymous' and str(li['type']) == 'http':
        
                        ip_port = str(li['host'])+":"+str(li['port'])
                        proxy.append(ip_port)
                except:
                    continue

def testProxy(t_proxy):
    target_proxy = t_proxy or proxy
    # c_ip_port = []
    for ip_port in target_proxy:
        c_proxy = {
            'http':ip_port
        }
        try:
            r = requests.get('http://www.baidu.com',headers=headers, proxies=c_proxy, timeout=5)
            print(r.status_code)
            if r.status_code != 200:
                target_proxy.remove(ip_port)
            else:
                # c_ip_port = [ip_port]
                print("success:{}".format(ip_port))
                # break
        except:
            target_proxy.remove(ip_port)
            print("faild:{}".format(ip_port))
    write_txt('ip_port.txt', '\n'.join(target_proxy))
    return target_proxy
    # return c_ip_port