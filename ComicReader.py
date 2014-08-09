#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright 2013 zRoer
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
#   Author  :   zRoer
#   E-mail  :   hellozRoer@gmail.com
#   Date    :   13/08/13 15:30:00
#
import os
import Image
import ImageTk
import Tkinter 
import ConfigParser
import Config

def GetPicL(pdir):   #读取图片文件列表
    _pics=[]
    for parent,dirnames,filenames in os.walk(pdir):
        for filename in filenames:
            _pics.append(os.path.join(parent,filename)) #保存PIC路径信息到列表
          #  print os.path.join(parent,filename)        #DEBUG
    return _pics

def Resize(w, h, w_box, h_box, pil_image):  #缩放图片
    f1 = 1.0*w_box/w
    f2 = 1.0*h_box/h
    factor = min([f1, f2])
    width = int(w*factor)
    height = int(h*factor)
    return pil_image.resize((width, height), Image.ANTIALIAS)

def ShowPic(value):  #显示图片
    global postion
    if(value==1):
	    if(postion>0):
		    postion=postion-1
    if(value==2):
	    if(postion<len(pics)-1):
		    postion=postion+1
    pil_image = Image.open(pics[postion])  #按游标打开文件
    w, h = pil_image.size                  #取得文件像素大小
    pil_image_resized = Resize(w, h, w_box, h_box, pil_image) #按显示区域比例缩放，返回缩放后图片
    tk_img = ImageTk.PhotoImage(pil_image_resized)     #缩放后文件，转化为ImageTk
    imglabel.configure(image = tk_img)                 #这是label类型为 tk-img类型image
    imglabel.image = tk_img                             #设置label显示的图片

    title['text']  = pics[postion]                   #设置图片标题
    title.pack(fill = "x",expand = 1)

    print pics[postion]
    cf.set("global", "lp",postion)
    cf.write(open("conf.ini", "w"))
    return True
def Repos(value):
	global postion
	postion = value
	ShowPic(2)

# def debug(value):
#     if(value is 1):
#         print "l"
#     else:
#         print 'r'

if __name__ == '__main__':

    MainForm = Tkinter.Tk()       #创建主窗体
    MainForm.title("漫画浏览器")  #窗体标题
  
    """读配置文件"""
    rdir  = Config.rdir        	   #图片根目录，限制图片<=3层
    w_box = Config.w               #图片显示大小
    h_box = Config.h

    cf = ConfigParser.ConfigParser()
    base=os.path.split(os.path.realpath(__file__))[0]   #获取本文件路径 方法1，推荐
   # base = os.getcwd()#RUN IN IDLE                       #获取本文件路径 方法2，IDLE中使用
    conf_path = os.path.join(base,"conf.ini")
    cf.read(conf_path)
    postion = cf.getint("global","lp")
    print "index is :",
    print  postion+1
    
    '''读配置文件 结束'''
    pics = []                 #PIC文件路径列表
    pics = GetPicL(rdir)        #获取PIC文件路径列表
    pics.sort(key = lambda x:int(filter(str.isdigit,os.path.basename(x)))) #按文件名末尾数字排序
    
    ''' 标题'''
    title = Tkinter.Label(MainForm, text="",fg='blue' , bg='gray',font='Helvetica -18 bold')
    title.pack(fill = "x",expand=1)

    ''' 按钮'''
    button = Tkinter.Button(MainForm, text='第一张', command= lambda :Repos(-1))
    button.pack(side='top')

    p_button = Tkinter.Button(MainForm, text='前一张', command= lambda :ShowPic(1))
    p_button.pack(side='left')
    
    n_button = Tkinter.Button(MainForm, text='后一张', command= lambda :ShowPic(2))
    n_button.pack(side='right')

    ''' 图框'''
    imglabel = Tkinter.Label(MainForm, image="", width=w_box, height=h_box)
    imglabel.pack(padx=15, pady=15)
    
    '''按键事件绑定'''
    MainForm.bind('<Left>', lambda x:ShowPic(1))
    MainForm.bind('<Right>',lambda x:ShowPic(2))
   
    ShowPic(1)   
    MainForm.mainloop()
