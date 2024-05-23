# This program scraps the Annual Report of the listed company base on the parameter below

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import os
import time

import ssl
ssl._create_default_https_context = ssl._create_stdlib_context

fin_URL = "https://merolagani.com/CompanyReports.aspx?type=ANNUAL"
search_year = "079/80"
filter_year = "2079/80"
loadmore_click_count = 1
should_open_window = False
context_offset =  "-".join(filter_year.split("/"))
out_folder_name = "FinReport" + "-" + context_offset
out_folder_offset = os.getcwd() + "/" + out_folder_name
per_delay_time = 4
should_overwrite_existing = True
should_write_links = False

print(out_folder_offset)

if should_overwrite_existing:
    if os.path.exists(out_folder_offset):
        print("Folder Already Exist! Overwrting in the directory")
    else:
        os.mkdir(out_folder_name)
elif not should_overwrite_existing:
    if os.path.exists(out_folder_offset):
        print("Folder Already Exist! Change either name new directory or deleted old one")
        exit(0)
    else:
        os.mkdir(out_folder_name)


options = Options()
options.add_experimental_option("detach", True)

options.add_argument(f'--window-size=1920,1080')
options.add_argument(f'--window-position=0,0')

active_driver = webdriver.Chrome(options=options)
active_driver.get(fin_URL)

search_year_ele = active_driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_ddlFiscalYearFilter"]')
search_year_ele.click()
search_year_ele.send_keys(search_year)

search_ele = active_driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_lbtnSearch"]')
search_ele.click()

try:
    loadmore_ele = active_driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_divData"]/a')
    for i in range(0, loadmore_click_count):
        time.sleep(per_delay_time/2)
        loadmore_ele.click()

    time.sleep(per_delay_time/8)
    fin_announcements_list = active_driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_divData"]/div')
    fin_announcement_links = fin_announcements_list.find_elements(By.TAG_NAME, 'a')

    report_links = list()
    for f in fin_announcement_links:
        name = f.text.upper()
        if filter_year in name:
            report_links.append(f.get_attribute("href"))

    if should_write_links:
        link_filename = context_offset + ".txt"
        print(os.getcwd() + "/" + link_filename)
        with open(os.getcwd() + "/" + link_filename, "w") as nf:
            link_content = "\n".join(report_links)
            nf.write(link_content)
            print("Links written successfully in file : " + link_filename)

    if should_open_window:
        for report_link in report_links:
            JSscript = 'window.open("'+ report_link + '","_blank");'    
            active_driver.execute_script(JSscript)
    else:
        for report_link in report_links:
            active_driver.get(report_link)
            time.sleep(per_delay_time/4)
            script_symbol = active_driver.find_element(By.XPATH, '//*[@id="aspnetForm"]/div[4]/div[5]/div/div/table/tbody/tr[1]/td[2]/a').text.split(" ")[0]
            print(script_symbol)

            while True:
                active_driver.execute_script("window.scrollBy(0, 700)")
                session = requests.Session()
                retry = Retry(connect=3, backoff_factor=0.5)
                adapter = HTTPAdapter(max_retries=retry)
                session.mount('http://', adapter)
                session.mount('https://', adapter)
                try:
                    time.sleep(per_delay_time/4)
                    raw_pdf_ele = active_driver.find_element(By.XPATH, '//*[@id="pdf-container"]/embed')
                    pdf_src = raw_pdf_ele.get_attribute('src')
                    print("# - pdf src - " + pdf_src)
                    raw_pdf = session.get(pdf_src).content
                    time.sleep(per_delay_time)
                    print("-> pdf path - " + out_folder_offset + "/" + script_symbol + ".pdf")
                    with open(out_folder_offset + "/" + script_symbol + ".pdf", "wb") as nf:
                        nf.write(raw_pdf)
                    print("# Write succesful for : " + script_symbol)
                    break
                except:
                    print("Couldn't resolve pdf url! trying again : ", pdf_src)
                    time.sleep(per_delay_time)
                    continue

except:
    print("Couldn't find the report for given year : " + filter_year)