from smtplib import SMTP_SSL
from email.mime.text import MIMEText


def sendMail(message, Subject):
    try:
        '''
        :param message: str 邮件内容
        :param Subject: str 邮件主题描述
        :param sender_show: str 发件人显示，不起实际作用如："xxx"
        :param recipient_show: str 收件人显示，不起实际作用 多个收件人用','隔开如："xxx,xxxx"
        :param to_addrs: str 实际收件人
        :param cc_show: str 抄送人显示，不起实际作用，多个抄送人用','隔开如："xxx,xxxx"
        '''
        # 填写真实的发邮件服务器用户名、密码
        user = '2296685742@qq.com'
        password = 'tnkecpmzjkjrdifa'
        # 邮件内容
        msg = MIMEText(message, 'plain', _charset="utf-8")
        # 邮件主题描述
        msg["Subject"] = Subject
        # 发件人显示，不起实际作用
        # 实际发给的收件人
        to_addrs = 'u3565714@connect.hku.hk'
        msg["from"] = '2296685742@qq.com'
        # 收件人显示，不起实际作用
        msg["to"] = 'u3565714@connect.hku.hk'

        with SMTP_SSL(host="smtp.qq.com", port=465) as smtp:
            # 登录发邮件服务器
            smtp.login(user=user, password=password)
            # 实际发送、接收邮件配置
            l = smtp.sendmail(from_addr=user, to_addrs=to_addrs.split(','), msg=msg.as_string())
            print(f'send mail, result {l}')
    except Exception as e:
        print(f'send email error, {e}')


if __name__ == "__main__":
    message = 'Python 测试邮件...'
    Subject = '主题测试2_robot'
    sendMail(message, Subject)