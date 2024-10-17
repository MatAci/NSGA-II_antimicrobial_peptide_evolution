import pandas as pd
import requests
from bs4 import BeautifulSoup
import urllib3

def scrape_fitness_function():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    url = 'https://www.camp.bicnirrh.res.in/predict/hii.php'
    file_path = 'in.txt'
    data = {
        'dataset': 'synthetic',
        'algo[]': ['rf'],
    }

    with open(file_path, 'rb') as file:
        files = {'userfile': (file.name, file, 'text/plain')}
        response = requests.post(url, data=data, files=files, verify=False)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', attrs={'border': '1'})
        rows = table.find_all('tr')
        data = []

        for row in rows[1:]:
            cols = row.find_all('td')
            data.append((cols[0].text, cols[2].text))  # Create a tuple (peptide_string, ff_amp_probability)

        return data
    else:
        print("Failed to submit the form. Status code:", response.status_code)
        return None