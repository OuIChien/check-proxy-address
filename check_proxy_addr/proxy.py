import requests
import sys
import threading

head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
url = 'http://139.162.122.46:8000/ip/'

succ = {}

class Check(threading.Thread):
    def __init__(self, addr, name):
        threading.Thread.__init__(self)
        self.addr = addr
        self.name = name

    def run(self):
        #print('checking:' + self.addr)
        try:
            request = requests.get(url, proxies={'http': self.addr}, headers=head)
            request.encoding = request.apparent_encoding
            if request.text == self.addr.split(':')[0]:
                print('可用:' + self.addr + self.name)
                succ[self.addr] = self.name
            else:
                #print('失败,实际:' + request.text + ',期望:' + self.addr + self.name)
                pass
        except(requests.exceptions.ProxyError):
            #print('不可用:' + self.addr + self.name)
            pass


def start():
    with open('ips2.txt', 'r', encoding='utf-8') as ips_file:
        while True:
            line = ips_file.readline()
            if line == '':
                break
            ip = line.split(',')
            if len(ip) == 2:
                t = Check(ip[0], ip[1])
                t.start()
            else:
                print(line)

start()