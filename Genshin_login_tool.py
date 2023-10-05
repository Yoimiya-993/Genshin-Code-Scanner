import json
import os.path
import pickle
import random
import sys
import time
import warnings
from hashlib import md5
from typing import List
from threading import Thread

import numpy as np
import cv2 as cv
import requests
import httpx
import mss

sys.path.append(os.path.abspath('.'))


def scan_frame():
    import scan_frame


def create_scan_frame():
    frame_thread = Thread(target=scan_frame)
    frame_thread.start()


class User:
    def __init__(self, web_cookie):
        self.web_cookie = web_cookie
        web_cookie = parse_cookie(web_cookie)
        self.uid = web_cookie['login_uid']
        self.ticket = web_cookie['login_ticket']
        self.stoken = self.get_stoken(web_cookie)
        self.game_token = self.get_game_token()
        # self.role = self.get_role()

    @staticmethod
    def get_stoken(web_cookie: dict):
        url = 'https://api-takumi.mihoyo.com/auth/api/getMultiTokenByLoginTicket'
        params = {
            'login_ticket': web_cookie['login_ticket'],
            'token_types': 3,
            'uid': web_cookie['login_uid']
        }
        get_url1 = requests.get(url, params)
        if get_url1.status_code == 200:
            tokens = json.loads(get_url1.text)
            if tokens.get('message') == 'OK':
                tokens = tokens['data']['list']
                for item in tokens:
                    if item.get('name') == 'stoken':
                        print('获取token成功')
                        return item['token']

    def get_game_token(self):
        url = 'https://api-takumi.mihoyo.com/auth/api/getGameToken'
        get_url = requests.get(url, {'stoken': self.stoken, 'uid': self.uid})
        if get_url.status_code == 200:
            json_loads = json.loads(get_url.text)
            if json_loads.get('message') == 'OK':
                return json_loads['data']['game_token']

    def get_role(self):
        url = 'https://api-takumi.miyoushe.com/binding/api/getUserGameRolesByStoken'
        headers['DS'] = get_DS()
        get_url = httpx.get(url,
                               cookies={'stuid': self.uid,
                                        'stoken': self.stoken,
                                        'mid': '043co169fb_mhy'},
                               headers=headers)
        if get_url.status_code == 200:
            json_loads = json.loads(get_url.text)
            if json_loads.get('message') == 'OK':
                return json_loads['data']['list']

    def __str__(self):
        # role = self.role[0]
        # return f'{role["nickname"]} UID：{role["game_uid"]} {role["region_name"]} {role["level"]}级'
        return f'米游社ID：{self.uid}'


def parse_header_and_cookie(text: str):
    text = text.strip().split('\n')[1:]
    text = [item.strip().split(':', 1) for item in text if item]
    headers_ = {k.strip(): v.strip() for k, v in text}
    cookie_ = headers_.pop('cookie')
    cookie_ = parse_cookie(cookie_)
    return headers_, cookie_


def parse_cookie(text: str):
    cookie_ = [item.strip().split('=', 1) for item in text.strip().split(';') if item]
    cookie_ = {k.strip(): v.strip() for k, v in cookie_}
    return cookie_


