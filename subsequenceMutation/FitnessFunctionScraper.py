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
    

from bs4 import BeautifulSoup

def toxicity():
    with open('in.txt', 'r') as file:
        peptide_sequences = file.read()

    # Prepare the data to be sent in the form
    data = {
        'seq': peptide_sequences,
        'method': '1',  # SVM (Swiss-Prot) based
        'eval': '0.1',  # E-value cut-off
        'thval': '0.0',  # SVM threshold
        'field[]': ['4', '7', '9', '11', '13']  # Physicochemical properties to be displayed
    }

    # Create a session
    session = requests.Session()

    # Send a POST request to the form's action URL
    response = session.post('https://webs.iiitd.edu.in/raghava/toxinpred/multiple_test.php', data=data)

    # Parse the response content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the meta refresh tag
    meta_refresh = soup.find('meta', attrs={'http-equiv': 'refresh'})

    # If the meta refresh tag is found
    if meta_refresh:
        # Get the URL from the content attribute of the meta refresh tag
        relative_url = meta_refresh['content'].split('url=')[1]

        # Form the absolute URL by prepending the base URL
        absolute_url = 'https://webs.iiitd.edu.in/raghava/toxinpred/' + relative_url

        # Send a GET request to the new URL
        response = session.get(absolute_url)

        # Parse the content of the new page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the table with id "tableTwo"
        table = soup.find('table', {'id': 'tableTwo'})

        # Initialize an empty list to store the peptide id and SVM score values
        peptide_scores = []

        # If the table is found
        if table:
            # Find all the rows in the table body
            rows = table.find('tbody').find_all('tr')

            # For each row
            for row in rows:
                # Find all the columns
                cols = row.find_all('td')

                # Get the peptide id and SVM score values
                peptide_id = cols[0].text
                svm_score = cols[2].text
                toxic = cols[3].text

                # Append the values to the list
                peptide_scores.append((peptide_id, float(svm_score) * (-1.0), toxic))

        # Return the list of peptide id and SVM score values
        return peptide_scores
    else:
        print('Failed to submit the form. Status code:', response.status_code)