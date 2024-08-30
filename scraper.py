import json
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
    
    # iterate over each hostel from li
    hostel_select = soup.find('select', {'name': 'hostel'})
    hostel_options = [option['value'] for option in hostel_select.find_all('option') if option['value']]
    
    
    all_hostel_data = {}

    # Step 5: Iterate through each hostel option
    for hostel in hostel_options:
        print(f"Scraping data for {hostel}...")
        response = session.get(search_page_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

        form_data = {
            'csrfmiddlewaretoken': csrf_token,
            'name': '',
            'bitsId': '',
            'branch': '',
            'hostel': hostel,
            'room': '',  
            'action': 'search'  
        }
        response = session.get(search_page_url, params=form_data)

        # Step 6: Submit form for the current hostel and scrape data
        if response.url != search_page_url:
            print(f"Unexpected redirection to: {response.url}")
            continue

        # Check the status of the response
        if response.status_code != 200:
            print(f"Failed to retrieve data for {hostel}. Status code: {response.status_code}")
            continue

        soup = BeautifulSoup(response.content, 'html.parser')

        # Debug: Save the page content to check what is returned
        # with open(f'page_debug_{hostel}.html', 'w') as file:
        #     file.write(soup.prettify())

        # Extract table data
        table = soup.find('tbody')
        if table is None:
            print(f"No table found for hostel: {hostel}. Check page_debug_{hostel}.html for details.")
            continue

        rows = table.find_all('tr')

        hostel_data = {}

        for row in rows:
            columns = row.find_all('td')
            if len(columns) >= 4:  # Ensure there are at least 4 columns
                key = columns[1].text.strip()  # First column as key
                values = {
                    'Column2': columns[2].text.strip(),
                    'Column3': columns[3].text.strip(),
                    'Column4': columns[4].text.strip()
                }
                hostel_data[key] = values

        # Append the scraped data to the main dictionary
        all_hostel_data[hostel] = hostel_data
        with open(f'page_debug_{hostel}.txt', 'w') as file:
            file.write(str(all_hostel_data))

        # with open('table_data.json', 'w') as jsonfile:
        #     json.dump(all_hostel_data, jsonfile, indent=4)

        with open('table_data.json', 'w') as jsonfile:
            json.dump(all_hostel_data, jsonfile, indent=4)


else:
    print('Login failed')
