import random
import re
import time

import requests
import json
import pandas as pd
from jsonpath import jsonpath

class MeiTuan(object):

    def __init__(self):
        self.url = "http://meishi.meituan.com/i/api/channel/deal/list"
        self.headers = {
                'Host': 'meishi.meituan.com',
                'Content-Length': '408',
                'Accept': 'application/json',
                'Origin': 'http://meishi.meituan.com',
                'x-requested-with': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; vivo X9 Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36 VivoBrowser/5.5.4.2',
                'Content-Type': 'application/json',
                'Referer': 'http://meishi.meituan.com/i/?ci=50&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,en-US;q=0.9',
                # cookie 每天在变化 需要及时更新
                'Cookie': '__mta=208057901.1577083547302.1577155994146.1577156005004.16; iuuid=A0A0E36A734E69268243D993E48BE10B027905C1CED069E22EBD0FFFA7AFD3DA; _lxsdk_cuid=16f11a95052c8-02f0c5d0cd399b-5d0a516d-38400-16f11a95053c8; _lxsdk=A0A0E36A734E69268243D993E48BE10B027905C1CED069E22EBD0FFFA7AFD3DA; webp=1; utm_source=60030; _hc.v=80fadb15-f724-953c-2fc7-999864aa7a71.1577083547; wm_order_channel=mtib; IJSESSIONID=2mkn4uqm5aa8jzoeyo3h2tnv; _lx_utm=utm_campaign%3Dwap.sogou%26utm_medium%3Dorganic%26utm_source%3Dwap.sogou%26utm_content%3D100001%26utm_term%3D%2525E7%2525BE%25258E%2525E5%25259B%2525A2%2525E7%2525BD%252591; latlng=29.604538,106.511166,1577236320467; ci3=1; cityname=%E6%9D%AD%E5%B7%9E; __utma=74597006.1786909417.1576549307.1577155329.1577236320.9; __utmb=74597006.7.9.1577236330534; __utmc=74597006; __utmz=74597006.1577236320.9.8.utmcsr=wap.sogou|utmccn=wap.sogou|utmcmd=organic|utmctr=%E7%BE%8E%E5%9B%A2%E7%BD%91|utmcct=100001; i_extend=C_b1Gimthomepagecategory11H__a; _lxsdk_s=16f3a9c4ccc-baf-36d-1a5%7C%7C6; client-id=878af996-e43d-428c-b8f6-d156ef94dbe8; ci=50; meishi_ci=50; cityid=50; uuid=d7d45925-1ab5-46cc-b278-38cbadb489ff; logan_session_token=vpbieyduk7wxj0r1nww5; logan_custom_report=',
                'Connection': 'keep-alive'
        }

        self.data = {"uuid":"bf5ebc0b-31ad-427d-9bb0-5aba775645b1","version":"8.3.3","platform":3,"app":"","partner":126,"riskLevel":1,"optimusCode":10,"originUrl":"http://meishi.meituan.com/i/?ci=50&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1","offset":0,"limit":15,"cateId":1,"lineId":0,"stationId":0,"areaId":0,"sort":"default","deal_attr_23":"","deal_attr_24":"","deal_attr_25":"","poi_attr_20043":"","poi_attr_20033":""}
        self.list = []
        self.category = "美食"

    def save2excel(self):
        df = pd.DataFrame(columns=['城市','类别','美食类别','区域','商圈','店铺名称','地址','电话','人均价格','评分'],data=self.list)
        df.to_excel(self.category + '.xls',index=False)

    def detai_page(self,poiid,ctpoi):
        # 店铺详情页
        detail_url = f"https://meishi.meituan.com/i/poi/{poiid}?ct_poi={ctpoi}"
        headers = {
            'Host': 'meishi.meituan.com',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; vivo X9 Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36 VivoBrowser/5.5.4.2',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'https://meishi.meituan.com/i/?ci=50&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.9',
            'Cookie': '__mta=208057901.1577083547302.1577088654043.1577088771833.9; __mta=208057901.1577083547302.1577089687538.1577090706568.7; iuuid=A0A0E36A734E69268243D993E48BE10B027905C1CED069E22EBD0FFFA7AFD3DA; nodown=yes; _lxsdk_cuid=16f11a95052c8-02f0c5d0cd399b-5d0a516d-38400-16f11a95053c8; _lxsdk=A0A0E36A734E69268243D993E48BE10B027905C1CED069E22EBD0FFFA7AFD3DA; webp=1; utm_source=60030; wm_order_channel=mtib; IJSESSIONID=1xoadt73q2j3v1cb5rlqysxrof; ci3=1; _lx_utm=utm_campaign%3Dwap.sogou%26utm_medium%3Dorganic%26utm_source%3Dwap.sogou%26utm_content%3D100001%26utm_term%3D%2525E7%2525BE%25258E%2525E5%25259B%2525A2%2525E7%2525BD%252591; uuid=bf5ebc0b-31ad-427d-9bb0-5aba775645b1; _hc.v=80fadb15-f724-953c-2fc7-999864aa7a71.1577083547; latlng=29.591653,106.515245,1577090701843; cityname=%E6%9D%AD%E5%B7%9E; __utma=74597006.1786909417.1576549307.1577086404.1577090701.5; __utmb=74597006.2.9.1577090705051; __utmc=74597006; __utmz=74597006.1577090701.5.5.utmcsr=meishi.meituan.com|utmccn=(referral)|utmcmd=referral|utmcct=/i/; i_extend=C_b1Gimthomepagecategory11H__a; ci=50; meishi_ci=50; cityid=50; logan_session_token=d6yhsaox41gjeg6zmitk; logan_custom_report=; client-id=878af996-e43d-428c-b8f6-d156ef94dbe8; _lxsdk_s=16f31ac8864-fa4-488-787%7C%7C151'
        }

        response = requests.get(detail_url,headers=headers)
        json_text = re.findall('window._appState = (.*?);</script>',response.text)[0]
        str_text = json.loads(json_text)

        cityName = jsonpath(str_text,"$..cityName")[0]  # 城市名称
        name= jsonpath(str_text, "$..name")[0]  # 店铺名称
        addr = jsonpath(str_text, "$..addr")[0] # 地址
        area = addr[:3] if "区" in addr else ""   # 所属区
        phone = jsonpath(str_text, "$..phone")[0]   # 电话
        avgPrice = jsonpath(str_text, "$..avgPrice")[0] # 平均价格
        avgScore = jsonpath(str_text, "$..avgScore")[0] # 平均评分

        print(cityName,area,name,addr,phone,avgPrice,avgScore)
        return cityName,area,name,addr,phone,avgPrice,avgScore

    def run(self):
        response = requests.post(self.url,headers=self.headers,data=json.dumps(self.data))
        print(response.text)
        data = response.json()

        # 获取所有的店铺数量
        totalCount = data["data"]["poiList"]["totalCount"]
        datas = data["data"]["poiList"]["poiInfos"]

        for data in datas:
            time.sleep(random.random())
            catename = data.get("cateName", "")  # 所属分类
            areaname = data.get("areaName", "")  # 商圈
            poiid = data.get("poiid", "")
            ctpoi = data.get("ctPoi", "")
            cityName, area, name, addr, phone, avgPrice, avgScore = self.detai_page(poiid, ctpoi)

            self.list.append([cityName,self.category,catename,area,areaname,name,addr,phone,avgPrice,avgScore])

        offset=0
        if totalCount >15:
            while offset < totalCount:
                offset += 15
                self.data["offset"] = offset
                response = requests.post(self.url,headers=self.headers,data=json.dumps(self.data))
                data = response.json()
                datas = data["data"]["poiList"]["poiInfos"]
                for data in datas:
                    catename = data.get("cateName", "")  # 所属分类
                    areaname = data.get("areaName", "")  # 商圈
                    poiid = data.get("poiid", "")
                    ctpoi = data.get("ctPoi", "")
                    if poiid and ctpoi:
                        cityName, area, name, addr, phone, avgPrice, avgScore = self.detai_page(poiid, ctpoi)

                        self.list.append([cityName, self.category, catename, area, areaname, name, addr, phone, avgPrice, avgScore])
                    else:
                        continue
        self.save2excel()
if __name__ == '__main__':
    meituan = MeiTuan()
    meituan.run()



# s = [['a','b','c'],['d','e','f']]
# df = pd.DataFrame(columns=['A','B','C'],data=s)
# df.to_excel('test.xls',index=False)