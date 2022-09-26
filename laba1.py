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

for i in range(year, MaxYear+1):
    url = years_change(i, url)
    MaxMonth = 12
    if i == MaxYear:
        MaxMonth = MMonth
    for j in range (1, MaxMonth + 1):
        flag = 0
        if j == MaxMonth:
            url = months_change(url , j , 1)
            flag = 1
        else:
            url = months_change(url , j , 1)

        html_text = requests.get(url, headers={'User-Agent':'Windows 10'}).text
        soup = BeautifulSoup(html_text, 'lxml')
        rows = soup.find_all('tr', align = 'center')#нахождение всех строк 

        for i in range (len(rows)):
            data = rows[i].find_all('td')#нахождение всех нужных значений
            MData=[]
            numbers = [0,1,2,5,6,7,10]
            for i in numbers:
                MData.append(data[i].text)
            with open('dataset.csv','a',encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow((MData[0],MData[1],MData[2],MData[3],MData[4],MData[5],MData[6]))
        if flag == 1:
           url = months_change(url, j, 2)