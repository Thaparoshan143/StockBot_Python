import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep

import ssl
ssl._create_default_https_context = ssl._create_stdlib_context

start = 1

script_file_name = "scripts.txt"
out_file_name = "gen.csv"
mode = "a"
base_URL = 'https://chukul.com/stock-profile?symbol='

# common class for scripts
class script_info:
    def __init__(self, sn, fn, sec, mp, puc, bv, eps, highlow52, avg120, avg180, ldiv) -> None:
        self.script_name = sn
        self.full_name = fn
        self.sector = sec
        self.market_price = mp
        self.paid_up_capital = puc
        self.book_value = bv
        self.EPS = eps
        self.highlow_52week = highlow52
        self.average_120day = avg120
        self.average_180day = avg180
        self.last_dividend = ldiv
# ----------------------------------------------------------

def get_list_from_file(file_name) -> list:
    with open(file_name, "r") as nf:
        temp = nf.read().split("\n")

    return [item for item in temp if item != '']

script_list = get_list_from_file(script_file_name)

script_info_list = list()
common_xpath_base = '//*[@id="q-app"]/div/div[1]/div/div[2]/main/div/div[2]/div/div/div/div/div/div[2]/div[1]/div[1]/'
time_delay = 3

def try_get_element_from_xpath(driver, xpath) -> str:
    try:
        return driver.find_element(By.XPATH, common_xpath_base + xpath).text
    except:
        return "Unknown"

options = Options()
options.add_experimental_option("detach", False)

options.add_argument(f'--window-size=1920,1080')
options.add_argument(f'--window-position=0,0')

active_driver = webdriver.Chrome(options=options)
script_info_list = list()

csv.field_size_limit(100)
with open(out_file_name, "w") as nf:
    csv_writer = csv.writer(nf)
    csv_writer.writerow(["SN", "Script", "Company", "Sector", "Market Price", "Paid up Capital", "Book Value", "EPS", "P/E", "P/B", "52 week High/Low", "120 days Avg.", "180 days Avg.", "Last Dividend"])

for ind, script in enumerate(script_list):
    active_driver.get(base_URL + script)
    sleep(time_delay)
    active_driver.execute_script("window.scrollTo(0, 250)")
    full_name = try_get_element_from_xpath(active_driver, 'div[1]/p[1]').split("(")[0]
    sector = try_get_element_from_xpath(active_driver, 'div[1]/p[2]')
    market_price = try_get_element_from_xpath(active_driver, 'div[1]/p[1]/div/div').split("(")[0]
    paid_up_capital = try_get_element_from_xpath(active_driver, 'div[3]/div').split("\n")[1]
    book_value = try_get_element_from_xpath(active_driver, 'div[5]/div[3]').split("\n")[1]
    eps = try_get_element_from_xpath(active_driver, 'div[5]/div[1]').split("\n")[1]
    highlow52 = try_get_element_from_xpath(active_driver, 'div[4]/div[4]').split("\n")[1]
    average120 = try_get_element_from_xpath(active_driver, 'div[4]/div[5]').split("\n")[1]
    average180 = try_get_element_from_xpath(active_driver, 'div[4]/div[6]').split("\n")[1]
    lastdiv = try_get_element_from_xpath(active_driver, 'div[6]/div[3]')

    script_obj = script_info(script, full_name, sector, market_price, paid_up_capital, book_value, eps, highlow52, average120, average180, lastdiv)

    with open(out_file_name, mode) as nf:
        csv_writer = csv.writer(nf)
        csv_writer.writerow([   str(ind+1),
                                script_obj.script_name,
                                script_obj.full_name,
                                script_obj.sector,
                                script_obj.market_price,
                                script_obj.paid_up_capital,
                                script_obj.book_value,
                                script_obj.EPS,
                                float(script_obj.market_price)/float(script_obj.EPS),
                                float(script_obj.market_price)/float(script_obj.book_value),
                                script_obj.highlow_52week,
                                script_obj.average_120day,
                                script_obj.average_180day,
                                script_obj.last_dividend
                             ])

