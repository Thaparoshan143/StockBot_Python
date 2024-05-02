from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
import os

import ssl
ssl._create_default_https_context = ssl._create_stdlib_context

baseURL = "https://meroshare.cdsc.com.np/#/login"
credfile_name = "credentials.txt"
bank_name = 'NIC ASIA BANK LIMITED (13700)' # copy the bank name from list of Meroshare dropdown option if different ## Warning: Should be exact match.
time_delay = 2 # min 2 sec recommended

def get_cred_list(filePath):
    if not os.path.exists(filePath):
        print("File or Directory doesn't exists")
        return 
    
    username_list = list()
    password_list = list()

    with open(filePath, "r") as nf:
        content = nf.read()
        splitContent = content.split("\n")

        for item in splitContent:
            username_list.append(item.split(" ")[0])
            password_list.append(item.split(" ")[-1])

    return [username_list, password_list]

username_list = get_cred_list(credfile_name)[0]
password_list = get_cred_list(credfile_name)[-1]
print(username_list)

splitScreenSizeX = int(1700/len(username_list))
xoffset = 0

options = Options()
options.add_experimental_option("detach", True)

for ind in range(0, len(username_list)):
    active_username = username_list[ind]
    active_password = password_list[ind]
    
    options.add_argument(f'--window-size={splitScreenSizeX},1080')
    options.add_argument(f'--window-position={xoffset},0')
    xoffset += splitScreenSizeX

    driver = webdriver.Chrome(options=options)
    driver.get(baseURL)

    sleep(time_delay)
    username_field = driver.find_element(By.ID, 'username')
    username_field.send_keys(active_username)
    password_field = driver.find_element(By.ID, 'password')
    password_field.send_keys(active_password)

    driver.find_element(By.XPATH, '//*[@id="selectBranch"]/span/span[1]/span').click()
    bank_selection = driver.find_element(By.XPATH, '/html/body/span/span/span[1]/input')
    bank_selection.send_keys(bank_name)
    bank_selection.send_keys(Keys.ENTER)
    
    driver.find_element(By.XPATH, '/html/body/app-login/div/div/div/div/div/div/div[1]/div/form/div/div[4]/div/button').click()

