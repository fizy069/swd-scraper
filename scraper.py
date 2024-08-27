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
    'username': os.getenv('USERNAME'),
    'password': os.getenv('PASSWORD'),
    'csrfmiddlewaretoken': csrf_token
}

response = session.post(login_url, data=data, verify=False)

target_url = f"https://swd.bits-goa.ac.in/search/?csrfmiddlewaretoken={csrf_token}&name=&bitsId=&branch=&hostel=AH1&room=&action="

if response.status_code == 200:
    print('Login successful')
    
    # search page
    search_page_url = 'https://swd.bits-goa.ac.in/search/'
    response = session.get(search_page_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
    form_data = {
    'csrfmiddlewaretoken': csrf_token,
    'name': '',
    'bitsId': '',
    'branch': '',
    'hostel': 'AH1',  
    'room': '',
    'action': 'search',
    }
    response = session.get(search_page_url, params=form_data)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('tbody')
    with open('output.txt', 'w') as file:
        file.write(table.prettify())


else:
    print('Login failed')
