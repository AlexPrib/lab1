from bs4 import BeautifulSoup
import csv
import requests

url = 'https://www.gismeteo.ru/diary/4618/2008/1/'
year = 2008

MaxYear = year #нахождение максимального года
linktmp = url
f = 0
while (f == 0):
      html_text = requests.get(linktmp,headers={'User-Agent':'Windows 10'}).text
      parse = BeautifulSoup(html_text, 'lxml')
      errorelement = parse.find('div', class_='grey digit')
      if errorelement:
        f = 1
        MaxYear -= 1

      else:
        MaxYear += 1
        linktmp = linktmp.replace(str(MaxYear - 1), str(MaxYear)) 

linktmp = linktmp.replace(str(MaxYear+1),str(MaxYear))

#замена года в ссылке
def years_change (year, url):
    url = url.replace(str(year - 1), str(year))
    return url

#нахождение максимального месяца
def month_chek (url):
    month = 1
    f = 0
    while (f == 0):
      html_text = requests.get(url,headers={'User-Agent':'Windows 10'}).text
      parse = BeautifulSoup(html_text, 'lxml')
      errorelement = parse.find('div', class_='grey digit')
      
      if errorelement:
        f = 1
        month -= 1
      else:
        month+= 1
        url = url[0:39] + '/' + str(month) + '/'
    return month

    #замена месяца в ссылке
def months_change(url , month , flag):
    if flag == 2:
        url = url[0:39] + '/1/'
    elif flag == 1:
        url = url[0:39] + '/' + str(month) + '/' 
    return url

MMonth = month_chek(linktmp)#запись максимального месяца в Mmonth