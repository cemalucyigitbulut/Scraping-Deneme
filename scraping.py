import requests
from bs4 import BeautifulSoup
import pandas as pd

baseurl = 'https://neareasthospital.com/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'
}


r = requests.get('https://neareasthospital.com/doctors/?lang=en')
soup = BeautifulSoup(r.content, 'html.parser')

# adını yaptık class_ çünkü python classi olmadığı için böyle yazdık

doctorNames = soup.find_all('div', class_='card-staff__title')
doctorLinks = soup.find_all('div', class_='card-staff__head')
doctorDuty = soup.find_all('div', class_='card-staff__duty')
doctorNumber = soup.find_all('ul', class_='list is-unstyled is-horizontal card-staff__list')

doctorLinkList = []
doctorNamesList = []
doctorDutyList = []
doctorNumberList = []

for number in doctorNumber:
    lines = number.text.strip().split('\n')
    for line in lines:
        if '+' in line:
            doctorNumberList.append(line.strip())

for class_ in doctorLinks:
    for link in class_.find_all('a', href=True):
        doctorLinkList.append(link['href'])

for title in doctorNames:
    doctorNamesList.append(title.text.strip())

for duty in doctorDuty:
    doctorDutyList.append(duty.text.strip())

Doctors = {
    'Name': doctorNamesList,
    'Expertise':doctorDutyList,
    'Contact': doctorNumber,
    'Link': doctorLinkList
}

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

df = pd.DataFrame(Doctors)

try:
    # print(soup.find('div', class_='mariselle-title title is-size-4 is-title-underline is-text-center').text.strip())
    # decodedDoctorText = decodeEmail(doctorText)
    # print(decodedDoctorText)
    # print(doctorNamesList,doctorLinkList)
    print(df)
except UnicodeEncodeError:
    print('Cannot print some characters.')
