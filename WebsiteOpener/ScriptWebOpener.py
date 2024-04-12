import webbrowser

file_name = "scripts.txt"

start, end = 0, 0 # use this if you want to select only particular range 
 
# base_URL = "https://www.sharesansar.com/company/" # sharesansar
base_URL = "https://merolagani.com/CompanyDetail.aspx?symbol=" # merolagnai
# base_URL = "https://nepsealpha.com/search?q=" # nepsealpha
# base_URL = "https://chukul.com/#/stock-profile?symbol=" # Chukul 

# app_path = chromePath = 'open -a /Applications/Google\ Chrome.app %s'
app_path = bravePath = 'open -a /Applications/Brave\ Browser.app %s'

try:
    with open(file_name,"r") as nf:
        file_content = nf.read()
        script_lists = file_content.split("\n")
        script_lists = [ele for ele in script_lists if ele != '']
        print(script_lists)
        for ind, scriptName in enumerate(script_lists):
            if start==end:
                mainURL = base_URL + scriptName
                print(mainURL)
                if(mainURL==base_URL):
                    continue
                webbrowser.get(app_path).open(mainURL)
            else:
                if ind >= start and ind <= end:
                    mainURL = base_URL + scriptName
                    print(mainURL)
                    if(mainURL==base_URL):
                        continue
                    webbrowser.get(app_path).open(mainURL)
                else:
                    continue

except:
    print("can't open the file check for the directory or ...")
    pass

