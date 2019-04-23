

import time
import request
import random
import json

from selenium import webdriver      
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#browser = webdriver.Firefox()#Chrome('./chromedriver.exe')
PATIENCE_TIME = 60
BRANDS = ['nike','jordan','adidas','other']

#return type list per brand
def get_types(brand):
    #account for unique identifiers
    if brand == 'jordan':
        brand = 'retro-jordans'
    elif brand == 'other':
        brand = 'other-sneakers'
    type_list = []
    driver = webdriver.Firefox()
    driver.get("https://stockx.com/{}".format(brand))
    while True:
        try:
            #if load more button present, click!
            loadMoreButton = driver.find_element_by_xpath("//div[@class='subcategory show-more']")
            print loadMoreButton
            time.sleep(2)
            loadMoreButton.click()
            time.sleep(5)
        #else -> continue
        except Exception as e:
            print e
            break
    #capture type divs
    elems = driver.find_elements_by_xpath("//div[@class='subcategoryList']/div[@class='form-group']/div[@class='checkbox subcategory']")
    for elem in elems:
        item = elem.find_element_by_tag_name('label').get_attribute('innerHTML')
        #account for unique identifiers
        if len(item.split(' ')) > 0:
            item = '-'.join(item.split(' '))
        if item == 'Other':
            item = 'footwear'
        if item.isdigit():
            item = 'air-jordan-'+item
        type_list.append(item.lower())
    driver.quit()
    print type_list
    return type_list

def page_information():
    brand_dict = {}
    missing = []
    sneaker_counter = 0
    years = ['before-2001','2001','2002','2003','2004','2005','2006','2007','2008','2009',
             '2010','2011','2012','2013','2014','2015','2016','2017','2018','2019']
    #iterate through brand & types ex. AirForce, Lebron, etc. 
    for b in BRANDS:
        type_dict = {}
        for t in get_types(b):
            page_dict = {}
            for y in years:
                #account for unique identifier
                if b == 'jordan':
                    b = 'retro-jordans'
                print "Starting "+t.capitalize()+" "+y
                #open URL with webdriver
                driver = webdriver.Firefox()
                url    = "https://stockx.com/{}/{}".format(b,t)+"?years="+y
                result = True
                time.sleep(5)
                driver.get(url)
                try:
                    no_result = driver.find_element_by_xpath(".//div[@class='no-results']")
                    check     = no_result.get_attribute("innerHTML").split(' ')[0]
                    if check == "NOTHING":
                        print 'No results found. Going to next page.'
                        driver.quit()
                        continue
                except NoSuchElementException as e:
                    result = True
                    print e
                if result:
                    #while True, Search for presence of loading button
                    page_counter = 0
                    while True:
                        try:
                            #wait for presence of load more button
                            WebDriverWait(driver, 30).until(
                                EC.text_to_be_present_in_element((By.XPATH, "//button[@class='btn btn-default']"), "Load More"))
                            print "Found Button!"
                            loadMoreButton = driver.find_element_by_xpath("//button[@class='btn btn-default']")
                            print "Clicking..."
                            loadMoreButton.click()
                            time.sleep(5)
                        except Exception as e:
                            print "Load More Not Found...Continuing"
                            break
                    print "Beginning Extraction"
                    #capture divs loaded from fully loaded page
                    elems = driver.find_elements_by_xpath("//div[@class='browse-grid']/div[@class='tile browse-tile']/div[@class='Tile__Card-sc-1tqri8b-0 cxXLSM']")
                    #search divs for name,href,src
                    for elem in elems:
                        sneaker_counter+=1
                        page_counter+=1
                        #contains parent div
                        href      = elem.find_element_by_tag_name('a').get_attribute("href")
                        #search for //div/img
                        img_tag   = elem.find_element_by_xpath(".//div[@class='TileImage-lflzuh-0 gzWegR']").get_attribute("innerHTML")
                        #extract img_src and name
                        img       = img_tag.split('"')
                        name, src = img[1], img[3]
                        print name
                        #write to dict
                        data = {
                            "src": src,
                            "href": href
                        }
                        page_dict[name] = data
                        #exit driver
                        time.sleep(1/(random.randint(1,100)*10000))
                    #if scraper encounters an error, the count will be zero
                    #identify what page is missing
                    if page_counter == 0:
                        missing.append([[b,t,y]])
                    driver.quit()
                    print 'Total Count: '+str(sneaker_counter)
            #seed page_dict[name] into type_dict
            type_dict[t] = page_dict
            print "SEEDING TYPE..."
        #seed type_dict into total
        brand_dict[b] = type_dict
        print "SEEDING BRANDS..."
    #return final dictionary
    with open('total.json', 'w') as outfile:  
        json.dump(brand_dict, outfile, indent=4)
    with open('missing.json', 'w') as outfile:  
        json.dump(missing, outfile, indent=4)
    print "Complete."
    print missing

if __name__ == "__main__":
    page_information()