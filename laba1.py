from bs4 import BeautifulSoup
import csv
import requests

url = "https://www.gismeteo.ru/diary/4618/2008/1/"
year = 2008

MaxYear = year  # нахождение максимального года
linktmp = url
f = 0
while f == 0:
    html_text = requests.get(linktmp, headers={"User-Agent": "Windows 10"}).text
    parse = BeautifulSoup(html_text, "lxml")
    errorelement = parse.find("div", class_="grey digit")
    if errorelement:
        f = 1
        MaxYear -= 1

    else:
        MaxYear += 1
        linktmp = linktmp.replace(str(MaxYear - 1), str(MaxYear))

linktmp = linktmp.replace(str(MaxYear + 1), str(MaxYear))

# замена года в ссылке
def years_change(year, url):
    url = url.replace(str(year - 1), str(year))
    return url

def days_redact(output):
    if (int(output[0]) < 10):
        return ('0' + output[0])

    else:
        return (output[0])


def months_redact(month):
    if (month < 10):
        return ('0' + str(month))

    else:
        return (str(month))

# нахождение максимального месяца
def month_chek(url):
    month = 1
    f = 0
    while f == 0:
        html_text = requests.get(url, headers={"User-Agent": "Windows 10"}).text
        parse = BeautifulSoup(html_text, "lxml")
        errorelement = parse.find("div", class_="grey digit")

        if errorelement:
            f = 1
            month -= 1
        else:
            month += 1
            url = url[0:39] + "/" + str(month) + "/"
    return month


def months_change(url:str, month, flag):
    """замена месяца в ссылке"""
    if flag == 2:
        url = url[0:39] + "/1/"
    elif flag == 1:
        url = url[0:39] + "/" + str(month) + "/"
    return url


MMonth = month_chek(linktmp)  # запись максимального месяца в Mmonth

for i in range(year, MaxYear + 1):
    url = years_change(i, url)
    max_month = 12
    if i == MaxYear:
        max_month = MMonth
    for j in range(1, max_month + 1):
        flag = 0
        if j == max_month:
            url = months_change(url, j, 1)
            flag = 1
        else:
            url = months_change(url, j, 1)

        html_text = requests.get(url, headers={"User-Agent": "Windows 10"}).text
        soup = BeautifulSoup(html_text, "lxml")
        rows = soup.find_all("tr", align="center")  # нахождение всех строк

        for k in range(len(rows)):
            data = rows[k].find_all("td")  # нахождение всех нужных значений
            MData = []
            numbers = [0, 1, 2, 5, 6, 7, 10]
            for v in numbers:
                MData.append(data[v].text)
            with open("dataset.csv", "a", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile, lineterminator='\n')
                writer.writerow(
                    (
                        str(i) + '-' + months_redact(j) + '-' + days_redact(MData),
                        MData[1],
                        MData[2],
                        MData[3],
                        MData[4],
                        MData[5],
                        MData[6],
                    )
                )
        if flag == 1:
            url = months_change(url, j, 2)
