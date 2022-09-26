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