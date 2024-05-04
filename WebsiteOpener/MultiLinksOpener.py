import webbrowser

file_name = "scripts.txt"

app_path = 'open -a /Applications/Google\ Chrome.app %s'
# app_path = 'open -a /Applications/Brave\ Browser.app %s'

base_URL_list = [
    "https://merolagani.com/CompanyDetail.aspx?symbol=",
    "https://www.sharesansar.com/company/",
    "https://nepsealpha.com/search?q=",
    "https://chukul.com/#/stock-profile?symbol=",
    "https://www.nepalipaisa.com/company/"
]

try:
    with open(file_name,"r") as nf:
        file_content = nf.read()
        script_list = file_content.split("\n")

        for script in script_list:
            if script == "":
                continue
            for url in base_URL_list:
                link = url + script
                webbrowser.get(app_path).open(link)
                print(link)

except:
    print("can't open the file check for the directory or ...")
    pass

