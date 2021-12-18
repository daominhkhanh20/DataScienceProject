from time import sleep
from selenium import webdriver

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
opts = Options()

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import urllib

# enable browser logging, không cần quan tâm
d = DesiredCapabilities.CHROME
d['goog:loggingPrefs'] = { 'browser':'ALL' }
user_agent =  ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
'AppleWebKit/537.36 (KHTML, like Gecko) '
'Chrome/39.0.2171.95 Safari/537.36')
opts.add_argument(f'user-agent={user_agent}')

# Start Chrome Driver. Thay chromedriver bằng đường dẫn của chromedriver.exe
chromedriver = 'D:/Program Files/chromedriver.exe'
driver = webdriver.Chrome(executable_path= chromedriver,chrome_options=opts,desired_capabilities=d)

# Open the URL you want to execute JS
URL = 'https://carnet.ai/'
driver.get(URL)

import json
lineByLine = []
# Mở file json
with open('D:/LEARN/LEARN/20211/DS/DataScienceProject/CrawlData/chotot.json',encoding="utf8") as file:
    for n,line in enumerate(file,1):
        if(len(line)>20):
            # xóa dấu , cuối dòng
            line = line[:-2]
            lineByLine.append(line)
print(len(lineByLine))

# vị trí lấy object trong json
lineByLine = lineByLine[:]

# Load từng object ra json để lấy url_image
for line in lineByLine:
    try:
        fullline = json.loads(line)
        dataurl = fullline["url_image"]
        print(dataurl)
        endurl = urllib.parse.quote(dataurl,safe = '')
        endurl = endurl.rstrip ("%0A")
        urlcommand = "CARURL = \""+ endurl +"\";"
        print(urlcommand)
        # đường dẫn tới file code js, crawl.txt đi kèm
        f = open("D:/crawl.txt", "r")
        crawlcommand = f.read()
        fullcommand = urlcommand + crawlcommand
        driver.execute_script(fullcommand)
        #nghỉ 5 giây, đừng chỉnh, không nó lăn ra lỗi đấy
        sleep(5)
    except:
        print(fullline)


