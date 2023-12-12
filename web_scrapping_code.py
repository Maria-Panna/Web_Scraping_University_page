import pandas as pd
import requests
from bs4 import BeautifulSoup


def urlToResponse(url: str) -> BeautifulSoup:
    r = requests.get(url=url)
    return BeautifulSoup(r.content, 'html.parser')

# alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

alphabet = 'A'

dataframe = []

for letter in alphabet:
    try:
        root_url = f'https://www.umcs.pl/pl/address-book,1.html?letter={letter}'
        response_html = urlToResponse(root_url)
        s = response_html.find('ul', class_='list-plain list-spaced')
        lists_of_staff = s.find_all('a')

        for staff in lists_of_staff:
            row = []
            staff_page_link = 'https://www.umcs.pl'+ staff.get('href')
            row.extend([staff.text, staff_page_link])
            staff_page_html = urlToResponse(staff_page_link)
            staff_class = staff_page_html.find('dl', class_='dl-spreaded')
            values = [i.text.strip() for i in staff_class.find_all('dd')]
            row.extend(values)
            print(row)
            dataframe.append(row)

            
    except Exception as e: print(f'Cannot find staff for the letter "{letter}" because of the error: {e}')


df = pd.DataFrame(dataframe, columns=['Nazwa', 'Link', 'Stanowisko', 'Jednostki', 'Funkcje'])
df.to_excel('EmployeesDetails.xlsx')
print('Saved!')


