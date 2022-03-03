import chardet
import csv
import glob
import logging
import os
import pandas as pd
import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s.%(msecs)03d - %(message)s', datefmt = '%y-%m-%d %H:%M:%S'
)

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
    logging.info(f"Getting data from {city}/{year}.")
    
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
        os.replace(f"{file}", f"{os.getcwd()}/data/{state}/{city}/{str(year)}.csv")
    else:
        clear_files()
        get_file(state, city, year)

    browser.close()

def get_missing():
    directory = os.getcwd() + '/data'
    missing = []

    for root, subdirectories, files in os.walk(directory):
        for file in files:

            with open(os.path.join(root, file), 'r', encoding = 'latin-1') as f:
                reader = csv.reader(f)

                if len(list(reader)) == 1:
                    path = os.path.join(root, file).split('/')

                    missing.append([path[-3], path[-2], path[-1][:4]])
    return missing

def main():
    logging.info('Search started.')
    
    for item in get_missing():
        try:
            get_file(item[0], str(item[1]), item[2])
        except Exception as e:
            with open('missing.txt', 'a') as f:
                f.write(f"{item[1]} - {item[2]}\n")

            pass
    
    logging.info('Search completed.')

logging.info(f"{len(get_missing())} items without Census data were found.")
main()
logging.info(f"After reprocessing, {len(get_missing())} items remained without Census data.")
