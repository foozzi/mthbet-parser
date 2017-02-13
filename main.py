#
# Copyright 2017 <copyright holder> <email>
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# 
#
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
import time

def start():
    driver = webdriver.Firefox()
    driver.set_window_size(1120, 550)
    driver.get("https://www.mthbet28.com/su/virtual-sports/football")
    #time.sleep(8)
    #switch to iframe 1
    frame1 = driver.find_element_by_xpath("//iframe[1]"); 
    driver.switch_to.frame(frame1);
    #switch to iframe 2
    frame2 = driver.find_element_by_xpath("//iframe[1]"); 
    driver.switch_to.frame(frame2);
    print getCurrentTour(driver)
    #html = driver.find_element_by_id('matchdays_container').get_attribute('innerHTML')
    #driver.find_element_by_id("search_button_homepage").click()
    #print html
    driver.quit()

def getCurrentTour(driver):
    tour = driver.find_element_by_id('matchdays_container').find_element_by_class_name('current').get_attribute('innerText')
    if tour:
        return tour
    else:
        print 'Can\'t find current tour'

if __name__ == "__main__":
    start()
