# coding:utf-8 
# 小航影院爬虫脚本
import requests
requests.packages.urllib3.disable_warnings()
from bs4 import BeautifulSoup
from urllib.parse import quote
from utils.customLogger import CustomLog
import re,os
from utils.vprint import sprint,fprint
import threading
import queue

Q = queue.Queue()

logger = CustomLog(__name__).getLogger()
search_url = "https://movie.xhboke.com/index.php/vod/search.html"
root_url = "https://movie.xhboke.com"

def status(r,status_code):
    if r.status_code == status_code:
        return True
    
    return False


def search(movies_name):
    '''
    @param {type} 电影名字
    @return: 
    '''
    movies_name = quote(movies_name, 'utf-8')
    payload = "wd="+movies_name+"&submit="
    headers = {
        'content-type': "application/x-www-form-urlencoded",
    }
    r = requests.post(search_url,data=payload,headers=headers,verify=False)
    return r

# 解析获取实际播放的内容和视频标题
def get_search_result(r):
    html = r.text
    soup = BeautifulSoup(html,"html.parser")
    results = soup.find_all('a',class_="btn-play btn-primary")

    titles = soup.find_all('h3',class_="title text-overflow")
    for name,result in zip(titles,results):
        link = result['href']
        title = name.text
        print("title: %s | link: %s" % (title, link))
        Q.put((link, title))


def get_content(i):
    content = ""
    while True:
        link, title = Q.get()
        links = get_playlist(link)
        content += title + "\n"
        for url in links:
            url = url['href']
            t,u = get_video(url)
            m3u8_url = get_m3u8(u)
            content += t+" | "+m3u8_url + '\n'

    sprint("线程{}获取到内容：{}".format(i,content))
    with open(os.path.join("download", movies_name + ".txt"), 'a', encoding='utf-8') as f:
        f.write(content)
    # return content

# 获取真实的视频链接
def get_m3u8(url):
    url = re.sub("\"", "", url)
    if not re.search('m3u8',url):
        r = requests.get(url,verify=False)
        res = re.search("var main = \"(.*?)\"", r.text)
        res.group(1)
        link = re.sub("share/.*", res.group(1),url)
    else:
        link = url
    #print("m3u8 links：",link)
    return link 

# 得到播放列表
def get_playlist(link):
    '''
    @param {type} 
    @return: 
    '''
    r = requests.get(root_url+link,verify=False)
    html = r.text
    soup = BeautifulSoup(html,'html.parser')
    ul = soup.find(id='con_playlist_1')
    links = ul.find_all('a')
    #print("playlist:",links)
    return links 


def get_video(link):
    '''
    @param {type}  详细播放页面链接
    @return: 影片名字，播放器链接
    '''
    r = requests.get(root_url+link,verify=False)
    if r.status_code == 200:
        html = r.text
        result = re.search("link_next.*\"url\"\:(.*?)\,",html)
        link = re.sub(r'\\','',result.group(1))
        title = re.search("vod_part=\'(.*?)\'\;",html).group(1)

    else:
        title = ""
        link = "Error. The res is {}".format(r.text)
    return title,link


def xhrun(movies_name):
    sprint("正在小航影院进行搜索....")
    r = search(movies_name)
    if status(r,200):
        get_search_result(r)
        get_content()
        # ts = [threading.Thread(target=get_content,args=(i,)) for i in range(20)]
        # for t in ts:
        #     t.start()
        # for t in ts:
        #     t.join()
    else:
        fprint("Error, status code is %s " % r.status_code)
   

