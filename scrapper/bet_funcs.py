
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
driver.get("")


    
first_team = WebDriverWait(driver, 20).until(ec.visibility_of_all_elements_located(
    (By.XPATH, "//*[@id='quick-game-matche-container']/div[5]/div[1] //*[contains(@class, 'teams-cell')]//span[1]")))
second_team = WebDriverWait(driver, 20).until(ec.visibility_of_all_elements_located(
    (By.XPATH, "//*[@id='quick-game-matche-container']/div[5]/div[1]//*[contains(@class, 'teams-cell')]//span[3]")))
odds = WebDriverWait(driver, 20).until(ec.visibility_of_all_elements_located(
    (By.XPATH, "//*[@id='quick-game-matche-container']/div[5]/div[1] //*[contains(@class, 'iw-outcome')]//span[1]")))


one_odds = odds[::3]
two_odds = odds[2::3]
arr_one = []
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

for i, (a, b) in enumerate(zip(arr_one, without_draw)):
    if a == 'MCI':
        b.click()
        if ((i+1) % 2 == 0):
            home_odds = (without_draw[i-1]).text
            away_odds = (without_draw[i]).text
            away_team = a
            home_team = (arr_one[i-1])
        else:
            away_odds = (without_draw[i+1]).text
            home_odds = (without_draw[i]).text
            home_team = a
            away_team = (arr_one[i+1])

print(home_team, home_odds, away_team, away_odds)


odds_input = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="quick-bet-container"]/div/div[2]/div[1]/div[2]/div[2]/div[2]/div/div/div/span')))

odds_input.click()
keys = WebDriverWait(driver, 20).until(ec.visibility_of_any_elements_located(
    (By.XPATH, "//span[contains(@class, 'm-keyboard-key')]")))

(keys[13]).click()

def keys_input(i):
    keys = WebDriverWait(driver, 20).until(ec.visibility_of_any_elements_located(
    (By.XPATH, "//span[contains(@class, 'm-keyboard-key')]")))

    keys_dict={1:0,2:1,3:2,4:3,5:4,6:5,7:7,8:8,9:9,0:10,'.':11}    
    for key,value in keys_dict.items():
        if(str(key)==str(i)):
            (keys[value]).click()
            return True
                  
def get_odds(odds):
    my_list = []
    for x in str(odds):
        my_list.append(x)        
    
    for i in my_list:
        keys_input(i)

get_odds(2.06)

place_bet = WebDriverWait(driver, 10).until(
    ec.visibility_of_element_located((By.XPATH, '//*[@id="quick-bet-container"]/div/div[3]/div[2]/div/div[2]')))

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
elif home_result == away_result:
    print('Draw with odds', home_odds, '', away_odds)
else:
    print(away_team, 'won with odds', away_odds)

next_round = WebDriverWait(driver, 10).until(ec.visibility_of_element_located(
    (By.CSS_SELECTOR, '#iv-live-score-result > div.btn-nav-bottom > div.nav-bottom-right > span > div > div:nth-child(1)')))
next_round.click()
    



