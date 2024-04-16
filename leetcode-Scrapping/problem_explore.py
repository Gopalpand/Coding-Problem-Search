import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup

s=Service(ChromeDriverManager().install())
driver=webdriver.Chrome(service=s)

heading_class=".flex.items-start.justify-between.gap-4"
body_class=".elfjS"
index=1
QDATA_FOLDER="leetcode-Scrapping\Qdata"


def get_array_of_links():
    arr=[]
    with open("leetcode-Scrapping\lc.txt","r",encoding="utf-8") as f:
        for i in f:
            arr.append(i)
    return arr

def add_text_to_index_file(text):
    file=os.path.join(QDATA_FOLDER,"index.txt")
    with open(file,"a",encoding="utf-8") as f:
        f.write(str(index)+". "+text+"\n")


def add_link_to_Qindex_file(text):
    file=os.path.join(QDATA_FOLDER,"Qindex.txt")
    with open(file,"a",encoding="utf-8") as f:
        f.write(str(index)+". "+text)


def create_and_add_text_to_file(file_name,text):
    folder_path=os.path.join(QDATA_FOLDER,"data",file_name)
    os.makedirs(folder_path,exist_ok=True)
    file_path=os.path.join(folder_path,file_name+".txt")
    with open(file_path,"w",encoding="utf-8") as f:
        f.write(text)

def getpagedata(url,index):
    try:
        driver.get(url)
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, body_class)))
        time.sleep(2)
        heading=driver.find_element(By.CSS_SELECTOR,heading_class)
        body=driver.find_element(By.CSS_SELECTOR,body_class)
        print(heading.text)
        print(body.text)
        if(heading.text and body.text):
            create_and_add_text_to_file(str(index),body.text)
            add_text_to_index_file(heading.text)
            add_link_to_Qindex_file(url)
        time.sleep(1)
        return True
    except Exception as e:
        print(e)
        return False

if __name__ == "__main__":
    arr=get_array_of_links()
    print(arr)
    print(len(arr))
    for i in range(0,len(arr)):
        link=arr[i]
        print(i+1,".")
        print(link)
        success=getpagedata(link,index)
        if success:index+=1
