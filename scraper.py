import json
import time
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import os

load_dotenv()


session = requests.Session()
login_url = 'https://swd.bits-goa.ac.in/login/'
target_url = 'https://swd.bits-goa.ac.in/search/'


soup = BeautifulSoup(session.get(
    login_url, verify=False).text, 'html.parser')
csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

data = {
    'username' : os.getenv('swd_id'),
    'password' : os.getenv('swd_pwd'),
    'csrfmiddlewaretoken': csrf_token
}


hostel_data = {}
response = session.post(login_url, data=data, verify=False)

target_url = f"https://swd.bits-goa.ac.in/search/?csrfmiddlewaretoken={csrf_token}&name=&bitsId=&branch=&hostel=AH1&room=&action="

if response.status_code == 200:
    print('Login successful')
    
    hostel_select = soup.find('select', {'name': 'hostel'})
    hostel_options = ['AH1', 'AH2', 'AH3', 'AH4', 'AH5', 'AH6', 'AH7', 'AH8', 'AH9', 
                      'DH1', 'DH2', 'DH3', 'DH4', 'DH5', 'DH6',
                      'CH1', 'CH2', 'CH3', 'CH4', 'CH5', 'CH7'
                      ]
    
    
    all_hostel_data = {}

    # search page
    for hostel in hostel_options:
        print(f"Scraping data for {hostel}...")
        time.sleep(2)
        search_page_url = 'https://swd.bits-goa.ac.in/search/'
        response = session.get(search_page_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
        form_data = {
        'csrfmiddlewaretoken': csrf_token,
        'name': '',
        'bitsId': '',
        'branch': '',
        'hostel': f'{hostel}',  
        'room': '',
        'action': 'search',
        }
        response = session.get(search_page_url, params=form_data)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('tbody')
        if table is None:
            print(f"No table found for hostel. Check page_debug_.html for details.")
           
        rows = table.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            if len(columns) >= 4:  # 
                key = columns[1].text.strip()  # 
                values = {
                    'name': columns[2].text.strip(),
                    'hostel': columns[3].text.strip(),
                    'room': columns[4].text.strip()
                }
                hostel_data[key] = values


    with open(f'data.json', 'w') as file:
        json.dump(hostel_data, file, indent=4)


else:
    print('Login failed')
