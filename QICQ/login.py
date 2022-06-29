# -*- coding: utf-8 -*-
import tkinter
from tkinter import font
import tkinter.messagebox
import sys
from socket import *
import threading
import register
class Ui_MainWindow(object):
    def tcp_start(self):
        address = '127.0.0.1'
        port = 6337
        self.buffsize = 1024
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.connect((address, port))

    def getuser(self):
        return self.user

    def login_recv(self):
        recv_info = self.s.recv(self.buffsize).decode('utf-8')
        print(recv_info)
        if str(recv_info) == 'true':
            tkinter.messagebox.showwarning(title='登入成功！', message="登入成功！")
            #login_ui.hide()
            #QQmain_ui.show()
            #ui1.label.setText(self.user)
        elif str(recv_info) == 'false-user':
            tkinter.messagebox.showwarning(title='失败', message="登入失败，账号名错误！")
        elif str(recv_info) == 'false-pw':
            tkinter.messagebox.showwarning(title='失败', message="登入失败，密码错误！")
        elif str(recv_info) == 'false-login':
            tkinter.messagebox.showwarning(title='失败', message="此账号已经登录！")

    def login_recvs(self,n1,n2):
        login_info=['login']
        self.user = n1
        password = n2
        user_l = len(str(self.user))
        if self.user == '':
            tkinter.messagebox.showwarning(title='提示', message="用户名不能为空")
        elif user_l < 5 or user_l > 10:
            tkinter.messagebox.showwarning(title='提示', message="用户名长度错误")
        else:
            if password == '':
                tkinter.messagebox.showwarning(title='提示', message="密码不能为空")
            else:
                login_info.append(self.user)
                login_info.append(password)
                print(login_info)
                print(str(login_info))
                #login_info = '$%'.join(str(login_info))
                #print(login_info)
                self.s.send(str(login_info).encode())
                self.login_recv()
    def login(self):
        reg = tkinter.Tk()
        reg.title("登入")
        reg.geometry("250x150+500+200")
        n1 = tkinter.StringVar()
        n2 = tkinter.StringVar()
        frm = tkinter.Frame(reg)
        frm.grid(padx='10', pady='10')
        frm_top = tkinter.Frame(frm)
        frm_top.grid(row=0, column=0, padx='20', pady='10')
        frm_down = tkinter.Frame(frm)
        frm_down.grid(row=1, column=0, padx='20', pady='10')
        label1 = tkinter.Label(frm_top, text="用户名：")
        label2 = tkinter.Label(frm_top, text="密码：")
        e1 = tkinter.Entry(frm_top, width=20, textvariable=n1)
        e1.grid(row=0, column=3, ipadx='2', ipady='2')
        e2 = tkinter.Entry(frm_top, width=20, textvariable=n2, show='*')
        e2.grid(row=1, column=3, ipadx='2', ipady='2')
        label1.grid(row=0, column=0, ipadx='2', ipady='2')
        label2.grid(row=1, column=0, ipadx='2', ipady='2')
        def resgins():
            reg.destroy()
            res = register.Ui_ReGist()
            res.tcp_start()
            res.resgin()
        def sign():
            self.login_recvs(n1.get(),n2.get())
        b = tkinter.Button(frm_down, text="登录", width=10, height=1, command=sign)
        c = tkinter.Button(frm_down, text="注册", width=10, height=1, command=resgins)
        b.grid(row=0, column=0, ipadx='2', ipady='2')
        c.grid(row=0, column=1, ipadx='2', ipady='2')
        reg.mainloop()

class Ui_Dialog(object):
    def __init__(self,name):
        self.user = name
    def tcp_start(self):
        address = '127.0.0.1'
        port = 6337
        self.buffsize = 1024
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.connect((address, port))
    def friend_recv(self):
        recv_info = self.s.recv(self.buffsize).decode('utf-8')
        print(recv_info)
        if str(recv_info) == 'true':
            tkinter.messagebox.showwarning(title='成功发送好友请求', message="成功发送好友请求")
            #login_ui.hide()
            #QQmain_ui.show()
            #ui1.label.setText(self.user)
        elif str(recv_info) == 'false-friuser':
            tkinter.messagebox.showwarning(title='警告', message="查无此人")
        elif str(recv_info) == 'empty':
            tkinter.messagebox.showwarning(title='警告', message="您搜索的用户不在线，请稍后添加")
        if str(recv_info) == 'addfr':
            tkinter.messagebox.showwarning(title='好友请求', message="好友请求")
    def friend_recvs(self,n1):
        login_info=['friend']
        if self.user == n1:
            tkinter.messagebox.showwarning(title='警告', message="不能添加自己")
        else:
            login_info.append(self.user)
            login_info.append(n1)
            self.s.send(str(login_info).encode())
            self.friend_recv()
    def setupUi(self):
        fr = tkinter.Tk()
        n = tkinter.StringVar(fr)
        fr.title("添加好友")
        fr.geometry("250x100+620+320")
        id = tkinter.Label(fr, text="搜索用户名：")
        idnum = tkinter.Entry(fr, width=20, textvariable=n)
        def action(event):
            if event.keysym == 'Return':
                name = n.get()
                self.friend_recvs(name)
        fr.bind("<Return>", action)
        id.place(x=10, y=40)
        idnum.place(x=90, y=40)
        fr.mainloop()



if __name__ == "__main__":
    ui = Ui_MainWindow()        # 登录界面
    ui.tcp_start()
    ui.login()
    username = ui.getuser()
    ui1 = Ui_Dialog(username)
    ui1.tcp_start()
    ui1.setupUi()
    #print(username)
    #print('tcp connect!')




