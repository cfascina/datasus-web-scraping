from itertools import groupby
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s.%(msecs)03d - %(message)s', datefmt = '%y-%m-%d %H:%M:%S'
)

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

def get_city_codes():
    logging.info('Getting city codes.')
  
    browser = webdriver.Chrome(options = chrome_options)
    browser.get("http://tabnet.datasus.gov.br/cgi/deftohtm.exe?popsvs/cnv/popbr.def")
    browser.find_element(By.ID, 'fig3').click()
    options = browser.find_element(By.ID, 'S3').find_elements(By.TAG_NAME, "option")
    city_codes = []

    for option in options:
        city_code = option.text.split(' ')[0]

        if city_code != "Todas" and city_code[:2] != "00" and city_code[2:] != "0000":
            city_codes.append(city_code)
            
    browser.close()
    logging.info('Done.')
    
    return city_codes

city_codes = get_city_codes()
logging.info(f"{len(city_codes)} cities collected.")

for state, cities in groupby(sorted(city_codes), key = lambda x: x[:2]):
    state_cities = []
    
    for city in cities:
        state_cities.append(city)
    
    with open(f"codes/{state}.txt", "w") as f:
        f.write('\n'.join(state_cities))
    
    logging.info(f"Created file for state {state} with {len(state_cities)} cities.")
