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
from selenium.common.exceptions import NoSuchElementException

import time



class parser():
    parse_tour = 0
    frame1 = ''
    frame2 = ''
    max_kof = 300
    min_kof = 150
    
    def start(self):
        driver = webdriver.Firefox() #or switch to PhantomJS
        driver.set_window_size(1120, 550)
        driver.get("https://www.mthbet28.com/su/virtual-sports/football")
        
        #time.sleep(10)
        i = 1
        time.sleep(3)
        
        driver.switch_to_default_content()
        #switch to iframe 1
        self.frame1 = self.getFrame(driver, "//iframe[1]")
        driver.switch_to.frame(self.frame1)
        #switch to iframe 2
        self.frame2 = self.getFrame(driver, "//iframe[1]")
        driver.switch_to.frame(self.frame2)
        
        current_tour = driver.find_element_by_id('matchdays_container').find_element_by_class_name('current').get_attribute('innerText')
        if current_tour == 30:
            i = 6
        
        while i < 30:
            self.parse_tour = i
            print 'Check ' + str(i) + ' tour'
            driver.switch_to_default_content()
            #switch to iframe 1
            self.frame1 = self.getFrame(driver, "//iframe[1]")
            driver.switch_to.frame(self.frame1)
            #switch to iframe 2
            self.frame2 = self.getFrame(driver, "//iframe[1]")
            driver.switch_to.frame(self.frame2)

            driver.find_element_by_id('matchday' + str(i)).click()
            self.getKofTour(driver)
            i += 1
        driver.quit()
        
    def getFrame(self, driver, frame):
        frame1 = driver.find_element_by_xpath(frame)
        return frame1

    def getCurrentTour(self, driver):
        tour = driver.find_element_by_id('matchdays_container').find_element_by_class_name('current').get_attribute('innerText')
        if tour:
            return tour
        else:
            print 'Can\'t find current tour'
            
    def getKofTour(self, driver):
        match = []
        kofs = []
        driver.switch_to_default_content()
        self.frame1 = self.getFrame(driver, "//iframe[1]")
        driver.switch_to.frame(self.frame1)
        time.sleep(5)
        
        for match in driver.find_elements_by_class_name("rgs-matchlist-item"):
            games_name = match.find_element_by_class_name("matchlist-item-teams").get_attribute('innerText')
            print games_name
            #get kofs
            type_result_i = 0
            for kofs in match.find_elements_by_class_name('matchlist-item-options-container'):
                type_result_i += 1
                # check if exists win kofs
                try:
                    game_kof_result_win_box = kofs.find_element_by_class_name('wonOdd').get_attribute('innerText') 
                    print int(round(float(game_kof_result_win_box)*100))
                except NoSuchElementException:
                    if type_result_i == 3:
                        print 'All ' + str(self.parse_tour) + ' is parsed'
                        driver.quit()
                    else:
                        continue
                    

if __name__ == "__main__":
    Bet = parser()
    Bet.start()
