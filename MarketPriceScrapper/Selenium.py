from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
import os
from datetime import date

import ssl
ssl._create_default_https_context = ssl._create_stdlib_context

scripts_file_name = "script.txt"
scrapping_url = "https://www.sharesansar.com/company/"
market_price_element_xpath = '/html/body/div[2]/div/section[2]/div[3]/div/div/div/div[1]/div[2]/div[1]/div/div[1]/div[1]/span[2]'
time_delay = 0.1
date_based_file = True # true if file name should contain date


def read_as_list(filePath, splitString="\n") -> list:
    if not os.path.exists(filePath):
        print("File or Directory doesn't exists")
        return 

    with open(filePath, "r") as nf:
        content = nf.read()
        splitContent = content.split(splitString)

    splitContent = [ele for ele in splitContent if ele != '']
    return splitContent

active_driver = webdriver.Chrome()
scripts_list = read_as_list(scripts_file_name)
print(scripts_list)
out_file_name = scripts_file_name.split(".")[0]
market_price_list = list()

if date_based_file:
    today = date.today()
    td = today.strftime("-%d-%m-%Y")
    out_file_name += td + ".txt"
else:
    out_file_name += ".txt"

for script_name in scripts_list:
    active_driver.get(scrapping_url+script_name)
    
    script_market_price = active_driver.find_element(By.XPATH, market_price_element_xpath)
    market_price_list.append(script_market_price.text)

    # avoiding bot activity for detection system
    ActionChains(active_driver).move_to_element_with_offset(script_market_price, 100, 100).click().perform()
    time.sleep(time_delay)


with open(out_file_name,"a") as nf:
    content = "\n".join(market_price_list)
    nf.write(content)




