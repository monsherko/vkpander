# -*- coding: utf-8 -*-
"""
:authors: monsherko
:contact: monsherko@yahoo.com
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2018 monsherko
"""


from core.vk_api.vk_api import VkApi as VkApi

import json
import time
import random
import urllib
import subprocess
import argparse
import multiprocessing
from PIL import ImageTk, Image
import tkinter as tk
from tkinter import *
banner = """
    created by monherko
"""

class App():
    tmp =''

    def __init__(self):
        self.root = tk.Tk()
        self.logo = ImageTk.PhotoImage(file='captcha.jpg')
        self.w1 = tk.Label(self.root, image=self.logo).grid(row=0)
        self.strings = tk.StringVar()
        self.w2= tk.Label(self.root, text='captcha').grid(row=1)
        self.w2 = Entry(self.root)
        self.w2.grid(row=0, column=1)
        Button(self.root, text='ok', command=self.show).grid(row=3, column=1, sticky=W, pady=4)
        mainloop()

    def show(self):
        self.tmp = self.w2.get()
        self.w2.delete(0, END)
        self.root.destroy()

    def get_res(self):
        return self.tmp

def captcha_handler(captcha):

    url = captcha.get_url()

    urllib.request.urlretrieve(url,"captcha.jpg")

    k = App()

    return captcha.try_again(k.get_res())




def tactics_action(session=None):
    print("[proxies] : %s"  % (session.http.proxies['http']))

    data = session.get_action()
    arr_pd = [post_id for post_id in data['message_post'].keys()]


    vk = vk_session.get_api()


    for val in arr_pd:

        for j in range(0, len(data['message_post'][val])):

            try:
                vk.wall.post(owner_id=val, message=data['message_post'][val][j], v='5.8')
                print("[POST] group_id : %s user_id %s" % (val, data['proxy']))
                time.sleep(random.randint(4, 9))
            except:
                print("[POST ERROR] group_id : %s" % (val))
                time.sleep(random.randint(3,4))

        time.sleep(20)

        try:
            post_id = vk.wall.get(owner_id=val,offset=0, count=90, v='5.8')
            for elem in vk.friends.areFriends(user_ids = list(map(lambda elem: elem['from_id'], post_id['items'])),need_sign=0, v='5.8'):
                if elem['friend_status'] == 0:
                    vk.friends.add(user_id=elem['user_id'],v='5.8')
                    print("[FRIEND ADD] id : %s " % (x))
                    time.sleep(1)
        except:
            pass

        time.sleep(random.randint(5,10))

        try:
            arrDel = vk.friends.getRequests(offset=0, count=20, extended=0,out=0, need_mutual=0,sort=0, v='5.8')
            for x in arrDel['items']:
                vk.friends.add(user_id=x,v='5.8')
                print("[FRIEND FIND] id : %s " % (x))
                time.sleep(4)

        except:
            pass

        time.sleep(random.randint(2,6))



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='rave vk script')
    parser.add_argument('-d', "--data", type=str,default='resources/data.json')
    parser.add_argument('-tf', "--time_fr", type=int, default=10)
    parser.add_argument('-td', "--time_ad", type=int, default=10)
    parser.add_argument('-r', "--repeat", type=int, default=3)
    parser.add_argument('-s', "--sign", type=int, default=0)
    args = parser.parse_args()
    print(banner)


    arr_procs = list()
    with open(args.data, 'r') as f: datastore = json.load(f)

    for i in range(0, args.repeat):

        for i in datastore.keys():
            login, password, token, app_id = i, datastore[i]['password'], datastore[i]['token'], datastore[i]["app_id"]

            vk_session = VkApi(login=login, password=password,
                                            token=token, app_id=app_id,
                                            captcha_handler=captcha_handler, data_action=datastore[str(i)])


            try:
                vk_session.auth(token_only=True)
            except:
                print("[error] : auth login")


            proc = multiprocessing.Process(target=tactics_action, args=(vk_session,))
            proc.start()
            print('[started]')
            arr_procs.append(proc)

            try:
                os.remove("vk_config.v2.json")
                print("[cookies] vk_config.v2.json was delete")
            except:
                pass
        for i in arr_procs:
            i.join()
