#-*-coding:utf-8-*-

from socket import *
import threading
import re
import pymssql


address='127.0.0.1'
port=6337
buffsize=1024
s = socket(AF_INET, SOCK_STREAM)
s.bind((address,port))
s.listen(10)     #最大连接数

client_list=[] # 已登录的用户

# user_list=[[2097557613, 123456], [2097557614, 123456], [2097557615, 123456], [2097557616, 123456], [2097557617,123456],[2097557618,123456]]
user_list=[]
user_l=0
user_client=[]
user_friend={}
group_list=[['信息论群'], ['微机原理群'], ['通信电子线路群'], ['通信原理群']]
class MSSQL:
    def __init__(self, host, user, pwd, db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):
        """
        得到连接信息
        返回: conn.cursor()
        """
        if not self.db:
            raise (NameError, "没有设置数据库信息")
        self.conn = pymssql.connect(host=self.host, user=self.user, password=self.pwd, database=self.db, charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "连接数据库失败")
        else:
            return cur

    def ExecQuery(self, sql):
        """
        执行查询语句
        返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段

        """
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        # 查询完毕后必须关闭连接
        self.conn.close()
        return resList

    def ExecNonQuery(self, sql):
        """
        执行非查询语句

        调用示例：
            cur = self.__GetConnect()
            cur.execute(sql)
            self.conn.commit()
            self.conn.close()
        """
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()

def uinit():#读入数据库的数据初始化user字典
    global user_l
    ms = MSSQL(host="localhost:1433", user="sa", pwd="ajx123456", db="QQ")
    resList = ms.ExecQuery("SELECT * FROM users")
    for i in range(len(resList)):
        if resList[i][1] != ' ':
            user_list.append(list(resList[i][0:2]))
    print(user_list)
    user_l = len(user_list)
def getfriend():
    ms = MSSQL(host="localhost:1433", user="sa", pwd="ajx123456", db="QQ")
    for y in range(0, user_l):
        resList = ms.ExecQuery("SELECT friend FROM users where name=" + '\'' + user_list + '\'' + "and password=none" )
    print(resList)
def rmall(aa,e):#aa 待处理列表，e是删除的元素
    cnt=0
    for ee in aa:
        if e==ee:
            cnt+=1     #统计元素e出现的次数
    for i in range(cnt):
        aa.remove(e)     #调用cnt次remove函数，将元素e都删除掉。
    return aa

def login(logindata, clientsock):
    uinit()
    for x in range(0,user_l):
        print("登录请求"+str(logindata[1]))
        if len(user_client)>=1:
            ul=len(user_client)
            if str(user_list[x][0])==str(logindata[1]) and str(user_list[x][1])!=str(logindata[2]):#账号正确，密码错误
                login_bkinfo = 'false-pw'
                clientsock.send(login_bkinfo.encode())
                break
            elif str(user_list[x][0])==str(logindata[1]) and str(user_list[x][1])==str(logindata[2]):
                for user_cl in range(0, ul):
                    if str(user_client[user_cl][0]) == str(logindata[1]):
                        login_bkinfo = 'false-login'
                        clientsock.send(login_bkinfo.encode())
                        break
                    elif user_cl == ul - 1:
                        usercl=[]
                        usercl.append(logindata[1])
                        usercl.append(clientsock)
                        login_bkinfo = 'true'
                        user_client.append(usercl)
                        print("*******")
                        print(user_client)
                        print("*********")
                        clientsock.send(login_bkinfo.encode())
                break
            elif x==user_l-1:#账号错误
                login_bkinfo = 'false-user'
                clientsock.send(login_bkinfo.encode())

        else:
            if str(user_list[x][0])==str(logindata[1]) and str(user_list[x][1])!=str(logindata[2]):
                login_bkinfo = 'false-pw'
                clientsock.send(login_bkinfo.encode())
                break
            elif str(user_list[x][0])==str(logindata[1]) and str(user_list[x][1])==str(logindata[2]):
                usercl=[]
                usercl.append(logindata[1])
                usercl.append(clientsock)
                login_bkinfo = 'true'
                user_client.append(usercl)
                print(user_client[0][1])

                clientsock.send(login_bkinfo.encode())
                break
            elif x==user_l-1:
                login_bkinfo = 'false-user'
                clientsock.send(login_bkinfo.encode())

def resgin(logindata, clientsock):
    #sleep(5)
    uinit()
    for x in range(0,user_l):
        print("注册请求"+str(logindata[1]))
        if str(logindata[1]) in user_list[x][0]:#相同的账号
            login_bkinfo = 'same-user'
            clientsock.send(login_bkinfo.encode())
            break
    if x == user_l-1:
        login_bkinfo = 'true'
        ms = MSSQL(host="localhost:1433", user="sa", pwd="ajx123456", db="QQ")
        ms.ExecNonQuery(
            "insert into users values(" + "\'" + logindata[1] + "\'" + "," + "\'" + logindata[2] + "\'" + "," + "\'" + ' ' + "\'" ")")
        clientsock.send(login_bkinfo.encode())

