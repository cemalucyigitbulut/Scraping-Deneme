import requests
import re
from bs4 import BeautifulSoup

baseurl = 'https://neareasthospital.com/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'
}


r = requests.get('https://neareasthospital.com/doctors/?lang=en')
soup = BeautifulSoup(r.content, 'html.parser')
# soup =  BeautifulSoup(r.content,'html.parser')


# adını yaptık class_ çünkü python classi olmadığı için böyle yazdık

doctorNames = soup.find_all('div', class_='card-staff__title')
doctorList2 = soup.find_all('div', class_='card-staff__head')
doctorDuty = soup.find('div', class_='card-staff__duty').text.strip()
doctorLinkList = []
doctorNamesList = []

for class_ in doctorList2:
    for link in class_.find_all('a', href=True):
        doctorLinkList.append(link['href'])

for title in doctorNames:
    doctorNamesList.append(title.text.strip())

textlink = "https://neareasthospital.com/doctor/yesim-ozgol/?lang=en"
r = requests.get(textlink, headers=headers)
soup = BeautifulSoup(r.content, 'html.parser')
doctorEmailAndNumber = soup.find('div', class_='text-block').text.strip()

lines1 = doctorEmailAndNumber.split('\n')
DoctorInfo = []

for line in lines1:
        if '@' in line:
            email = line.strip()
            DoctorInfo.append(('Email', email))
        elif '+' in line:
            phone = line.strip()
            DoctorInfo.append(('Phone', phone))
    
    
doctor={
     'Name':doctorNamesList,
     'Contact':doctorEmailAndNumber,
     'Link':doctorLinkList
        
}

try:
    # print(doctorList2)
    # print(soup.find('div', class_='mariselle-title title is-size-4 is-title-underline is-text-center').text.strip())
    # decodedDoctorText = decodeEmail(doctorText)
    # print(decodedDoctorText)
    print()
except UnicodeEncodeError:
    print('Cannot print some characters.')
