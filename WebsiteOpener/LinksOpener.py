import webbrowser

file_name = "links.txt"

# app_path = 'open -a /Applications/Google\ Chrome.app %s'
app_path = 'open -a /Applications/Brave\ Browser.app %s'

try:
    with open(file_name,"r") as nf:
        file_content = nf.read()
        links_list = file_content.split("\n")

        for link in links_list:
            if link == None:
                continue
            webbrowser.get(app_path).open(link)
            print(link)

except:
    print("can't open the file check for the directory or ...")
    pass

