import chardet
import glob
import os
import pandas as pd
import random
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def clear_files():
    temp_folder = os.getcwd() + '/temp'
    
    for item in os.listdir(temp_folder):
        if item.endswith('.csv'):
            os.remove(os.path.join(temp_folder, item))

def get_encoding(file):
    with open(f'{file}', 'rb') as f:
        result = chardet.detect(f.read())
        
    return result['encoding']

def is_file_correct(file, year, city):
    encoding = get_encoding(file)
    
    try:
        df = pd.read_csv(f'{file}', nrows = 3, encoding = encoding)
        
        try:
            if(str(year) in df[df.columns[0]][2]) and (city in df[df.columns[0]][1]):
                return True
            return False
        except:
            return False
    except:
        return False

def get_file(state, city, year):
    print(f"Getting data from {city}/{year}...", end = ' ')
    
    browser = webdriver.Chrome(options = chrome_options)
    browser.get('http://tabnet.datasus.gov.br/cgi/deftohtm.exe?popsvs/cnv/popbr.def')
    browser.find_element(By.ID, 'L').find_elements(By.TAG_NAME, 'option')[-1].click()
    browser.find_element(By.ID, 'C').find_elements(By.TAG_NAME, 'option')[-3].click()
    browser.find_element(By.ID, 'fig3').click()
    all_cities = browser.find_element(By.ID, 'S3').find_element(By.TAG_NAME, 'option')

    if all_cities.is_selected():
        all_cities.click()

    for option in browser.find_element(By.XPATH, '//select[@id="A"]').find_elements(By.TAG_NAME, 'option'):
        if option.get_attribute('selected') == 'true':
            option.click()
    
    browser.find_element(By.XPATH, f"//select[@id='A']/option[text()={str(year)}]").click()
    browser.find_element(By.XPATH, f"//select[@id='S3']/*[contains(text(), {city})]").click()
    browser.find_element(By.CLASS_NAME, 'mostra').click()
    time.sleep(random.randint(5, 10))

    browser.find_elements(By.CLASS_NAME, 'botao_opcao')[0].find_element(By.TAG_NAME, 'a').click()
    time.sleep(random.randint(5, 10))
    
    file = glob.glob(f"{os.getcwd()}/temp/*csv")[0]

    if is_file_correct(file, year, city):
        os.rename(f"{file}", f"{os.getcwd()}/data/{state}/{city}/{str(year)}.csv")
        print('Done.')
    else:
        print('Error.')
        clear_files()
        get_file(state, city, year)

    browser.close()

def get_cities(state_code):
    print(f"Getting cities from state code {state_code}...", end = ' ')
  
    browser = webdriver.Chrome(options = chrome_options)
    browser.get('http://tabnet.datasus.gov.br/cgi/deftohtm.exe?popsvs/cnv/popbr.def')
    browser.find_element(By.ID, 'fig3').click()
    options = browser.find_element(By.ID, 'S3').find_elements(By.TAG_NAME, 'option')
    cities = []

    for option in options:
        city_code = option.text.split(' ')[0]

        if city_code[:2] == str(state_code):
            cities.append(city_code)
            
    browser.close()
    print('Done.')
    
    if state_code == 53:
        return cities
    else:
        return cities[:-1]

def get_restart_point(state, cities):
    completed = []
    
    for city in cities:
        folder = f"{os.getcwd()}/data/{state}/{city}"
        
        if os.path.exists(folder):
            files = glob.glob(f"{folder}/*.csv")
                
            if len(files) == 21:
                completed.append(city)

    remaining = [city for city in cities if city not in completed]

    for city in remaining:
        folder = f"{os.getcwd()}/data/{state}/{city}"
        
        if os.path.exists(folder):
            files = glob.glob(f"{folder}/*.csv")
            
            if len(files) > 0:
                remaining.remove(city)
                remaining.insert(0, city)
                year = int(sorted(files)[-1][-8:-4]) + 1
            
                return remaining, year
            else:
                remaining.remove(city)
                remaining.insert(0, city)
            
                return remaining, 2000
                            
    return remaining, 2000

def collect_data(state, cities, year):
    for city in cities:
        if not os.path.exists(f"{os.getcwd()}/data/{state}/{city}"):
            os.makedirs(f"data/{state}/{city}")
        
        for i in range(year, 2021):
            try:
                get_file(state, city, i)
            except IndexError:
                with open(f"data/{state}/{city}/{i}.csv", 'w') as f:
                    f.write(f"No data for city {city} in {i}.")
                
                print(f"No data for city {city} in {i}.")

            year = 2000 if i == 2020 else year

def main(state, cities, year, exceptions):
    clear_files()
    
    try:
        collect_data(state, cities, year)
    except KeyboardInterrupt:
        print("\nScript interrupted.")
    except Exception as e:
        print(f"Exception Thrown ({exceptions + 1}).")
        
        if exceptions < 4:
            cities, year = get_restart_point(state, cities)
            main(state, cities, year, exceptions + 1)
        else:
            print(f"Stopped after {exceptions + 1} exceptions.")
            print("The script is going to pause for 30 minutes and then return.")
            
            time.sleep(1800)
            cities, year = get_restart_point(state, cities)
            main(state, cities, year, exceptions = 0)            
    else:
        print("All data collected.")

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_experimental_option('prefs', {
    'download.default_directory': f"{os.getcwd()}/temp",
    'download.Prompt_for_download': False,
    'download.directory_upgrade': True,
    'safebrowsing.enabled': True
})

state_codes = [
    11, 12, 13, 14, 15, 16, 17,
    21, 22, 23, 24, 25, 26, 27, 28, 29,
    31, 32, 33, 35,
    41, 42, 43,
    50, 51, 52, 53
]

if len(sys.argv) != 2:
    print('Wrong number of arguments.')
else:
    state_code = int(sys.argv[1])

    if state_code not in state_codes:
        print('The argument must a state code.')
    else:
        with open(f"codes/{state_code}.txt", 'r') as f:
            all_cities = f.read().splitlines()

        cities, year = get_restart_point(state_code, all_cities)

        print(f"""{len(all_cities)} cities at total.
        {len(all_cities) - len(cities)} collected.
        {len(cities)} cities remaining.
        Starting at {cities[0]}/{year}.\
        """)

        main(state_code, cities, year, exceptions = 0)
