from decimal import Decimal

import time
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

opt = Options()
opt.add_experimental_option("debuggerAddress", "localhost:9222")

service = Service(executable_path="Drivers/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=opt)

driver.switch_to.new_window('tab')
driver.get("https://www.sportybet.com/ke/m/sporty-instant-virtuals/quickgame")

URL = "http://127.0.0.1:8000/bets/"

def post_to_api(progression,result,stake,odds,total_lost):
        try:
            jsonData = {"progression":progression,"result": result, "stake": stake,"odds": odds,"total_lost": total_lost}
            requests.post(URL, data=jsonData)
            return True
        except:
            print('exception')
            return False


def func():
    # switch to double chance
    d_chance = WebDriverWait(driver, 20).until(ec.visibility_of_element_located(
        (By.XPATH, '//*[@id="quick-game-matche-container"]/div[3]/ul/li[4]')))
    d_chance.click()
    # ac_balance = WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.XPATH,'//*[@id="quick-game-matche-container"]/div[1]/div[2]/div/div/span')))
    first_team = WebDriverWait(driver, 20).until(ec.visibility_of_all_elements_located(
        (By.XPATH, "//*[@id='quick-game-matche-container']/div[5]/div[1] //*[contains(@class, 'teams-cell')]//span[1]")))
    second_team = WebDriverWait(driver, 20).until(ec.visibility_of_all_elements_located(
        (By.XPATH, "//*[@id='quick-game-matche-container']/div[5]/div[1]//*[contains(@class, 'teams-cell')]//span[3]")))
    odds = WebDriverWait(driver, 20).until(ec.visibility_of_all_elements_located(
        (By.XPATH, "//*[@id='quick-game-matche-container']/div[5]/div[1] //*[contains(@class, 'iw-outcome')]//span[1]")))

    arr_one = []

    one_odds = odds[::3]
    two_odds = odds[2::3]
    without_draw = []

    for f, b in zip(one_odds, two_odds):
        without_draw.append(f)
        without_draw.append(b)

    for f, b in zip(first_team, second_team):
        arr_one.append(f.text)
        arr_one.append(b.text)

    # save home and away teams
    home_team = ''
    home_odds = ''
    away_team = ''
    away_odds = ''
    

    diff_list = []
    
    for index,( x, y )in enumerate (zip(without_draw[0::], without_draw[1::])):
        if(index%2 ==0):
            diff_list.append(abs(Decimal(y.text) - Decimal(x.text)))
          
        
    odd_index=(diff_list.index(min(diff_list)))    
    equal_odd_team=(arr_one[odd_index*2])
    print(diff_list)
    for i, (a, b) in enumerate(zip(arr_one, without_draw)):

        if a == equal_odd_team:
            b.click()
            (WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="quick-bet-container"]/div/div[1]/img')))).click()
            
            (without_draw[i+1]).click()
            (WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="quick-bet-container"]/div/div[1]/img')))).click()
            
            away_odds = (without_draw[i+1]).text
            home_odds = (without_draw[i]).text
            home_team = a
            away_team = (arr_one[i+1])

    print(home_team, home_odds, away_team, away_odds)

    input_container=(WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="quick-game-matche-container"]/div[6]/div[2]/span'))))
    input_container.click()
    

    first_odd_input=(WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="betslip-container"]/div[3]/div[1]/div[1]/div[2]/div[2]/div[2]/div/div/div/div[1]/span[2]'))))
    first_odd_input.click()
    
    keys = WebDriverWait(driver, 20).until(ec.visibility_of_any_elements_located(
        (By.XPATH, "//span[contains(@class, 'm-keyboard-key')]")))

    (keys[13]).click()
    # the first amount is always for the home team (or the first progression)
    (keys[0]).click()
    
    # click done on the keyboard
    done_input=(WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="betslip-container"]/div[3]/div[1]/div[1]/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[2]/span'))))
    done_input.click()
    
    second_odd_input=(WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="betslip-container"]/div[3]/div[1]/div[2]/div[2]/div[2]/div[2]/div/div/div/div[1]/span[2]'))))
    second_odd_input.click()
    keys = WebDriverWait(driver, 20).until(ec.visibility_of_any_elements_located((By.XPATH, "//span[contains(@class, 'm-keyboard-key')]")))

    (keys[13]).click()
    (keys[0]).click()

    
    place_bet = WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, '#bet-btn > p:nth-child(2)')))

    place_bet.click()

    confirm = WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.XPATH, '//*[@id="confirm-btn"]')))
    confirm.click()
    try:
        kick_off = WebDriverWait(driver, 10).until(ec.visibility_of_element_located(
            (By.CSS_SELECTOR, '#open-bets-container > div.btn-nav-bottom > div.nav-bottom-right > span > span')))
        kick_off.click()
    except:
        kick_off = WebDriverWait(driver, 10).until(ec.visibility_of_element_located(
            (By.CSS_SELECTOR, '#open-bets-container > div.btn-nav-bottom > div.nav-bottom-right > span > span')))
        kick_off.click()

    skip_to_result = WebDriverWait(driver, 10).until(ec.visibility_of_element_located(
        (By.CSS_SELECTOR, '#iv-live-score-running > div.bottom')))
    skip_to_result.click()

    for i in range(10):
        imgs = WebDriverWait(driver, 10).until(
            ec.visibility_of_any_elements_located((By.TAG_NAME, 'img')))
        try:
            if (imgs[2]):
                time.sleep(1)
        except:
            break

    # get results for both stakes
    results = WebDriverWait(driver, 10).until(
        ec.visibility_of_all_elements_located((By.CLASS_NAME, 'score')))
    home_result = (results[0]).text
    away_result = (results[1]).text

    if home_result > away_result:
        print(home_team, 'won with odds', home_odds)
        post_to_api(0,'w',1,home_odds,0)
        post_to_api(1,'l',1,away_odds,0)
        
    elif home_result == away_result:
        print('Draw with odds', home_odds, '', away_odds)
        post_to_api(0,'d',1,home_odds,0)
        post_to_api(1,'d',1,away_odds,0)

    else:
        print(away_team, 'won with odds', away_odds)
        post_to_api(0,'l',1,home_odds,0)
        post_to_api(1,'w',1,away_odds,0)


    next_round = WebDriverWait(driver, 10).until(ec.visibility_of_element_located(
        (By.CSS_SELECTOR, '#iv-live-score-result > div.btn-nav-bottom > div.nav-bottom-right > span > div > div:nth-child(1)')))
    next_round.click()
func()