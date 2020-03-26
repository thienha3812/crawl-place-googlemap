from flask_api import FlaskAPI
from flask import request 
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located,visibility_of,visibility_of_element_located,visibility_of_all_elements_located
from  time import sleep
import sys
import re



app = FlaskAPI(__name__)



@app.route("/searchplace", methods = ['POST'])
def index():
    try:
        query = request.get_json()["query"]
        lat = request.get_json()["lat"]
        lng = request.get_json()["lng"]
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        option.add_argument("--enable-logging --v=1")
        d = DesiredCapabilities.CHROME
        d['goog:loggingPrefs'] = { 'browser':'ALL' }
        with webdriver.Chrome(executable_path='./chromedriver',options=option,desired_capabilities=d) as driver:
            wait = WebDriverWait(driver, 10)
            driver.get("https://www.google.com/maps/search/{}/@{},{}z?hl=vi-VN".format(query,lat,lng))        
            wait.until(visibility_of_element_located((By.CLASS_NAME, "section-result-content")))        
            section_content = driver.find_elements_by_class_name("section-result-content")        
            result = []
            for i in section_content:                       
                title  = i.find_element_by_class_name("section-result-title")
                img  = i.find_element_by_class_name("section-image-container ")       
                address = i.find_element_by_class_name('section-result-location')            
                detail = i.find_element_by_class_name('section-result-details')
                regex = '(?<=url\()(?s)(.*)(?=\)"\sjsan)'
                match = re.search(regex,img.get_attribute('innerHTML'))
                result.append({"title": title.text,"img":match.group(),"address":address.text,"detail":detail.text})            
        return result
    except:
        pass 


if __name__ == "__main__":
    app.run(debug=True)