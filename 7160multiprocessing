import requests
from bs4 import BeautifulSoup
import os
from multiprocessing import Pool

#导入所需要的模块
class work:
    def all_url(self, url):
        html = self.request(url)##调用请求
        html.encoding = 'gb2312'#此处网页编码为gb2312
        all_a = BeautifulSoup(html.text, 'lxml').find('div', class_='news_bom-left').find_all('a',attrs={"target": True})#使用target跳过前两个href
        for a in all_a:
            title = a.get_text()#获取链接标题
            #path = str(title).replace("?", '_') ##替换掉带有的？
            self.mkdir(str(title)) ##调用mkdir函数创建文件夹！这儿path代表的是标题title
            href = a['href']#取出href属性
            url2 = "https://www.7160.com" + href
            self.html(url2)

    def html(self, href):   ##获得图片的页面地址
        html = self.request(href)
        html.encoding = 'gb2312'
        max_span = BeautifulSoup(html.text, 'lxml').find('div', class_='itempage').find_all('a')[-2].get_text()
        #使用get_text()清空所有html标签元素,之后就会返回干净的文字,使用get_text()方法从大段html中提取文本,这里提取页码数字,因为实际href比抓的少,所以减去两个
        for page in range(1, int(max_span) + 1):
            print("第" ,page , "页")#???int(max_span)
            if page ==1:
                page_url = href[0:34] + 'index' + ".html"
                self.img(page_url)
            else:
                page_url = href[0:34] + 'index_' + str(page) + ".html"
                #print(page_url)
                self.img(page_url) ##调用img函数

    def img(self, page_url): ##处理图片页面地址获得图片的实际地址
        img_html = self.request(page_url)
        img_html.encoding = 'gb2312'
        #print(img_html.content)#...截取html如果只是片段的话，可能是因为get的网址就是那么多代码，用get的网址打开源代码看一下
        img_url = BeautifulSoup(img_html.text, 'lxml').find('div', class_='picsbox picsboxcenter').find('img')['src']
        self.save(img_url)

    def save(self, img_url): ##保存图片
        name = img_url[-10:-4]#用图片的名称保存,截取部分字符串
        headers1 = {
            'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'referer': "url1",  # 伪造一个访问来源
            'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;v = b3',
            'Accept - Encoding': 'gzip, deflate, br',
            'Accept - Language': 'zh - CN, zh;q = 0.9',
            'Connection': 'keep - alive'
        }
        img = requests.get(img_url, headers = headers1,verify = False)#verify = False，不验证https证书，这里验证的话抓取时间长了会报ssl错误
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close()

    def mkdir(self, path): ##创建文件夹
        path = path.strip()#用于移除字符串头尾指定的字符,此处用于去除字符串空格
        isExists = os.path.exists(os.path.join("E:\wwe",path))#os.path.exists判断括号里的文件是否存在的意思，括号内的可以是文件路径。
        if not isExists:
            print('建了一个文件夹！')
            os.makedirs(os.path.join("E:\wwe",path))#创建文件夹
            os.chdir(os.path.join("E:\wwe",path)) ##切换到目录
            return True
        else:
            print( path, '文件夹已经存在了！')
            os.chdir(os.path.join("E:\wwe", path))  ##切换到目录
            return False

    def request(self, url): ##这个函数获取网页的response 然后返回
        headers = {
            'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'referer':"https://www.7160.com/",#伪造一个访问来源
            'Connection': 'keep - alive'
        }
        content = requests.get(url, headers=headers)
        return content

    def __init__(self):
        p = Pool(20)
        for j in range(1,200):
            print('第{}组开始下载'.format(j))#每下载一组输出第几组正在下载
            url1 = "https://www.7160.com/qingchunmeinv/list_2_{}.html".format(str(j))
            p.apply_async(self.all_url,args=(url1,)) ##给函数all_url传入参数,逗号别忘了
        p.close()
        p.join()


if __name__=='__main__':
    worm = work()  ##实例化
