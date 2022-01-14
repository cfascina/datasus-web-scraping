#!/usr/bin/env python
# coding: utf-8

# In[34]:


import chardet
import glob
import os
import pandas as pd
import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


# In[35]:


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


# In[36]:


def clear_files():
    temp_folder = os.getcwd() + '/temp'
    
    for item in os.listdir(temp_folder):
        if item.endswith('.csv'):
            os.remove(os.path.join(temp_folder, item))


# In[37]:


def get_encoding(file):
    with open(f'{file}', 'rb') as f:
        result = chardet.detect(f.read())
        
    return result['encoding']


# In[38]:


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


# In[39]:


def get_file(year, city):
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
        os.rename(f"{file}", f"{os.getcwd()}/data/{city}/{str(year)}.csv")
        print('Done.')
    else:
        print('Error.')
        clear_files()
        get_file(year, city)

    browser.close()


# In[40]:


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
    
    return cities[:-1]


# In[47]:


def get_restart_point(cities):
    for city in cities:
        folder = f"{os.getcwd()}/data/{city}"

        if os.path.exists(folder):
            files = glob.glob(f"{folder}/*.csv")
            remaining_cities = cities[cities.index(city):]

            if len(files) == 21:
                pass
            elif len(files) == 0:
                return remaining_cities, 2000
            else:
                year = int(sorted(files)[-1][-8:-4]) + 1
                
                return remaining_cities, year
        else:
            remaining_cities = cities[cities.index(city):]


# In[42]:


def collect_data(cities, year):
    for city in cities:
        if not os.path.exists(f"{os.getcwd()}/data/{city}"):
            os.makedirs(f"data/{city}")
        
        for i in range(year, 2021):
            try:
                get_file(i, city)
            except IndexError:
                with open(f"data/{city}/{year}.csv", 'w') as f:
                    f.write(f"No data for city {city} in {year}.")
                
                print(f"No data for city {city} in {year}.")
        
            year = 2000 if i == 2020 else year


# In[43]:


def main(cities, year, exceptions = 0):
    clear_files()
    
    try:
        collect_data(cities, year)
    except:
        print(f"Exception Thrown ({exceptions + 1}).")
        
        if exceptions < 14:
            cities, year = get_restart_point(cities)
            main(cities, year, exceptions + 1)
        else:
            print(f"Stopped after {exceptions + 1} exceptions.")
            print("The script is going to pause for 30 minutes and then return")
            
            time.sleep(1800)
            cities, year = get_restart_point(cities)
            main(cities, year)
            
    print("All data collected.")


# In[44]:


all_cities = get_cities(43)


# In[45]:


# with open('codes/43.txt', 'w') as f:
#     f.write('\n'.join(all_cities))

# file = open('codes/43.txt', 'r')
# codes = file.read()
# all_cities = codes.split('\n')
# file.close()


# In[48]:


cities, year = get_restart_point(all_cities)


# In[49]:


print(f"{len(all_cities)} cities at total.\n{len(cities)} cities remaining.")


# In[51]:


main(cities, year)

