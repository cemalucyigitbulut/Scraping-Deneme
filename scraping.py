import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
import locale
from tabulate import tabulate

# set console encoding to utf-8
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)
locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')

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
    link = number.find('a', href=True)
    if link:
        doctorNumberList.append(link['href'])

for class_ in doctorLinks:
    for link in class_.find_all('a', href=True):
        doctorLinkList.append(link['href'])

for title in doctorNames:
    doctorNamesList.append(title.text.strip())

for duty in doctorDuty:
    duty_text = duty.text.strip().replace('  ', ' ')
    doctorDutyList.append(duty_text)


Doctors = {
    'Name': doctorNamesList,
    'Expertise':doctorDutyList,
    'Contact': doctorNumberList,
    'Link': doctorLinkList
}

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)


df = pd.DataFrame(Doctors)

#texte yaz
# with open('doctors.txt','w',encoding='utf-8') as f:
#     for index ,row in df.iterrows():
#         f.write(f"{row['Name']}\n{row['Expertise']}\n{row['Contact']}\n{row['Link']}\n\n")

# df.to_csv('doctors.txt', sep='|', index=False, encoding='utf-8-sig')


try:
    # print(soup.find('div', class_='mariselle-title title is-size-4 is-title-underline is-text-center').text.strip())
    # decodedDoctorText = decodeEmail(doctorText)
    # print(decodedDoctorText)
    # print(doctorNamesList,doctorLinkList)
    print(tabulate(df, headers='keys', tablefmt='psql'))
    with open('Doctors.txt', 'w', encoding='utf8') as f:
        f.write(tabulate(df, headers='keys', tablefmt='psql'))
except UnicodeEncodeError:
    print('Cannot print some characters.')
