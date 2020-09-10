#!/usr/bin/python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import pprint
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# подключение к сайту
url = "https://www.toramp.com/schedule.php?id=3109"

session = requests.Session()
resp = session.get(url, data={})
# проверяем код ответа
if resp.status_code != 200:
    print("Ошибка при чтении страницы. Код ответа HTTP - " + resp.status_code)
    exit(1)

# парсинг страницы
bsObj = BeautifulSoup(resp.text, "html.parser")
data = bsObj.find("div", {"class": "main-episodes-info"})
episodes = []
airdates = []
info = {}
output = ''

# парсим номера эпизодов
for div in bsObj.findAll('td', attrs={'class': 'number-of-episodes'}):
    episodes.append(div.text)

# парсим даты выхода серий
for div in bsObj.findAll('td', attrs={'class': 'air-date'}):
    airdates.append(div.text)

# собираем данные воедино
info = {episodes[i]: airdates[i] for i in range(len(episodes))}
# подготавливаем для вывода
output = pprint.pformat(info)

# отправляем почту
FROM = 'mailtestsenderr@gmail.com'
TO = ["cogano6457@inxto.net"]
SUBJECT = "Hello!"
mypass = 'ouYyIIIy21&o'
msg = MIMEMultipart()
msg['From'] = FROM
msg['To'] = TO
msg['Subject'] = "Привет!"
body = output
msg.attach(MIMEText(body, 'plain'))
server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.login(FROM, mypass)

message = 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(FROM,
                                                       TO,
                                                       SUBJECT,
                                                       body)


server.sendmail(FROM, TO, message.encode('utf-8'))
server.quit()



