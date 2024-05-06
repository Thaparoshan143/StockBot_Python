import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep

import ssl
ssl._create_default_https_context = ssl._create_stdlib_context

start = 1

script_file_name = "hydroscript.txt"
out_file_name = "temp2.csv"
mode = "a"
base_URL = 'https://chukul.com/stock-profile?symbol='

# class specific to hydropower
class script_info:
    def __init__(self, sn, mp, ic, cpMW, puc) -> None:
        self.script_name = sn
        self.market_price = mp
        self.installed_capacity = ic
        self.cost_per_MW = cpMW
        self.paid_up_capital = puc
# ----------------------------------------------------------

def get_list_from_file(file_name) -> list:
    with open(file_name, "r") as nf:
        temp = nf.read().split("\n")

    return [item for item in temp if item != '']

def print_script_info(script_info_list):
    for ind, script in enumerate(script_info_list):
        print("-> " + str(ind) + " . " + script.script_name + " | " + script.market_price + " | "  + script.installed_capacity + " | " + script.cost_per_MW + " | " + script.paid_up_capital) 
        print("----------------------------------------------------------------------")


script_list = get_list_from_file(script_file_name)

script_info_list = list()
common_xpath_base = '//*[@id="q-app"]/div/div[1]/div/div[2]/main/div/div[2]/div/div/div/div/div/div[2]/div[1]/div[1]/'

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
    csv_writer.writerow(["SN", "Script", "Market Price (RS)", "Installed Capacity (MW)", "Cost/MW (Cr)", "Float Share", "MP * Cost/MW"])

for ind, script in enumerate(script_list):
    active_driver.get(base_URL + script)
    sleep(2)
    active_driver.execute_script("window.scrollTo(0, 250)")
    market_price = try_get_element_from_xpath(active_driver, 'div[1]/p[1]/div/div').split("(")[0]
    cost_per_MW = try_get_element_from_xpath(active_driver, 'div[1]/div[1]/div/div[3]/div[2]').split("\n")[1]
    installed_cap = try_get_element_from_xpath(active_driver, 'div[1]/div[1]/div/div[3]/div[1]').split("\n")[1]
    paid_up_capital = try_get_element_from_xpath(active_driver, 'div[3]/div').split("\n")[1]

    script_obj = script_info(script, str(market_price), str(installed_cap), str(cost_per_MW), str(paid_up_capital))

    with open(out_file_name, mode) as nf:
        csv_writer = csv.writer(nf)
        csv_writer.writerow([   str(ind+1),
                                script_obj.script_name,
                                script_obj.market_price,
                                script_obj.installed_capacity, 
                                script_obj.cost_per_MW,
                                script_obj.paid_up_capital,
                                float(script_obj.market_price.split(" ")[0]) * float(script_obj.cost_per_MW.split(" ")[0])
                            ])

