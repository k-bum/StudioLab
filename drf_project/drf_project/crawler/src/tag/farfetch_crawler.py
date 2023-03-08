from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import sys
import json
import asyncio
sys.path.append('/Users/kyebeomjeon/workspace/Studio_Lab/Django_Project/drf_git/drf_project')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drf_project.settings")
import django
django.setup()
from crawler.models import *

#'https://www.farfetch.com/kr/shopping/women/clothing-1/items.aspx'
#'https://www.farfetch.com/kr/shopping/men/clothing-2/items.aspx'

def tag_crawler(driver, website) :
    #chrome_options = Options() 
    #chrome_options.headless = True
    #chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')
    #driver = webdriver.Chrome(service = Service('./chromedriver'), options = chrome_options) 

    driver.get(website)
    max_try = 25
    for i in range(max_try):
        body = driver.find_element(By.CSS_SELECTOR, 'body')
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)
        
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')    
    try :
        page_num = int(soup.find('div', class_ = 'ltr-1lxgr2x e9mjthj9').string.split('/')[1].strip())
    except :
        page_num = 1
    #finally :
    #    driver.quit()
    page_num = 1
    page = list(range(1, page_num + 1))
    
    #chrome_options = Options() 
    #chrome_options.headless = True
    #chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')
    #driver = webdriver.Chrome(service = Service('./chromedriver'), options = chrome_options)

    word_dict = {}

    for i in page : 
        url = website + '?page=' + str(i) + '&view=90&sort=3'
        try : 
            driver.get(url)
            time.sleep(30)

            max_try = 25
            for i in range(max_try):
                body = driver.find_element(By.CSS_SELECTOR, 'body')
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(2)
            
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            product_titles = soup.find_all('p', class_ = 'ltr-4y8w0i-Body e1s5vycj0')   
            texts = []
            for i in range(len(product_titles)) :
                if product_titles[i].string != None :
                    words = [x for x in product_titles[i].string.split(' ')]
                    for j in range(len(words)) :
                        texts.append(words[j])
            for item in texts:
                if item in word_dict:
                    word_dict[item] += 1
                else:
                    word_dict[item] = 1
            texts = []
        except : 
            pass
        
    #driver.quit()

    sorted_word_dict = dict(sorted(word_dict.items(), key=lambda x: x[1], reverse=True))
    return sorted_word_dict

def save_dict_to_json(dict_obj):
    # convert dictionary to string
    dict_str = json.dumps(dict_obj, ensure_ascii=False)
    return dict_str

if __name__ == '__main__' :
    instance_id = sys.argv[1]
    instance_project_id = sys.argv[2]
    instance_website = sys.argv[3]
    crawler_object = Crawler.objects.get(id=instance_id)
    project_object = Project.objects.get(id=instance_project_id)

    chrome_options = Options() 
    #chrome_options.headless = True
    #chrome_options.add_argument('--ignore-certificate-errors')
    #chrome_options.add_argument('--no-sandbox')
    #chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')
    driver = webdriver.Chrome(service = Service('./chromedriver'), options = chrome_options)

    sorted_word_dict = tag_crawler(driver, instance_website)
    total_collected = len(sorted_word_dict)
    sorted_word_json = save_dict_to_json(sorted_word_dict)
    crawler_object.collected = total_collected
    crawler_object.expected_total = total_collected
    crawler_object.save()

    Tag(project = project_object,
        crawler = crawler_object,
        tag = sorted_word_json).save()
    
    project_object.expected_total += total_collected
    project_object.collected += total_collected  
    project_object.save()

    crawler_object.state = "Done"
    crawler_object.save()
    driver.quit()

    