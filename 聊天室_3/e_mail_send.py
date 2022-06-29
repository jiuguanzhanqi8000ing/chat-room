import smtplib
from email.mime.text import MIMEText    #邮件正文
from email.header import Header #邮件头

def email_send():
    target = ['2765653453@qq.com',
              '2361980399@qq.com',
              '2315208844@qq.com']
    # 账号
    sender = '763586526@qq.com'  # 账号
    # 密码
    pwd = 'ogcfbekxrqzqbbcd'  # 密码

    # 邮件：发送人，接收人，主题，内容

    # 内容
    body = input("输入发送的内容:")
    # 转换成浏览器认识的
    msg = MIMEText(body, 'html')
    # 主题
    msg['subject'] = "咸武的信"
    # 发送人
    msg['from'] = Header("来自咸武的问候", 'utf-8')
    # 接收人
    msg['to'] = Header("有缘人", 'utf-8')

    # jashuloytyybbfjc
    smtp_obj = smtplib.SMTP_SSL("smtp.qq.com", 465)
    # 模拟登录
    smtp_obj.login(sender, pwd)
    smtp_obj.sendmail(sender, target, msg.as_string())  # 发送邮件
    print('发送成功!')

email_send()