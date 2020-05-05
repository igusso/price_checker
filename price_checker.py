import requests
from bs4 import BeautifulSoup
import smtplib
import time
import os


#GENERAL
rakitic_url = 'https://www.futwiz.com/en/fifa20/player/ivan-rakitic/559'
busquets_url = 'https://www.futwiz.com/en/fifa20/player/sergio-busquets/416'
degea_url ='https://www.futwiz.com/en/fifa20/player/de-gea/418'

#83
tolliso_url = 'https://www.futwiz.com/en/fifa20/player/corentin-tolisso/772'
jorginho_url = 'https://www.futwiz.com/en/fifa20/player/jorginho/272'
sarabia_url ='https://www.futwiz.com/en/fifa20/player/pablo-sarabia/742'
guedes_url ='https://www.futwiz.com/en/fifa20/player/goncalo-guedes/777'
dzeko_url = 'https://www.futwiz.com/en/fifa20/player/edin-dzeko/668'


#85
burki_url = 'https://www.futwiz.com/en/fifa20/player/roman-burki/608'
lukaku_url = 'https://www.futwiz.com/en/fifa20/player/romelu-lukaku/610'
icardi_url = 'https://www.futwiz.com/en/fifa20/player/mauro-icardi/18318'
aspas_url ='https://www.futwiz.com/en/fifa20/player/iago-aspas/686'
koke_url = 'https://www.futwiz.com/en/fifa20/player/koke/613'


# MAX PRICES:
rakitic_max_price = 15000
dzeko_max_price = 1800
busquets_max_price = 35000
degea_max_price = 43000

def average_85():
    first = price_check(burki_url,0,'burki','average')
    second = price_check(lukaku_url,0,'lukaku','average')
    third = price_check(icardi_url,0,'icardi','average')
    fourth = price_check(aspas_url,0,'aspas','average')
    fifth =price_check(koke_url,0,'koke','average')
    average = (first+second+third+fourth+fifth)/5

    print('85 rated players average: {}'.format(average))

    if average < 6500:
        send_mail('85 rated players','https://www.futwiz.com/en/fifa20/players?order=bin&s=asc?page='
                                     '0&minrating=85&maxrating=85')
    if average > 9000:
        send_mail('85 rated players','https://www.futwiz.com/en/fifa20/players?order=bin&s=asc?page='
                                     '0&minrating=85&maxrating=85')


def average_83():
    first = price_check(dzeko_url,0,'dzeko','average')
    second = price_check(tolliso_url,0,'tolliso','average')
    third = price_check(jorginho_url,0,'jorginho','average')
    fourth = price_check(sarabia_url,0,'sarabia','average')
    fifth =price_check(guedes_url,0,'guedes','average')
    average = (first+second+third+fourth+fifth)/5

    print('83 rated players average: {}'.format(average))

    if average < 1900:
        send_mail('83 rated players','https://www.futwiz.com/en/fifa20/players?page=0&order=bin&s='
                                     'asc&minrating=83&maxrating=83')
    if average > 3000:
        send_mail('83 rated players','https://www.futwiz.com/en/fifa20/players?page=0&order=bin&s='
                                     'asc&minrating=83&maxrating=83')

def send_mail(player, link):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('your@mail', 'yourpassword')   #add your email and a password here
    subject = "{} price has reached your target".format(player)
    body = 'Check out the futwiz link:\n {}'.format(link)
    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(
        'email',   #email from which you want an email to be send
        'email',     #receiver
        msg
    )
    print("{} price target has been reached".format(player))
    server.quit()


def price_check(URL, max_price, player,task):
    digits_list = []

    header = {"User-Agent": 'YOUR USER AGENT'}  #add your user agent here

    page = requests.get(URL, headers=header)
    soup = BeautifulSoup(page.content, 'html.parser')
    soup.prettify()
    prices = (soup.find_all("div", {"class": "playerprofile-price"}))
    price = prices[1].get_text()

    for x in price:
        if x != ',':
            digits_list.append(x)

    converted_price = int(''.join(digits_list))
    if task == 'max':
        print(player, ": ", converted_price, "| Lower limit: ", max_price)
        if converted_price <= max_price:
            send_mail(player, URL)
    if task == 'min':
        print(player, ": ", converted_price, "| Upper limit: ", max_price)
        if converted_price >= max_price:
            send_mail(player, URL)
    else:
        return converted_price




input()
while True:

    up_time = 300  #number of senconds between updates
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print("Last Update: ",current_time)
    price_check(rakitic_url, rakitic_max_price, 'Rakitic','max')
    time.sleep(2)
    price_check(dzeko_url, dzeko_max_price, 'Dzeko','max')
    time.sleep(1)
    price_check(busquets_url, busquets_max_price, 'Busquets','max')
    time.sleep(1)
    price_check(degea_url, degea_max_price, 'De Gea','min')
    time.sleep(1)
    average_83()
    time.sleep(1)
    average_85()

    print("---------------------------------------------")
    for x in range(0, up_time):
        b = "Next update in {} seconds".format(up_time)
        print(b, end="\r")
        time.sleep(1)
        up_time -=1
    clear = lambda: os.system('cls')
    clear()





