import requests
from bs4 import BeautifulSoup
import os
import json
from multiprocessing import Pool

class wangzhe():
    def hero_skills(self,rec,alt):
        rec.encoding = 'gbk'
        #print(rec.text)
        skill = BeautifulSoup(rec.text, 'lxml').find_all('div', class_='show-list')[0:4]
        skill_list = []
        for (s,i) in zip(skill,['-被动','-1技能','-2技能','-3技能']):
            text1 = s.text
            skill_list.append(alt + i + text1.replace('\n','---------'))
            #print(skill_list)
        os.chdir(os.path.join("E:\wangzhe1"))  ##切换到目录
        content = json.dumps(skill_list, ensure_ascii=False, indent=4)
        #print(type(content))
        with open('英雄介绍及技能.json', 'a+', encoding="utf-8") as f:
            f.write(content)
            print('>>>>>技能下载中>>>>')

    def hero_img_dow(self,alt,num):
            for i in range(0,10):
                url = 'https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{}/{}-bigskin-{}.jpg'.format(num,num,i)
                rec = self.request(url)
                #print(rec.status_code)
                #print(rec)
                if rec.status_code ==200:
                    isExists = os.path.exists(os.path.join("E:\wangzhe1", alt))
                    if not isExists:
                        print('建了一个文件夹！')
                        os.makedirs(os.path.join("E:\wangzhe1", alt))  # 创建文件夹
                        self.save_img(alt,i,rec)
                    else:
                        print(alt, '文件夹已经存在！皮肤保存中>>>>>>>>')
                        self.save_img(alt, i, rec)

    def save_img(self,alt,i,rec):
        os.chdir(os.path.join("E:\wangzhe1", alt))  ##切换到目录
        f = open(alt + str(i) + '.jpg', 'ab')
        f.write(rec.content)


    def hero_list_number(self):
        url = 'https://pvp.qq.com/web201605/herolist.shtml'
        rec = self.request(url)
        rec.encoding = 'gbk'
        number = []#英雄编号
        alts = []#英雄名字
        figure = BeautifulSoup(rec.text, 'lxml').find('div', class_='herolist-content').find_all('a',attrs={"target": True})
        print(figure)
        for all in figure:
            href = all['href']
            alt = all.get_text()#清空所有标签元素，只留下文字内容
            number.append(href[-9:-6])
            alts.append(alt)
        print(number)
        print(alts)
        ##self.hero_img_dow(number,alts)
        return number,alts


    def request(self,url):
        headers1 = {
            'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
        req = requests.get(url,headers=headers1)
        return req


    def __init__(self):
        p = Pool(20)
        number, alts = self.hero_list_number()
        for (num,alt) in zip(number,alts):
            url1 = 'https://pvp.qq.com/web201605/herodetail/{}.shtml'.format(num)
            rec1 = self.request(url1)
            self.hero_skills(rec1,alt)
            p.apply_async(self.hero_img_dow,args=(alt,num,))
        p.close()
        p.join()

if __name__ == '__main__':
    WANG = wangzhe()