def get_qr_code():
    # 识别二维码
    with mss.mss() as sct:
        img = sct.grab(dict(left=region[0] // 2 - region[2] // 2, top=region[1] // 2 - region[3] // 2, width=region[2], height=region[3]))
    img = np.array(img)
    # img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    return detector.detectAndDecode(img)[0]


def get_qr_ticket():
    # 获取ticket
    qr_code = get_qr_code()
    if qr_code:
        return qr_code[0][-24:]


def get_DS():
    # 获取DS
    time_now = str(int(time.time()))
    rand = str(random.randint(100001, 200000))
    m = f'salt={salt}&t={time_now}&r={rand}'.encode('u8')
    return f'{time_now},{rand},{md5(m).hexdigest()}'


def save_users():
    with open('userinfo.pickle', 'wb') as f:
        pickle.dump(users, f)


def load_users():
    try:
        with open('userinfo.pickle', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return []


def get_scan_session():
    sess = requests.Session()
    url = 'https://api-sdk.mihoyo.com/hk4e_cn/combo/panda/qrcode/scan'
    headers['DS'] = get_DS()
    data_ = {}
    sess.post(url, json=data_, headers=headers, cookies=cookies)
    return sess


def call_scan(t: str, sess: requests.Session):
    url = 'https://api-sdk.mihoyo.com/hk4e_cn/combo/panda/qrcode/scan'
    sess.headers['DS'] = get_DS()
    data_ = {
        "app_id": "4",
        "device": "d9951154-6eea-35e8-9e46-20c53f440ac7",
        "ticket": t
    }
    response = sess.post(url, json=data_)
    return response


def call_confirm(u: User, t: str, sess: requests.Session):
    # print('向服务器发送确认信息')
    url = 'https://api-sdk.mihoyo.com/hk4e_cn/combo/panda/qrcode/confirm'
    sess.headers['DS'] = get_DS()
    data_ = {"app_id": 4,
             "device": "d9951154-6eea-35e8-9e46-20c53f440ac7",
             "payload": {"proto": "Account",
                         "raw": "{\"uid\":\"%s\",\"token\":\"%s\"}" % (u.uid, u.game_token)},
             "ticket": t}
    response = sess.post(url, json=data_, cookies=cookies)
    return response


def login(login_sleep, user, ticket, session, t2):
    if bool(login_sleep):
        time.sleep(float(login_sleep))
    # if 'y' in input('按y进行登录：'):
    res = call_confirm(user, ticket, session)
    t3 = time.time()
    res = json.loads(res.text)
    if res['retcode'] == 0:
        print(f'登录成功，耗时：{t3 - t2:.4f}s\n')
    else:
        print(f'登录失败：{res}\n')


def main():
    while True:
        print()
        if len(users) != 0:
            for i, user in enumerate(users):
                print(f'[{i + 1}]', user, sep=' ')
        else:
            print('【没有任何用户，请添加】')
        order = input('1. 添加用户\n'
                      '2. 删除用户\n'
                      '3. 开始扫码\n'
                      '0. 退出\n'
                      '\n请输入（回车直接使用1号用户速登扫码）：')

        if not bool(order):
            user = users[0]
            cookies['stuid'] = user.uid
            cookies['stoken'] = user.stoken
            # print(f'开始使用【{user.role[0]["nickname"]}】连续扫码\n')
            print(f'开始使用【米游社ID：{user.uid}】连续扫码\n')
            create_scan_frame()
            session = get_scan_session()
            old_ticket = ''
            while True:
                # 识别二维码
                t0 = time.time()
                ticket = get_qr_ticket()
                if (not ticket) or (ticket == old_ticket):
                    continue
                # 扫码
                old_ticket = ticket
                t1 = time.time()
                res = call_scan(ticket, sess=session)
                print(f'识别成功，耗时：{t1 - t0:.4f}s {ticket}')
                t2 = time.time()
                # 确认登录
                res = json.loads(res.text)
                if res['retcode'] == 0:
                    print(f'抢码成功，耗时：{t2 - t1:.4f}s')
                    login_thread = Thread(target=login, args=[0, user, ticket, session, t2])
                    login_thread.start()
                else:
                    print(f'抢码失败，二维码已被扫描\n')

        if order == '0':
            sys.exit(0)
        elif order == '1':
            cookie_new_user = input('请输入米哈游通行证cookie：')
            try:
                user = User(cookie_new_user)
            except ValueError:
                print('解析失败，请检查cookie格式')
            else:
                if user.stoken:
                    users.append(user)
                    save_users()
                    print('添加成功')
                else:
                    print('添加失败，请检查cookie正确性')
        elif order == '2':
            idx = input('请输入待删除的用户编号：')
            if idx.isdigit() and 0 < int(idx) < len(users) + 1:
                idx = int(idx)
                users.pop(idx - 1)
                save_users()
                print('删除成功')
            else:
                print('你输入的数字不对')
        elif order == '3':
            while True:
                try:
                    idx = int(input('请选择你要使用的账号的序号：'))
                    if not 0 < idx < len(users) + 1:
                        raise ValueError
                    else:
                        break
                except ValueError:
                    print('请输入正确的序号')
            login_sleep = input('输入延时登录秒数（回车无延迟）：')
            user = users[idx - 1]
            cookies['stuid'] = user.uid
            cookies['stoken'] = user.stoken
            # print(f'开始使用【{user.role[0]["nickname"]}】连续扫码\n')
            print(f'开始使用【米游社ID：{user.uid}】连续扫码\n')
            create_scan_frame()
            session = get_scan_session()
            old_ticket = ''
            while True:
                # 识别二维码
                t0 = time.time()
                ticket = get_qr_ticket()
                if (not ticket) or (ticket == old_ticket):
                    continue
                # 扫码
                old_ticket = ticket
                t1 = time.time()
                res = call_scan(ticket, sess=session)
                print(f'识别成功，耗时：{t1 - t0:.4f}s {ticket}')
                t2 = time.time()
                # 确认登录
                res = json.loads(res.text)
                if res['retcode'] == 0:
                    print(f'抢码成功，耗时：{t2 - t1:.4f}s')
                    login_thread = Thread(target=login, args=[login_sleep, user, ticket, session, t2])
                    login_thread.start()
                else:
                    print(f'抢码失败，二维码已被扫描\n')


if __name__ == '__main__':
    # 变量
    users: List[User] = load_users()
    cookies = {
        'stuid': '',
        'stoken': '',
        'mid': '043co169fb_mhy'
    }
    warnings.filterwarnings("ignore")
    salt = 'PVeGWIZACpxXZ1ibMVJPi9inCY4Nd4y2'
    app_version = '2.38.1'
    detector = cv.wechat_qrcode_WeChatQRCode('model/detect.prototxt',
                                             'model/detect.caffemodel',
                                             'model/sr.prototxt',
                                             'model/sr.caffemodel')
    # detector = cv.QRCodeDetector()
    headers = {
        'DS': '',
        'x-rpc-client_type': '2',
        'x-rpc-app_version': app_version,
        'x-rpc-sys_version': '7.1.2',
        'x-rpc-channel': 'miyousheluodi',
        'x-rpc-device_id': 'd9951154-6eea-35e8-9e46-20c53f440ac7',
        'x-rpc-device_fp': '38d7ed301ed62',
        'x-rpc-device_name': 'HUAWEI LIO-AN00',
        'x-rpc-device_model': 'LIO-AN00',
        'Referer': 'https://app.mihoyo.com',
        'Content-Type': 'application/json; charset=UTF-8',
        'Host': 'api-sdk.mihoyo.com',
        'Connection': 'Keep-Alive',
        'User-Agent': 'okhttp/4.9.3'
    }
    with open('region.txt', 'r', encoding='u8') as f:
        region = tuple(json.load(f))
    # 主函数
    main()
