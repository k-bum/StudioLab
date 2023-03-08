from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import urllib.request
import time
import os, sys
sys.path.append('/Users/kyebeomjeon/workspace/Studio_Lab/Django_Project/drf_git/drf_project')

#sys.path.append(os.getcwd())
#sys.path.append('C:\\Users\\user\\anaconda3')
#print(f"sys.path:{sys.path}")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drf_project.settings")
import django
django.setup()
from crawler.models import *

#https://www.farfetch.com/kr/shopping/women/search/items.aspx
#https://www.farfetch.com/kr/shopping/men/search/items.aspx
def page_crawler(driver, keyword, website) :

    #chrome_options = Options() 
    #chrome_options.headless = True
    #chrome_options.add_argument('--ignore-certificate-errors')
    #chrome_options.add_argument('--no-sandbox')
    #chrome_options.add_argument('--disable-dev-shm-usage')
    #chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')
    #driver = webdriver.Chrome(service = Service('./chromedriver'), options = chrome_options) 
    driver.get(website + '?page=1&view=90&sort=3&scale=279&q=' + keyword + '&category=135967')
    
    max_try = 25
    for i in range(max_try):
        body = driver.find_element(By.CSS_SELECTOR, 'body')
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    try :    
        page_num = int(soup.find('div', class_ = 'ltr-1lxgr2x e9mjthj9').string.split('/')[1].strip())
    #print(page_num)
    except :
        page_num = 1
    #page_num = 1
    page = list(range(1, page_num + 1))
    #driver.quit()

    #chrome_options = Options() 
    #chrome_options.headless = True
    #chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')
    #driver = webdriver.Chrome(service = Service('./chromedriver'), options = chrome_options)

    href = []
    for i in page :
        try : 
            page_url = website + '?page='+ str(i) + '&view=90&sort=3&scale=279&q=' + keyword + '&category=135967'
            driver.get(page_url)
            time.sleep(30)

            max_try = 25
            for i in range(max_try):
                body = driver.find_element(By.CSS_SELECTOR, 'body')
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(2)

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            product_titles = soup.find_all('a', class_ = 'ltr-1gxq4h9 e4l1wga0')

            for i in product_titles :
                href.append('http://www.farfetch.com' + i.attrs['href'])
        except :
            pass

    #driver.quit()
    return href

def image_crawler(driver, href) :
    #chrome_options = Options() 
    #chrome_options.headless = True
    #chrome_options.add_argument('--ignore-certificate-errors')
    #chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')
    #driver = webdriver.Chrome(service = Service('./chromedriver'), options = chrome_options) 
    img_url = []
    img_dict = {}
    
    for i in range(0, len(href)) :
        try :
            driver.get(href[i])
            time.sleep(10)
    
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
    
            images = soup.find_all('img', class_ = 'ltr-sglqoc e2u0eu40')
    
            name = soup.find('a', class_ = 'ltr-jtdb6u-Body-Heading-HeadingBold e1h8dali1').get_text()
            product_id = soup.select_one('#tabpanel-0 > div > div.ltr-15eja7h.exjav152 > div > div:nth-child(4) > p:nth-child(2) > span').get_text()
            for image in images :
                url = image.get('src')
                img_url.append(url)
        
            for index, url in enumerate(img_url) :
                img_dict[name + '_' + product_id + '_' + str(index)] = url

            img_url = []

        except :
            pass

    #driver.quit()
    return img_dict

def save_image(url, file_path) :
    urllib.request.urlretrieve(url, file_path)
    
if __name__ == '__main__' : 
    instance_id = sys.argv[1]
    instance_project_id = sys.argv[2]
    instance_website = sys.argv[3]
    instance_keyword = sys.argv[4]
    crawler_object = Crawler.objects.get(id=instance_id)
    project_object = Project.objects.get(id=instance_project_id)
    keyword = instance_keyword.strip()

    chrome_options = Options() 
    #chrome_options.headless = True
    #chrome_options.add_argument('--ignore-certificate-errors')
    #chrome_options.add_argument('--no-sandbox')
    #chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')
    driver = webdriver.Chrome(service = Service('./chromedriver'), options = chrome_options)
    
    href = page_crawler(driver, keyword, instance_website)
    expected = len(href) * 4
    crawler_object.expected_total = expected
    project_object.expected_total += expected
    crawler_object.save()
    project_object.save()
    img_dict = image_crawler(driver, href)
    for name, url in img_dict.items() :
        file_path='./images/' + name + '.jpg'
        save_image(url, file_path)
        crawler_object.collected += 1
        project_object.collected += 1
        crawler_object.save()
        project_object.save()
        Image(project = project_object,
        crawler = crawler_object,
        url = url,
        save_path = file_path).save()

    crawler_object.state = "Done"
    crawler_object.save()
    driver.quit()

    