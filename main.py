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
from selenium.common.exceptions import NoSuchElementException
import re
import time
import sys  
import sqlite3
from datetime import datetime, date


class parser():
    reload(sys)  
    sys.setdefaultencoding('utf-8')
    
    parse_tour = 0
    frame1 = ''
    frame2 = ''
    max_kof = 2500
    min_kof = 300
    season = 0

    con = ''
    
    def start(self):
        driver = webdriver.PhantomJS() #or switch to PhantomJS
        driver.set_window_size(1120, 800)
        driver.get("https://www.mthbet28.com/su/virtual-sports/football")

        self.con = sqlite3.connect('bets.db')

        # create table win_bets if not exists
        self.con.cursor()
        self.con.execute(
            'CREATE TABLE IF NOT EXISTS win_bets (id INTEGER PRIMARY KEY, season INTEGER, tour INTEGER, kof INTEGER, date_parse DATE)')
        self.con.commit()
                
        i = 1
        time.sleep(5)
        
        driver.switch_to_default_content()
        #switch to iframe 1
        self.frame1 = self.getFrame(driver, "//iframe[1]")
        driver.switch_to.frame(self.frame1)
        #switch to iframe 2
        self.frame2 = self.getFrame(driver, "//iframe[1]")
        driver.switch_to.frame(self.frame2)
        
        self.season = driver.find_element_by_id('tab_season').get_attribute('innerText')
        self.season = int(filter(str.isdigit, str(self.season)))
        print self.season
        
        current_tour = driver.find_element_by_id('matchdays_container').find_element_by_class_name('current').get_attribute('innerText')
        if int(current_tour) == 30:
            i = 6
        
        while i <= 30:
            self.parse_tour = i
            print 'Check ' + str(i) + ' tour'
            driver.switch_to_default_content()
            #switch to iframe 1
            self.frame1 = self.getFrame(driver, "//iframe[1]")
            driver.switch_to.frame(self.frame1)
            #switch to iframe 2
            self.frame2 = self.getFrame(driver, "//iframe[1]")
            driver.switch_to.frame(self.frame2)
            tour = driver.find_element_by_id('matchday' + str(i))
            #dont check current and not played games
            m = re.search('notPlayedYet|current', tour.get_attribute('class'))
            if m == None:
                print driver.find_element_by_id('matchday' + str(i)).get_attribute('innerText')
                driver.find_element_by_id('matchday' + str(i)).click()
                self.getKofTour(driver)
            i += 1
        self.con.close()
        driver.quit()
        
    def getFrame(self, driver, frame):
        frame1 = driver.find_element_by_xpath(frame)
        return frame1
            
    def getKofTour(self, driver):
        match = []
        kofs = []
        driver.switch_to_default_content()
        self.frame1 = self.getFrame(driver, "//iframe[1]")
        driver.switch_to.frame(self.frame1)
        time.sleep(5)

        matchlist_container = driver.find_element_by_id('rgs-matchlist-container')
        
        # for incr xpath
        i_c = 1

        for match in matchlist_container.find_elements_by_class_name("rgs-matchlist-item"):
            games_name = match.find_element_by_class_name("matchlist-item-teams").get_attribute('innerText')
            print games_name                

            # incr xpath
            number_matchlist_container = i_c * 3
            i_c += 1

            matchlist_item_option_container = match.find_element_by_xpath("(//div[@class='matchlist-item-options-container 3way'])["+str(number_matchlist_container)+"]")
            matchlist_betting_options = matchlist_item_option_container.find_element_by_class_name('matchlist-betting-options')


            for total_kofs_box in matchlist_betting_options.find_elements_by_tag_name("label"):
                # check if exists win kofs
                # game_kof_result_win_box = total_result_box.find_element_by_class_name('wonOdd').get_attribute('innerText') 
                # self.checkWinSeries(int(round(float(game_kof_result_win_box)*100)))
                game_kof_result_win_box = 0

                game_kof_result_not_win_box = total_kofs_box.get_attribute('class') 

                m = re.search('wonOdd', game_kof_result_not_win_box)
                if m == None:
                    game_kof_result_win_box = total_kofs_box.get_attribute('innerText')
                    kof = int(round(float(game_kof_result_win_box)*100))
                    self.checkIfExistsKof(kof)
                    self.checkAndSaveNotWinSeries(kof)

                        
                    
    def checkAndSaveNotWinSeries(self, kof):
        print kof
        if self.min_kof <= kof:
            if self.max_kof >= kof:
                self.con.execute(
                    'INSERT INTO win_bets VALUES(NULL, ?, ?, ?, ?)', (self.season, self.parse_tour, kof, datetime.now()))
                self.con.commit()

    def checkIfExistsKof(self, kof):
        self.con.execute(
            'SELECT id FROM win_bets WHERE season = ? AND tour = ? AND kof = ?', (self.season, self.parse_tour, kof))
        data = self.con.fetchone()
        print data[0]

    # def checkWinSeries(self, kof):
    #     if self.min_kof <= kof:
    #         if self.max_kof >= kof:
    #             print kof
    #             file = open("./kofs_win", "w")
    #             file.write('Season: ' + str(self.season) + ' Tour:' + str(self.parse_tour) + ' Kof. win:' + str(kof))
    #             #file.write('\n')
    #             file.close()

if __name__ == "__main__":
    Bet = parser()
    Bet.start()
