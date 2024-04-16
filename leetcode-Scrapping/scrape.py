import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

s=Service(ChromeDriverManager().install())
driver=webdriver.Chrome(service=s)

page_url="https://leetcode.com/problemset/?page="

def get_all_links(url):
    driver.get(url)
    time.sleep(3)

    arr=driver.find_elements(By.TAG_NAME,'a')

    links=[]

    for i in arr:
        try:
            link=i.get_attribute('href')
            if "/problems/" in link and "/solution" not in link:
                links.append(link)
        except:
            pass

    links=list(set(links))
    return links

final_links=[]

for j in range(1,63):
    url=page_url+str(j)
    print(url)
    final_links+=get_all_links(url)

final_links=list(set(final_links))

with open('leetcode-Scrapping\lc.txt','a') as f:
    for i in final_links:
        f.write(i+'\n')

driver.quit()
