# -*- coding: utf-8 -*-
import tkinter
from tkinter import font
import tkinter.messagebox
import sys
from socket import *
import login
recv_info = ''
class Ui_ReGist(object):
    def tcp_start(self):
        address = '127.0.0.1'
        port = 6337
        self.buffsize = 1024
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.connect((address, port))

    def regist_recv(self):
        global recv_info
        recv_info = self.s.recv(self.buffsize).decode('utf-8')
        print(recv_info)
        if str(recv_info) == 'true':
            tkinter.messagebox.showwarning(title='成功', message="注册成功！")
            # login_ui.hide()
            # QQmain_ui.show()
            # ui1.label.setText(self.user)
        elif str(recv_info) == 'same-user':
            tkinter.messagebox.showwarning(title='失败', message="用户名相同，请重新注册")

    def regist_recvs(self, n1, n2, n3):
        login_info = ['regist']
        self.user = n1
        password = n2
        npassword = n3
        user_l = len(str(self.user))
        if self.user == '':
            tkinter.messagebox.showwarning(title='警告', message="用户名不能为空")
        elif user_l < 5 or user_l > 10:
            tkinter.messagebox.showwarning(title='警告', message="用户名长度错误")
        elif password != npassword:
            tkinter.messagebox.showwarning(title='警告', message="两次密码不同")
        else:
            if password == '':
                tkinter.messagebox.showwarning(title='警告', message="密码不能为空")
            else:
                login_info.append(self.user)
                login_info.append(password)
                print(login_info)
                print(str(login_info))
                # login_info = '$%'.join(str(login_info))
                # print(login_info)
                self.s.send(str(login_info).encode())
                self.regist_recv()

    def resgin(self):
        reg = tkinter.Tk()
        reg.title("注册")
        reg.geometry("300x200+500+200")
        n1 = tkinter.StringVar()
        n2 = tkinter.StringVar()
        n3 = tkinter.StringVar()
        frm = tkinter.Frame(reg)
        frm.grid(padx='10', pady='10')
        frm_top = tkinter.Frame(frm)
        frm_top.grid(row=0, column=0, padx='20', pady='10')
        frm_down = tkinter.Frame(frm)
        frm_down.grid(row=1, column=0, padx='20', pady='10')
        label1 = tkinter.Label(frm_top, text="用户名")
        label2 = tkinter.Label(frm_top, text="密码")
        label3 = tkinter.Label(frm_top, text="再次输入密码")
        e1 = tkinter.Entry(frm_top, width=20, textvariable=n1)
        e1.grid(row=0, column=3, ipadx='2', ipady='2')
        e2 = tkinter.Entry(frm_top, width=20, textvariable=n2, show='*')
        e2.grid(row=1, column=3, ipadx='2', ipady='2')
        e3 = tkinter.Entry(frm_top, width=20, textvariable=n3, show='*')
        e3.grid(row=2, column=3, ipadx='2', ipady='2')
        label1.grid(row=0, column=0, ipadx='2', ipady='2')
        label2.grid(row=1, column=0, ipadx='2', ipady='2')
        label3.grid(row=2, column=0, ipadx='2', ipady='2')

        def error():
            global recv_info
            self.regist_recvs(n1.get(), n2.get(), n3.get())
            if recv_info == 'true':
                reg.destroy()
                log = login.Ui_MainWindow()
                log.tcp_start()
                log.login()
        c = tkinter.Button(frm_down, text="注册", width=10, height=1, command=error)
        c.grid(row=0, column=1, ipadx='2', ipady='2')
        reg.mainloop()


