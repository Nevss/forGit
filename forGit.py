import requests
from config import user, keyword, whitelist, email, rec, CC
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


def send(email, rec, words, CC):

    receivers = rec + CC

    subject = 'Git泄露监控'

    words = words

    msg = MIMEMultipart()

    msg['Subject'] = Header(subject, 'utf-8')

    msg['from'] = email['username']

    msg['CC'] = "%s\r\n".join(CC)

    msg['to'] = rec

    msg.attach(MIMEText(words, 'plain', 'utf-8'))

    smtp = smtplib.SMTP()

    smtp.connect('smtp.exmail.qq.com')

    smtp.login(email['username'], email['password'])

    print(email['username'])
    print(receivers)
    print(words)
    smtp.sendmail(email['username'], receivers, msg.as_string())

    smtp.quit()


class Begin:

    def __init__(self, session, result):

        self.session = session
        self.result = result

    ''' def login(self):

        url = 'https://api.github.com/user'

        res = self.session.get(url, auth=user)

        if res.status_code == 200:
            print('login sucsess!')'''

    def spider(self):
        for i in keyword:
            url = 'https://api.github.com/search/code?q='+i
            res = self.session.get(url, auth=user)
            tojson = json.loads(res.content.decode('utf8'))
            if 'items' in tojson:
                for i in tojson['items']:
                    if i['sha'] not in whitelist:
                        self.result.append({'name': i['name'],
                                            'html_url': i['html_url'],
                                            'owner': i['repository']['owner']['login'],
                                            'sha': i['sha']
                                            })


def main():

    result = []
    session = requests.session()
    se = Begin(session, result)
    Begin.spider(se)
    session.close()
    fina = ''
    for i in result:
        fina = fina+'文件名称：'+i['name']+'\n文件链接：'+i['html_url']+'\ngit所属者：'+i['owner']+'\nsha:'+i['sha']+'\n\n'

    if fina:
        send(email, rec, str(fina), CC)


main()
