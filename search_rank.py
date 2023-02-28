import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

# 自行輸入檔名最後方的流水編碼(可用日期)，才不會重複檔名將就的檔案覆蓋
no=input('請輸入最後方的流水編碼(可用日期):')

def rank2csv(search):    
    fn='rank'+no+'.csv'
    
    url='https://www.google.com/search?q='+search
    # 第一頁為靜態使用requests去爬
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}   
    html=requests.get(url,headers=headers)   
    bs=BeautifulSoup(html.text,'html.parser') 
    ress = bs.find_all(class_='yuRUbf')
    print('關鍵字:',search)    
    # i是排名
    i=0
    exist=0
    
    for res in ress:    
        i+=1
        #title=res.find('h3')
        blog_url= res.find('a')['href']
        # p代表頁數
        p=1
        # 判斷文章是否已出現在當前頁面
        if 'chilldaily' in blog_url:  
            exist=1
            day=datetime.date.today()
            print('文章頁數',p)
            print('文章排名',i)
            print('文章網址',blog_url)
            print('查詢日期',day)
            print()
            with open(fn,'a',newline='') as file:
                file=csv.writer(file)
                file.writerow([search,str(p),str(i),str(day)])
                #(search+','+str(p)+','+str(i)+','+str(day))
                #file.writelines('\n')
    
    # 沒有排名在第一頁，再用driver爬
    if exist==0:
        driver=webdriver.Chrome()
        driver.get(url)
        try:
            while exist==0:           
                p+=1        
                next_p=driver.find_element(By.ID,'pnnext')
                next_p.click()
                #緩衝一下
                time.sleep(3)
                ress=driver.find_elements(By.CLASS_NAME,'MjjYud')
                
                for res in ress:
                    i+=1
                    blog_url=res.find_element(By.TAG_NAME,'a').get_attribute('href')                    
                    if 'chilldaily' in blog_url:  
                        exist=1
                        day=datetime.date.today()
                        print('文章頁數',p)
                        print('文章排名',i)
                        print('文章網址',blog_url)
                        print('查詢日期',day)
                        print()
                        with open(fn,'a',newline='') as file:
                            file=csv.writer(file)
                            file.writerow([search,str(p),str(i),str(day)])
            
        except:
            # 爬資料次數太多可能跳出確認是否為機器人訊息，或是文章沒有被這個關鍵字排名
            print('哭哭沒有出現或是出現錯誤...')
            print()          
            with open(fn,'a') as file:
                file.writelines(search+',無,無,無')
                file.writelines('\n')


fn='rank'+no+'.csv'
# 先將欄名寫入檔案
with open(fn,'w') as file:
    file.writelines('關鍵字,頁數,排名,查詢時間')
    file.writelines('\n')

# 使用檔案中所有關鍵字去擷取排名
with open('keywords.txt','r') as file:
   keys=file.readlines()
   key=keys[0].split(',')
   key.pop()

for k in key:
    rank2csv(k)