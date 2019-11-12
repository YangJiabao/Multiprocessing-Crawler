import requests
import json
import os
from multiprocessing import Pool

class lol_hero:
    def hero(self,data):
        hero_data_list = []
        data_dict = {}
        '''
        #for i in hero_list_number:
        url = 'https://game.gtimg.cn/images/lol/act/img/js/hero/{}.js'.format(str(i))
        req = self.request_hero(url)
        #print(req.status_code)
            #print(url)
        data_dict = {}
        data = json.loads(req.text)#读取json
        self.img_save(i,data)
        '''
        data_dict['名字'] = data['hero']['name'] + '-' + data['hero']['title']
        data_dict['介绍'] = data['hero']['shortBio']
        data_dict['被动技能'] = data['spells'][1]['name']
        data_dict['被动技能介绍'] = data['spells'][1]['description']
        data_dict['Q'] = data['spells'][2]['name']
        data_dict['Q技能介绍'] = data['spells'][2]['description'] + "----详细说明----->" + data['spells'][2]['dynamicDescription']
        data_dict['W'] = data['spells'][4]['name']
        data_dict['W技能介绍'] =  data['spells'][4]['description'] + "----详细说明----->" + data['spells'][4]['dynamicDescription']
        data_dict['E'] = data['spells'][0]['name']
        data_dict['E技能介绍'] = data['spells'][0]['description'] + "----详细说明----->" +  data['spells'][0]['dynamicDescription']
        data_dict['R'] = data['spells'][3]['description'] + "----详细说明----->" +  data['spells'][3]['name']
        data_dict['R技能介绍'] = data['spells'][3]['dynamicDescription']
            #print(data_dict)
        hero_data_list.append(data_dict)
        #print(hero_data_list)
        #print(data['hero']['name'])
        #print(data['spells'][0]['name'])
        return hero_data_list

    '''
    def hero_list(self):
        url = 'https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js'
        rec = self.request_hero(url)
        hero_data = json.loads(rec.text)  # 读取json
        hero_list_number = []
        for i in range(0,145):
            number = hero_data['hero'][i]['heroId']
            hero_list_number.append(number)
            #print(hero_list_number)
        self.hero(hero_list_number)
        return
'''
    def img_save(self,i,data):
        for j in range(0, 30):
            if j < 10:
                url1 = 'https://game.gtimg.cn/images/lol/act/img/skinloading/{}00{}.jpg'.format(i, j)
                url2 = 'https://game.gtimg.cn/images/lol/act/img/skin/big{}00{}.jpg'.format(i, j)
            else:
                url1 = 'https://game.gtimg.cn/images/lol/act/img/skinloading/{}0{}.jpg'.format(i, j)
                url2 = 'https://game.gtimg.cn/images/lol/act/img/skin/big{}0{}.jpg'.format(i, j)
            req_img = self.request_hero(url1)
            req_img2 = self.request_hero(url2)
            if (req_img2.status_code & req_img.status_code) == 200:
                name1 = data['skins'][0]['name'] + '-' + data['skins'][0]['heroTitle']
                name2 = (data['skins'][j]['name'] + 'big').replace('"', '-').replace('/', '-').replace(':', '-')  # 替换命名规范符号
                isExists = os.path.exists(os.path.join("E:\loe", name1))
                if not isExists:
                    print('建了一个文件夹！')
                    os.makedirs(os.path.join("E:\loe", name1))  # 创建文件夹
                    os.chdir(os.path.join("E:\loe", name1))  ##切换到目录
                else:
                    print(name1, '文件夹已经存在了！第', j, '个皮肤开始保存！')
                if int(data['skins'][j]['chromas']) == 0:  # 去掉炫彩
                    os.chdir(os.path.join("E:\loe", name1))  ##切换到目录
                    f = open(name2 + '.jpg', 'ab')
                    f.write(req_img.content)
                    f = open(name2 + '1.jpg', 'ab')
                    f.write(req_img2.content)
                    f.close()
        print('--------------------------------------------------------')
        return

    def save_file(self,hero_data_list):
        #s =hero_data_list.decode("unicode-escape")
        content = json.dumps(hero_data_list,ensure_ascii=False, indent=4)
        print(content)
        # 把全局变量转化为json数据
        #os.makedirs(os.path.join("E:\loe", '英雄介绍及技能'))  # 创建文件夹
        os.chdir(os.path.join("E:\loe", '英雄介绍及技能'))  ##切换到目录
        with open( '英雄介绍及技能.json','a+',encoding="utf-8") as f:
            f.write(content)
            #print(content)
            print("全部英雄介绍及技能json文件写入成功！全部英雄及皮肤图片下载成功！")
        return

    def request_hero(self,url):
        headers1 = {
            'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 77.0.3865.90Safari / 537.36'
        }
        req = requests.get(url, headers=headers1)
        return req

    def __init__(self):
        p = Pool(20)
        url = 'https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js'
        rec = self.request_hero(url)
        hero_data = json.loads(rec.text)  # 读取json
        os.makedirs(os.path.join("E:\loe", '英雄介绍及技能'))  # 创建文件夹
        for i in range(0,146):
            number = hero_data['hero'][i]['heroId']
            url1 = 'https://game.gtimg.cn/images/lol/act/img/js/hero/{}.js'.format(str(number))
            req = self.request_hero(url1)
            data1 = json.loads(req.text)  # 读取json
            s = self.hero(data1)
            #hero_list_number.append(number)
            #print(hero_list_number)
        #self.hero(hero_list_number)
            p.apply_async(self.img_save,args=(number,data1,)) ##给函数all_url传入参数,逗号别忘了
            self.save_file(s)
        p.close()
        p.join()


if __name__=='__main__':
    LOL = lol_hero()  ##实例化


