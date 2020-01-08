#!/usr/bin/python3
# coding  : utf-8
# @Author : Labyrinthine Leo
# @Time   : 2020.01.08

import os
from urllib.request import urlretrieve
# 使用selenium爬取动态网页
from selenium import webdriver
# 图形开发界面库
from tkinter import *

# 爬虫功能函数
# https://music.163.com/#/search/m/?s=%E7%BB%BF%E8%89%B2&type=1
# http://music.163.com/song/media/outer/url?id={}.mp3
# http://music.163.com/mv/media/outer/url?id={}.mp4
# https://music.163.com/#/outchain/2/{}/

# 获取歌曲信息
def get_song_info():
    name = entry.get()
    url = 'https://music.163.com/#/search/m/?s={}&type=1'.format(name)
    # 隐藏浏览器
    option = webdriver.FirefoxOptions()
    option.add_argument('--headless')
    driver = webdriver.Firefox(firefox_options=option)
    driver.get(url=url),

    # 使用xpath进行查找信息结点
    driver.switch_to.frame('g_iframe')  # 获取iframe标签
    req = driver.find_element_by_id('m-search') # 找到id为"m-search"的div
    # 获取歌曲链接
    a_id = req.find_element_by_xpath('.//div[@class="item f-cb h-flag  "]/div[2]//a').get_attribute('href')
    # print(a_id)
    # 获取歌曲id
    song_id = a_id.split("=")[-1]
    # print(song_id)
    # 获取歌曲名字
    song_name = req.find_element_by_xpath('.//div[@class="item f-cb h-flag  "]/div[2]//b').get_attribute('title')
    print(song_name)

    item = {}
    item['song_id'] = song_id
    item['song_name'] = song_name

    download_song(item)


def download_song(item):
    song_id = item['song_id']
    song_name = item['song_name']
    song_url = "http://music.163.com/song/media/outer/url?id={}.mp3".format(song_id)
    # 创建文件夹
    os.makedirs('NEC_musics', exist_ok=True) # 存在则不新建
    path = 'NEC_musics\{}.mp3'.format(song_name)
    # 文本框
    text.insert(END, '歌曲：《{}》 正在下载...'.format(song_name))
    # 文本框滚动
    text.see(END)
    # 更新
    text.update()
    # 下载
    urlretrieve(song_url, path)
    # 文本框
    text.insert(END, '歌曲：《{}》下载完成，请试听...'.format(song_name))
    # 文本框滚动
    text.see(END)
    # 更新
    text.update()

# # 创建UI界面函数
# def plotUI():

# 创建底层面板类
root = Tk()
# 添加标题
root.title('Music downloader')
# 设置窗口大小
root.geometry('500x420')
# 标签控件
label = Label(root, text="Input to download Music: ", font=('宋体', 14))
# 标签定位
label.grid()  #默认 row=0, col=0
# 输入框
entry = Entry(root)
entry.grid(row=0, column=1)
# 列表框
text = Listbox(root, width=50, heigh=15)
text.grid(row=1,columnspan=2)
# 开始下载按钮
dl_botton = Button(root, text="下载歌曲", font=("华文正楷", 14), command=get_song_info)
dl_botton.grid(row=2, column=0, sticky=W)
# 退出按钮
# 注意quit和quit()的区别
quit_botton = Button(root, text="退出程序", font=("华文正楷", 14), command=root.quit)
quit_botton.grid(row=2, column=1, sticky=E)

#显示界面
root.mainloop()