def add_fri(logindata, clientsock):
    uinit()
    user_clients = []
    user_lists = []
    for y in range(len(user_client)):
        user_clients.append(user_client[y][0])
    for y in range(0,user_l):
        user_lists.append(user_list[y][0])
    print(user_lists)
    print(logindata[2])
    print(logindata[1])
    if str(logindata[2]) in user_lists and str(logindata[1]) in user_lists:
        if str(logindata[2]) not in user_clients:
            login_bkinfo = 'empty'
            clientsock.send(login_bkinfo.encode())
        else:
            login_bkinfo = 'true'
            ms = MSSQL(host="localhost:1433", user="sa", pwd="ajx123456", db="QQ")
            ms.ExecNonQuery(
                "insert into users values(" + "\'" + logindata[1] + "\'" + "," + "\'" + ' ' + "\'" + "," + "\'" + logindata[2] + "\'" + ")")
            clientsock.send(login_bkinfo.encode())
            login_bkinfo = 'addfr'
            for x in (len(user_client)):
                if logindata[2] == user_client[x][0]:
                    user_client[x][1].send(login_bkinfo.encode())
    else:
        login_bkinfo = 'false-friuser'
        clientsock.send(login_bkinfo.encode())

def tcplink(clientsock, clientaddress):
    group_l = len(group_list)
    while True:
        recvdata = clientsock.recv(buffsize).decode('utf-8')
        recvdata_list = list(recvdata)
        recvdata_list = rmall(recvdata_list, '[')
        recvdata_list = rmall(recvdata_list, ']')
        recvdata_list = rmall(recvdata_list, ',')
        recvdata_list = rmall(recvdata_list, ' ')
        re1 = [s.split() for s in ''.join(recvdata_list).split('\'') if s]
        recvdata_list = []
        for i in range(len(re1)):
            a1 = ''.join(re1[i])
            recvdata_list.append(a1)
        #print(recvdata_list[0])
        #print(type(recvdata))
        if str(recvdata_list[0]) == 'login':  # 处理登录消息
            login(recvdata_list, clientsock)
        elif str(recvdata_list[0]) == 'regist':  # 处理登录消息
            resgin(recvdata_list, clientsock)
        elif str(recvdata_list[0]) == 'friend':  # 处理添加好友
            add_fri(recvdata_list, clientsock)
        elif str(recvdata_list[0]) == 'wechat_req':  # 处理群聊消息
            for y in range(0, group_l):
                if str(group_list[y][0]) == str(recvdata_list[1]):
                    requser = str(recvdata_list[2]) + ' ' + '加入群聊'
                    group_list[y].append(clientsock)
                    # print('my clientsock is : ' + str(clientsock))
                    print(group_list[y])
                    groupl = len(group_list[y])
                    print(groupl)
                    if True:                                            #  groupl>2
                        for h in range(1, groupl):
                            group_list[y][h].send(requser.encode())
                    break
        elif str(recvdata_list[0]) == 'wechat_quit':  # 处理群聊消息
            for y in range(0, group_l):
                if str(group_list[y][0]) == str(recvdata_list[1]):
                    requser = str(recvdata_list[2]) + ' ' + '退出群聊'
                    group_list[y].remove(clientsock)
                    print(group_list[y])
                    groupl = len(group_list[y])
                    if True:
                        for h in range(1, groupl):
                            group_list[y][h].send(requser.encode())
                    else:
                        clientsock.send(requser.encode())
                    break
        elif str(recvdata_list[0]) == 'wechat':
            for wl in range(0, group_l):
                if str(group_list[wl][0]) == str(recvdata_list[1]):  ###
                    senddata=str(recvdata_list[2])+":"+str(recvdata_list[3])
                    l = len(group_list[wl])
                    try:
                        if l >= 2:
                            for x in range(1, l):
                                group_list[wl][x].send(senddata.encode())
                        else:
                            clientsock.send(senddata.encode())
                            break
                        print("群聊信息" + str(senddata)+str(clientaddress))
                    except ValueError:
                        break
        elif str(recvdata_list[0]) == 'personal':   # 处理私聊消息
            user_cl = len(user_client)
            send_info = str(recvdata_list[1])+":"+str(recvdata_list[3])
            z = 1
            for pl in range(0, user_cl):
                if user_client[pl][0]==recvdata_list[2]:
                    for ql in range(0, user_cl):
                        if user_client[ql][0] == recvdata_list[1]:
                            user_client[ql][1].send(send_info.encode())
                    user_client[pl][1].send(send_info.encode())
                    print(clientaddress)
                    break
                elif z == user_cl:
                    back = str(recvdata_list[2])+'不在线'
                    backtext = 'personal$%'+recvdata_list[1]+'$%'+recvdata_list[2]+'$%'+back
                    print('sendback text is: ' + backtext)
                    clientsock.send(back.encode())
                z = z + 1
        elif str(recvdata_list[0]) == 'voicechat':   # 处理语音聊天消息
            length = len(recvdata_list)
            if str(recvdata_list[length-2]) == 'end':
                user_cl = len(user_client)  # list[1] sender  list[2] receiver
                # send_info = str(recvdata_list[1])+":"+str(recvdata_list[3])
                length = len(recvdata_list)
                z = 1
                for pl in range(0, user_cl):
                    if user_client[pl][0] == recvdata_list[2]:
                        p1 = re.compile(r'[(](.*?)[)]', re.S)  # 正则表达式提取客户端的地址
                        list1 = re.findall(p1, str(user_client[pl][1]))
                        list2 = list1[1].split(',')
                        result = ''.join(list2)
                        result = result + '$%' + 'ignore' +'$%'+'voicechat_accept'  # 发送给发起方
                        print(list2)

                        for ql in range(0, user_cl):
                            if user_client[ql][0] == recvdata_list[1]:
                                p1 = re.compile(r'[(](.*?)[)]', re.S)  # 正则表达式提取客户端的地址
                                list1 = re.findall(p1, str(user_client[ql][1]))
                                list2 = list1[1].split(',')
                                send_info = ''.join(list2)
                                if recvdata_list[length - 2] == 'end':
                                    send_info = ''.join('end')
                                send_info = send_info + '$%' + 'voicechat_request'  # 发送给接收方
                                print('send_info is:' + send_info)
                                user_client[pl][1].send(send_info.encode())
                                # user_client[ql][1].send(result.encode())
                        print(clientaddress)

                        break
                    elif z == user_cl:
                        back = str(recvdata_list[2]) + '不在线'
                        clientsock.send(back.encode())
                    z = z + 1
            else:
                user_cl = len(user_client)         # list[1] sender  list[2] receiver
                # send_info = str(recvdata_list[1])+":"+str(recvdata_list[3])
                length = len(recvdata_list)
                z = 1
                for pl in range(0, user_cl):
                    if user_client[pl][0] == recvdata_list[2]:
                        p1 = re.compile(r'[(](.*?)[)]', re.S)  # 正则表达式提取客户端的地址
                        list1 = re.findall(p1, str(user_client[pl][1]))
                        list2 = list1[1].split(',')
                        result = ''.join(list2)
                        result = result + '$%' + 'voicechat_accept'  # 发送给发起方
                        print(list2)

                        for ql in range(0, user_cl):
                            if user_client[ql][0] == recvdata_list[1]:
                                p1 = re.compile(r'[(](.*?)[)]', re.S)  # 正则表达式提取客户端的地址
                                list1 = re.findall(p1, str(user_client[ql][1]))
                                list2 = list1[1].split(',')
                                send_info = ''.join(list2)
                                if recvdata_list[length-2] == 'end':
                                    send_info = ''.join('end')
                                send_info = send_info + '$%' + 'voicechat_request'   # 发送给接收方
                                print('send_info is:' + send_info)
                                user_client[pl][1].send(send_info.encode())
                                user_client[ql][1].send(result.encode())
                        print(clientaddress)

                        break
                    elif z == user_cl:
                        back = str(recvdata_list[2])+'不在线'
                        clientsock.send(back.encode())
                    z = z + 1
        elif str(recvdata_list[0]) == 'filesend':   # 处理文件传输
            user_cl = len(user_client)  # list[1] sender  list[2] receiver
            # send_info = str(recvdata_list[1])+":"+str(recvdata_list[3])
            z = 1
            for pl in range(0, user_cl):
                if user_client[pl][0] == recvdata_list[2]:
                    p1 = re.compile(r'[(](.*?)[)]', re.S)  # 正则表达式提取客户端的地址
                    list1 = re.findall(p1, str(user_client[pl][1]))
                    list2 = list1[1].split(',')
                    result = ''.join(list2)
                    result = result + '$%' + 'filesend_accept'
                    print(list2)

                    for ql in range(0, user_cl):
                        if user_client[ql][0] == recvdata_list[1]:
                            p1 = re.compile(r'[(](.*?)[)]', re.S)  # 正则表达式提取客户端的地址
                            list1 = re.findall(p1, str(user_client[ql][1]))
                            list2 = list1[1].split(',')
                            send_info = ''.join(list2)
                            send_info = send_info + '$%' + 'filesend_request'
                            print('send_info is:' + send_info)
                            user_client[pl][1].send(send_info.encode())
                            user_client[ql][1].send(result.encode())
                    print(clientaddress)

                    break
                elif z == user_cl:
                    back = str(recvdata_list[2]) + '不在线'
                    clientsock.send(back.encode())
                z = z + 1
        elif str(recvdata_list[0]) == '':
            print('无法识别：')
            print(recvdata_list[0])
            break

    clientsock.close()
    del client_list[-1]



while True:
    clientsock, clientaddress = s.accept()
    client_list.append(clientsock)
    print('connect from:', clientaddress)   # clientaddress 包含IP与端口
    t = threading.Thread(target=tcplink, args=(clientsock,clientaddress))  #新创建的线程
    t.start()
# s.close()



