import time
import random
import shutil
import requests
import argparse

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup as bs

def driver(driver_path):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(driver_path, options = options)
    return driver

def search_pinterest(search_text):
    chrome = driver('chromedriver.exe')
    chrome.get('https://www.pinterest.com/pin/798122365205129040/')
    
    search = chrome.find_element_by_xpath('//*[@id="__PWS_ROOT__"]/div/div/div/div[2]/div[1]/div/div[2]/div/div/form/div/div[1]/div[2]/div/input')
    search.send_keys(search_text + Keys.ENTER)
    time.sleep(random.random())

    html = chrome.page_source
    source = bs(html)

    # add scrolling algorithm following number of images to scrape
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    urls = [block.get('src') for block in source.find_all('img') if block.get('src').startswith('https://i.pinimg.com')]
    driver.close()

    return urls

def search_google(search_text):
    chrome = driver('chromedriver.exe')
    chrome.get('https://www.google.com/imghp')

    search = chrome.find_element_by_xpath('//*[@id="sbtc"]/div/div[2]/input')
    search.send_keys(search_text + Keys.ENTER)

    urls = []
    num = 1

    # add scraping for multiple images

    for i in range(num):
        img = driver.find_element_by_xpath(f'//*[@id="islrg"]/div[1]/div[{i}]/a[1]/div[1]/img')
        img.click()
        time.sleep(random.random())

        image_url = driver.find_elements_by_class_name('n3VNCb')
        if image_url.get_attribute('src')[:4].lower() == 'http':
            urls.append(image_url)

    return urls

def download(url, save_dir):
    response = requests.get(url, stream = True)
    if response.status_code == 200:
        response.raw.decode_content = True

        with open(url.split('/')[-1], 'wb') as f:
            shutil.copyfileobj(response.raw, f'{save_dir}/f')
            print('image downloaded')
    else:
        print("could not retrieve image")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', 
                        '--text', 
                        default = None)
    parser.add_argument('-e', 
                        '--engine', 
                        default = 'google')
    parser.add_argument('-s', 
                        '--save_dir', 
                        default = './images')
    args = parser.parse_args()

    if args.engine == 'google':
        result = search_google(args.text)
    else:
        result = search_pinterest(args.text)

    for url in result:
        download(url, args.save_dir)
    
if __name__ == '__main__':
    main()