from bs4 import BeautifulSoup
import requests
import multiprocessing as mp
import os
from datetime import date

import ssl
ssl._create_default_https_context = ssl._create_stdlib_context

script_file_name = "script.txt"
date_based_file = False # file will be based on the date if true
number_of_processes = 10

scrapping_url = "https://merolagani.com/CompanyDetail.aspx?symbol="
market_price_element_id = 'ctl00_ContentPlaceHolder1_CompanyDetail1_lblMarketPrice'


def read_as_list(filePath, splitString="\n") -> list:
    if not os.path.exists(filePath):
        print("File or Directory doesn't exists")
        return 

    with open(filePath, "r") as nf:
        content = nf.read()
        splitContent = content.split(splitString)

    splitContent = [ele for ele in splitContent if ele != '']
    return splitContent

scripts_MP = list()
scripts_list = read_as_list(script_file_name)

scripts_split_count = int(len(scripts_list) / number_of_processes)
split_scripts_list = list()

# spliting into different list for multiprocessing
for i in range(number_of_processes):
    start = i * scripts_split_count
    end = start + scripts_split_count
    if i == number_of_processes-1:
        split_scripts_list.append(scripts_list[start:])
    else:
        split_scripts_list.append(scripts_list[start:end])

def get_price_content(script) -> str:
    target_url = scrapping_url + script
    print(target_url)
    web_repsonse = requests.get(target_url)

    if web_repsonse.status_code == 200: 
        page_content = BeautifulSoup(web_repsonse.content, 'lxml')
        market_price = page_content.find('span', id=market_price_element_id).text
        return market_price
    else:
        print("Newtork Error! Try again later")
        return 0

def write_list_MP(scripts_list : list):
    joined_str = ""
    for script in scripts_list:
        scripts_MP.append(get_price_content(script))
        joined_str += (script + " - " + scripts_MP[-1] + "\n")
    
    file_name = ''
    if date_based_file:
        today = date.today()
        td = today.strftime("-%d-%m-%Y")
        file_name = script_file_name.split(".")[0] + td + "_MP.txt"
    else:
        file_name = script_file_name.split(".")[0] + "_MP.txt"
    
    with open(file_name, "a") as scriptsMPFile:
        scriptsMPFile.write(joined_str)

# entry point
if __name__ == '__main__':
    for i in range(number_of_processes):
        process = mp.Process(target=write_list_MP, args=(split_scripts_list[i], ))
        process.start()
