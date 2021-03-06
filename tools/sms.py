import datetime
import hashlib
import base64
import json
import requests

class YunTongXin():

    base_url = 'https://app.cloopen.com:8883'

    def __init__(self, accountSid, accountToken, appId, templateId):

        self.accountSid = accountSid
        self.accountToken = accountToken
        self.appId = appId
        self.templateId = templateId

    # 构造url
    def get_request_url(self, sig):

        self.url = self.base_url + \
                   '/2013-12-26/Accounts/{}/SMS/TemplateSMS?sig={}'.format(self.accountSid, sig)

        return self.url

    def get_timestamp(self):
        # 生成时间戳
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    def get_sig(self, timestamp):

        s = self.accountSid + self.accountToken + timestamp
        m = hashlib.md5()
        m.update(s.encode())

        return m.hexdigest().upper()

    def get_request_header(self, timestamp):
        # 构建请求头
        # 1.使用Base64编码（账户Id + 冒号 + 时间戳）其中账户Id根据url的验证级别对应主账户
        # 2.冒号为英文冒号
        # 3.时间戳是当前系统时间，格式"yyyyMMddHHmmss"，需与SigParameter中时间戳相同。
        s = self.accountSid + ':' + timestamp
        b_s = base64.b64encode(s.encode()).decode()
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=utf-8',
            'Authorization': b_s
        }

    def get_request_body(self, phone, code):
        # 构建请求体
        data = {
            "to": phone,
            "appId": self.appId,
            "templateId": self.templateId,
            "datas": [code,"3"]
        }
        return data

    def do_request(self, url, header, body):
        # 发请求
        res = requests.post(url, headers=header, data=json.dumps(body))
        return res.text

    def run(self, phone, code):
        # 第一部分 构建url
        timestamp = self.get_timestamp()
        sig = self.get_sig(timestamp)
        url = self.get_request_url(sig)
        header = self.get_request_header(timestamp)
        body = self.get_request_body(phone, code)
        res = self.do_request(url, header, body)
        return res

if __name__ == '__main__':

    aid = '8a216da8730561fd017309d02f700237'
    atoken = 'afe61368cd4d4d0d9a6878f26cae0cc5'
    appId = '8a216da8730561fd017309d03055023d'
    templateId = '1'
    x = YunTongXin(aid, atoken, appId, templateId)
    res = x.run('15259964385', '881227')
    print(res)

