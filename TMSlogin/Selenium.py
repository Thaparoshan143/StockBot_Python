from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import io
from PIL import Image
import json
import numpy as np

import ssl
ssl._create_default_https_context = ssl._create_stdlib_context

import easyocr
import cv2
use_GPU = True
kernal_size = 5
kernal_size_2 = 2

# image processing using different methods and text extraction
def GetTextFromImage(imageName, filter_mode) -> str:

    img = cv2.imread(imageName) # 0 params, for gray image
    kernel = np.ones((kernal_size, kernal_size), np.uint8)
    kernel_two = np.ones((kernal_size_2, kernal_size_2),np.uint8)

    if filter_mode == 0:
        img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
    elif filter_mode == 1:
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    elif filter_mode == 2:
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    else:
        img = cv2.medianBlur(img, 5)
        img = cv2.dilate(img, kernel_two, 1)

        #edge detection    
        img = cv2.Canny(img, 100, 200)

    cv2.imwrite(imageName,img)

    image_path = r'{}'.format(imageName)  
    reader = easyocr.Reader(['en'],gpu=use_GPU) 
    # extracat text
    text = reader.readtext(image_path)[0][1]
    return text


TMS_URL = "" # TMS URL for login portal here eg: "https://tms58.nepsetms.com.np/login"
# if different for your borker please inspect and update these field below
username_xpath = '/html/body/app-root/app-login/div/div/div[2]/form/div[1]/input' 
password_xpath = '//*[@id="password-field"]'
captcha_img_xpath = '/html/body/app-root/app-login/div/div/div[2]/form/div[3]/div[2]/div/img'
captch_field_xpath = '//*[@id="captchaEnter"]'
login_xpath = '/html/body/app-root/app-login/div/div/div[2]/form/div[4]/input'
error_xpath = '//*[@id="toasty"]'
captcha_error_xpath = '//*[@id="toasty"]/ng2-toast/div/div[2]'
captcha_error_text = 'Wrong Captcha!\nPlease try again.'
delay_time = 0.5 # in seconds
image_filter_index = 0

credentials_file_name = "credentials.txt"
captcha_SSname = "captcha.png"
MAX_SCREEN_SIZE = 1700

class _account:
    def __init__(self, un, pw):
        self.username = un
        self.password = pw

# function to parse the account details based on json into the list format
def get_account_list(fileName) -> list:
    with open(fileName, "r") as nf:
        file_content_dict = json.load(nf)
    account_list = list()
    
    for item in file_content_dict:
        account_list.append(_account(
            item['username'],
            item['password']
        ))
    
    return account_list

# function for gettting element and sending key immediately
def find_element_send(by, path, key):
    try:
        temp = driver.find_element(by, path)
        temp.clear()
        temp.send_keys(key)
    except:
        print("- Error! can't find the search element")
        print("=> Error Element at : " + by + " | Associated Xpath is : " + path + " | with key : " + key)
        exit()

account_list = get_account_list(credentials_file_name)

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

split_screen_sizeX = int(MAX_SCREEN_SIZE/len(account_list))
xoffset = 0

for i in range(0, len(account_list)):
    sleep(delay_time/4)
    active_username = account_list[i].username
    active_password = account_list[i].password

    options.add_argument(f'--window-size={split_screen_sizeX},1080')
    options.add_argument(f'--window-position={xoffset},0')
    xoffset += split_screen_sizeX

    driver = webdriver.Chrome(options=options)
    driver.get(TMS_URL)

    sleep(delay_time)
    image_filter_index = 0

    while True:
        try:
            find_element_send(By.XPATH, username_xpath, active_username)
            find_element_send(By.XPATH, password_xpath, active_password)

            captcha = driver.find_element(By.XPATH, captcha_img_xpath).screenshot_as_png
            captcha_ss = Image.open(io.BytesIO(captcha)).save(captcha_SSname)
            try:
                print("Try get element")
                raw_captcha_text = GetTextFromImage(captcha_SSname, image_filter_index%4)
                filtered_captcha_text = ""
                print(raw_captcha_text)
                # filtering for only a-z, A-Z and 0-9 (alphanumeric)
                for char in raw_captcha_text:
                    if char.isalpha() or char.isnumeric():
                        filtered_captcha_text += char
                    else:
                        print("Invalid character detected by OCR! trying again with next processing method")
                        image_filter_index += 1
                        continue

            except:
                print("Could not extract text from the image! Trying again with next method")
                image_filter_index += 1
                continue

            find_element_send(By.XPATH, captch_field_xpath, filtered_captcha_text)
            sleep(delay_time/2)
            login_button = driver.find_element(By.XPATH, login_xpath).click()
            print("# Login Button clicked successful")
            sleep(delay_time*1.5)

            # catch if any error occured and retry again
            try:
                print("Inside error code finder successful")
                login_error = driver.find_element(By.XPATH, captcha_error_xpath)
                if login_error.text == captcha_error_text:
                    print("-> Login Error Text : " + login_error.text)
                    print("Captcha Failed! Trying again")
                    image_filter_index += 1
                    continue
                else:
                    print("Login successful! Other errors occured, please see terminal for the error")
                    break
            except:
                print("No Login Error! Successfully Logged in")
                break
        except:
            print("Unable to retrieve the datas field from given URL! please either update the xpath or other fields and try again")
        


