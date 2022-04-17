from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import csv
import pandas as pd
import time


def seleniumscrape(webaddress):
    finallistdict = {}
    options = Options()
    dataList = []
    options.headless = True
    driver = webdriver.Firefox(options=options, executable_path='driver/geckodriver')
    try:
        # driver = webdriver.Firefox(options=options, executable_path='driver/geckodriver')
        # driver = webdriver.Firefox(executable_path='driver/geckodriver')
        driver.get(webaddress)
        elements = driver.find_element_by_class_name("usa-accordion-bordered").find_elements_by_tag_name('li')
        for e in elements:
            coursePerUniveristy=[]
            e.click()
            for university, course in zip(e.find_elements_by_tag_name("a"), e.find_elements_by_tag_name("p")):
                coursePerUniveristy.append(course.text)
            finallistdict[university.text] = coursePerUniveristy
        driver.quit()

        # for coursecount in range(1, len(finallist)+1):
        #     driver = webdriver.Firefox(options=options, executable_path='driver/geckodriver')
        #     driver.get(webaddress)
        #     time.sleep(2)
        #     course=driver.find_element_by_id("ctl00_ctl00_ContentMain_"+str(coursecount))
        #     print(course.text)
        #     # driver.find_element_by_id("ctl00_ctl00_ContentMain_backButton").click()
        #     driver.quit()
        for eachUnivesirty in range(len(finallistdict.keys())):
            for eachcours in range(len(finallistdict[list(finallistdict.keys())[eachUnivesirty]])):
                datadict = {}
                driver = webdriver.Firefox(options=options, executable_path='driver/geckodriver')
                driver.get(webaddress)
                driver.find_element_by_class_name("usa-accordion-bordered").find_elements_by_tag_name(
                    'li')[eachUnivesirty].click()
                driver.find_element_by_class_name("usa-accordion-bordered").find_elements_by_tag_name(
                    'li')[eachUnivesirty].find_elements_by_tag_name("a")[eachcours].click()
                datadict["University Name"] = driver.find_element_by_id("ctl00_ctl00_ContentTitle_progDescHeader").text
                datadict["Course Name"] = driver.find_element_by_id("ctl00_ctl00_ContentTitle_progDescTitle").text
                datadict["Description"] = driver.find_element_by_id("ctl00_ctl00_ContentMain_progDescPara1").text
                datadict["Degree"] = driver.find_element_by_id("ctl00_ctl00_ContentMain_progDescDegree").text
                datadict["Internship"] = driver.find_element_by_id("ctl00_ctl00_ContentMain_progDescInternDetail").text
                datadict["Accreditation"] = driver.find_element_by_id("ctl00_ctl00_ContentMain_progDescAccred").text
                datadict["URL"] = driver.find_element_by_id("ctl00_ctl00_ContentMain_progDescWeb").text
                datadict["Last Update"] = driver.find_element_by_id("ctl00_ctl00_ContentMain_progDescUpdateDate").text
                dataList.append(datadict)
                driver.quit()
                print(dataList)

        df = pd.DataFrame(dataList)
        df.to_csv("Data.csv")


    finally:
        driver.quit()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    seleniumscrape('https://training.fema.gov/hiedu/collegelist/')
