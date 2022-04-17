from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import csv
import pandas as pd


from selenium.webdriver.common.keys import Keys
import time

def scrape(webaddress):
    vgm_url = webaddress
    html_text = requests.get(vgm_url).text
    soup = BeautifulSoup(html_text, features="lxml")
    blocklist = soup.find_all("div", class_='usa-media_block-body')
    for eachvalue in blocklist:
        if eachvalue.find("h3") is not None:
            print(eachvalue.find("h3").text)
            print(eachvalue.find("p").text)
    print(len(blocklist))

def seleniumscrape(webaddress):
    infodict = dict()
    finallist = []
    options = Options()
    options.headless = True
    try:
        driver = webdriver.Firefox(options=options, executable_path='driver/geckodriver')
        # driver = webdriver.Firefox(executable_path='driver/geckodriver')
        driver.get(webaddress)
        elements = driver.find_element_by_class_name("usa-accordion-bordered").find_elements_by_tag_name('li')
        for e in elements:
            e.click()
            for university, course in zip(e.find_elements_by_tag_name("a"), e.find_elements_by_tag_name("p")):
                infodict["UniversityName"] = university.text
                infodict["CourseName"] = course.text
                print(infodict)
                finallist.append(infodict)
            # for univeristy, coursename in zip(e.find_element_by_class_name("usa-accordion-content").find_elements_by_tag_name('a'),
            #                                   e.find_element_by_class_name("usa-accordion-content").find_elements_by_tag_name('p')):
            #     infodict["UniversityName"] = univeristy.text
            #     infodict["CourseName"] = coursename.text
            #     print(infodict)


        print(finallist)
    finally:
        driver.quit()





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    seleniumscrape('https://training.fema.gov/hiedu/collegelist/')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
