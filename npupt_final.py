import requests
from bs4 import BeautifulSoup
import time
import re
import random 
from copy import deepcopy
import datetime
from os import getcwd

def manydowns(ups,downs):
    if 2*ups <= downs:
        return True
    else:
        return False
    
working_path = getcwd()    
conf = open(working_path + '\\gettorrent.txt','r')
configlist = conf.read()
config = {}
for line in configlist.split('\n'):
    key,value = line.split('=',1)
    config[key] = value
conf.close()



movies = open(r'C:\Users\李宇衡\Desktop\auto downloaded\剧集 关键词.txt','r')
varieties = open(r'C:\Users\李宇衡\Desktop\auto downloaded\综艺 关键词.txt','r')

#设置请求信息
url = config['url']
cookie_str = config['cookie_str']
cookies ={}
for line in cookie_str.split(';'):
    key, value = line.split('=',1)
    cookies[key] = value
headers = {'User-agent':config['user_agent']}
#Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134

old_pattern = re.compile('[年月日时]')

#从txt获取关键词列表
#暂不可用
key_list = []
movielist = movies.read()
varietylist = varieties.read()
for keywords in movielist.split('\n'):
    key_list.append(keywords)
for keywords in varietylist.split('\n'):
    key_list.append(keywords)
key_str = ''
for one in key_list:
    key_str += one + '|'
key_str = key_str[0:-1]
key_pattern = re.compile(key_str)

lastname = ''
five_downs = []

def popular(name):
    if re.search(key_pattern,name) == None:
        return False
    else:
        return True

    
#循环检查
while 1:
    resp = requests.get(url, headers = headers, cookies = cookies)
    tmp = BeautifulSoup(resp.content,'html.parser')
    a = tmp.find_all('td',attrs={'class':'rowfollow left nobr td-thin','id':'torrenttable_username'})

    whichone = 0
    for one in a:
        tim = one.find('td',attrs={'class':'nobr'})
        tim = tim.find('div',attrs={'class':'small'})
        tim = tim.find('span')
        tim = tim.get_text()
        if re.search(old_pattern,tim) == None:
            break
        whichone += 1

    print(whichone)
    if whichone > 100:
        time.sleep(200+random.randint(0,200))
        continue

    #解析新的前五个
    tmp_name_id = tmp.find_all('td',attrs={'class':'rowfollow th-fat'})
    tmp_name_id = tmp_name_id[whichone:whichone+5] #前五个
    tmp_up_down = tmp.find_all('td',attrs={'class':'rowfollow vcenter nowrap'})
    tmp_up_down = tmp_up_down[whichone:whichone+5]
    namelist = []
    idlist=[]
    chs_name = []
    uplist = []
    downlist = []
    for one in tmp_name_id:
        name_id = one.find('a')
        name = name_id['title']
        namelist.append(name)
        id_ = name_id['href']
        id_ = id_[15:21]
        idlist.append(id_)
        #chs_name = one.find_all('span')
        #print(chs_name[0].get_text())
        
    for one in tmp_up_down:
        ups = one.find('a')
        ups = ups.find('b')
        uplist.append(ups.get_text())
        downs = one.find_all('span',attrs={'class':'badge'})
        downlist.append(downs[1].get_text())

    samplelist = []
    i = 0
    tmpdic = {}
    while i < 5:
        t = namelist[i].replace('\\','')
        t = t.replace('/','')
        tmpdic['name'] = t
        tmpdic['id'] = idlist[i]
        tmpdic['ups'] = uplist[i]
        tmpdic['downs'] = downlist[i]
        samplelist.append(tmpdic)
        tmpdic = deepcopy(tmpdic)       
        #print(samplelist)
        i += 1
    
    now = datetime.datetime.now()
    clock = now.strftime('%y-%m-%d %H:%M:%S')
    print(clock)
    
    for sample in samplelist:
        pop = popular(sample['name'])
        print(sample['name'],end='   ')
        if pop == False:
            print('not ',end='')
        print('popular  ',end='')
        many = manydowns(sample['ups'],sample['downs'])
        if many == False:
            print('not ',end='')
        print('manydowns')
        if pop or many == True:
            if (sample['name'] in five_downs) == False:
                five_downs.append(sample['name'])
                download_url = 'https://npupt.com/download.php?id=' + sample['id'] + '&passkey=' + config['passkey']
                torrent = requests.get(download_url, headers = headers, cookies = cookies)        
                print('  write started')
                path = config['path'] + name + '.torrent'
                f = open(path,'wb')
                f.write(torrent.content)
                f.close()
                print('  write ended')
                if(len(five_downs) == 6):
                    five_downs.pop(0)
        print('\n')
    time.sleep(500+random.randint(0,200))

       

    
   
