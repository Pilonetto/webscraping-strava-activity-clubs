# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 10:29:35 2021

@author: marlon
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import time
import pandas as pd
import pickle

def scrollpage():
    SCROLL_PAUSE_TIME = 5
    
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
    
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height    
        
def checkEndLoad():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        time.sleep(10)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print('End Scroll')
            break
        last_height = new_height 
        


options = Options()
options.headless = True
options.add_argument('window-size=1920x1080')

LOGIN = 'https://www.strava.com/login'
CLUB = '''https://www.strava.com/clubs/%s/recent_activity''' % (CODE_CLUB)

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(LOGIN)

mail = driver.find_element_by_id("email")
pw = driver.find_element_by_id("password")


driver.execute_script("arguments[0].setAttribute('value','YOUR-EMAIL')", mail)
driver.execute_script("arguments[0].setAttribute('value','YOUR-PASSWORD')", pw)

time.sleep(1)
accept = driver.find_element_by_id('login-button')
accept.click()


for i in range(1,5):
    print('waiting ', i)
    time.sleep(1)
    
driver.get(CLUB)   

scrollpage() 

checkEndLoad()

activitys = driver.find_elements_by_xpath("//div[@class='activity entity-details feed-entry']")

groupactivitys = driver.find_elements_by_xpath("//div[@class='feed-entry group-activity']")


data = []
kmmask = '''//*[@id="%s"]/div[2]/div[2]/ul/li[1]'''
elevmask = '''//*[@id="%s"]/div[2]/div[2]/ul/li[2]'''
tempmask = '''//*[@id="%s"]/div[2]/div[2]/ul/li[3]'''
othermask = '''//*[@id="%s"]/div[2]/div[2]/ul/li[4]'''

for activity in activitys:
    code = activity.get_attribute('id')
    name = activity.find_element_by_class_name('entry-athlete').text
    atcode = activity.find_element_by_class_name('entry-athlete'). get_attribute('href').replace('https://www.strava.com/athletes/','')
    
    hora = activity.find_element_by_class_name("timestamp").text.split('·')
    desc = activity.find_element_by_tag_name("strong").text
    
    km = activity.find_element_by_xpath(kmmask % (code)).text
    if km == 'Treino':
       km = activity.find_element_by_xpath(elevmask % (code)).text 
       elev = activity.find_element_by_xpath(tempmask % (code)).text
       tempo = activity.find_element_by_xpath(othermask % (code)).text
    else:   
        elev = activity.find_element_by_xpath(elevmask % (code)).text
        #elev = activity.find_element_by_xpath('//*[@title="Ganho de elev."]').text
        tempo = activity.find_element_by_xpath(tempmask % (code)).text
    
    data.append([code,atcode,name,hora[0],hora[1],desc,km,elev, tempo,'I' ])
    print( desc)
    
for groupactivity in groupactivitys:
    entries = groupactivity.find_elements_by_xpath("//ul[@class='list-entries']")  
    hora = groupactivity.find_element_by_class_name("timestamp").text.split('·')
    desc = groupactivity.find_element_by_tag_name("strong").text
    print( desc)
    for entrie in entries:
        activitys = entrie.find_elements_by_xpath("//li[@class='entity-details feed-entry']")
        for activity in activitys:
            code = activity.get_attribute('id')
            name = activity.find_element_by_class_name('entry-athlete').text
            atcode = activity.find_element_by_class_name('entry-athlete'). get_attribute('href').replace('https://www.strava.com/athletes/','')
            

            
            km = activity.find_element_by_xpath(kmmask % (code)).text
            if km == 'Treino':
               km = activity.find_element_by_xpath(elevmask % (code)).text 
               elev = activity.find_element_by_xpath(tempmask % (code)).text
               tempo = activity.find_element_by_xpath(othermask % (code)).text
            else:   
                elev = activity.find_element_by_xpath(elevmask % (code)).text
                #elev = activity.find_element_by_xpath('//*[@title="Ganho de elev."]').text
                tempo = activity.find_element_by_xpath(tempmask % (code)).text
            
            data.append([code,atcode,name,hora[0],hora[1],desc,km,elev, tempo,'G' ])
        
       

df = pd.DataFrame(data=data, columns = ['activity-id','athlete-id','athlete','timestamp','location', 'activity','distance', 'elevation', 'duration','type' ])



def adjust_dt(dt):
    
    if "Hoje" in dt:
        d = dt.split(' ')
        ds = datetime.today()
        ds.day
        data = datetime(ds.year, ds.month, ds.day,int(d[2].split(':')[0]),int(d[2].split(':')[1]) )
    elif "Ontem" in dt:        
        d = dt.split(' ')
        ds = datetime.today() - timedelta(days=1)
        ds.day
        data = datetime(ds.year, ds.month, ds.day,int(d[2].split(':')[0]),int(d[2].split(':')[1]) )
    else:        
        dtt = dt.split(' ')
        mt = 12
        if dtt[2].lower() == 'janeiro':
            mt = 1
        elif dtt[2].lower() == 'fevereiro':
            mt = 2   
        elif dtt[2].lower() == 'março':
            mt = 3    
        elif dtt[2].lower() == 'maio':
            mt = 4               
        elif dtt[2].lower() == 'abril':
            mt = 5   
        elif dtt[2].lower() == 'junho':
            mt = 6
        elif dtt[2].lower() == 'julho':
            mt = 7   
        elif dtt[2].lower() == 'agosto':
            mt = 8              
        elif dtt[2].lower() == 'setembro':
            mt = 9            
        elif dtt[2].lower() == 'outubro':
            mt = 10             
        elif dtt[2].lower() == 'novembro':
            mt = 11
        else:
            mt = 12
        data = datetime(int(dtt[4]), mt, int(dtt[0]),int(dtt[6].split(':')[0]),int(dtt[6].split(':')[1]) )
    return data   

def adjust_km(km):
    if "km" in km:
        km = float(km.replace(' km', '').replace(',','.')) * 1000
    elif "Treino" in km:
        km = 0
    else:
        km = float(km.replace(' m', '').replace(',','.')) 
    return km

df['Date'] = df['timestamp'].apply(adjust_dt)
df['metros'] = df['distance'].apply(adjust_km)
df['elevation'] = df['elevation'].apply(lambda x: x.replace(' m', ''))

df.to_csv('activitys.csv',sep=';',decimal= ',', index=False)




