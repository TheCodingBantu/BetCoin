
import time
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
while True:
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

    for i, (a, b) in enumerate(zip(arr_one, without_draw)):
        if a == 'ARS':
            b.click()
            if ((i+1) % 2 == 0):
                (without_draw[i-1]).click()
                home_odds = (without_draw[i-1]).text
                away_odds = (without_draw[i]).text
                away_team = a
                home_team = (arr_one[i-1])
            else:
                (without_draw[i+1]).click()
                away_odds = (without_draw[i+1]).text
                home_odds = (without_draw[i]).text
                home_team = a
                away_team = (arr_one[i+1])

    print(home_team, home_odds, away_team, away_odds)

    # # open the odds input
    input_container = WebDriverWait(driver, 10).until(ec.visibility_of_element_located(
        (By.XPATH, '//*[@id="quick-bet-container"]/div/div[2]/div[1]/span')))
    input_container.click()
    singles = WebDriverWait(driver, 10).until(ec.visibility_of_element_located(
        (By.CSS_SELECTOR, '#bet-type-tab > div:nth-child(1)')))
    singles.click()
    # odds_input = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="quick-bet-container"]/div/div[2]/div[1]/div[2]/div[2]/div[2]/div/div/div/span')))
    double_odds_input = WebDriverWait(driver, 10).until(
        ec.visibility_of_all_elements_located((By.CLASS_NAME, 'm-keybord-input')))

    # # odds_input.click()

    # # clear btn

    (double_odds_input[0]).click()

    keys = WebDriverWait(driver, 20).until(ec.visibility_of_any_elements_located(
        (By.XPATH, "//span[contains(@class, 'm-keyboard-key')]")))

    (keys[13]).click()
    # the first amount is always for the home team (or the first progression)
    (keys[0]).click()

    double_odds_input[1].click()
    keys = WebDriverWait(driver, 20).until(ec.visibility_of_any_elements_located(
        (By.XPATH, "//span[contains(@class, 'm-keyboard-key')]")))

    (keys[13]).click()
    (keys[0]).click()

    # # stake_confirm= WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="quick-bet-container"]/div/div[2]/div[1]/div[2]/div[2]/div[2]/div/div/div/span')))
    place_bet = WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.XPATH, '//*[@id="bet-btn"]/p[1]')))

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

    # # total_won= WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="iv-live-score-result"]/div[3]/div[2]/span/div/div[2]')))
    # # s = ''.join(x for x in total_won.text if (x.isdigit() or x=='.'))
    # # print(s)

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

# # # for index, key in enumerate(keys):
# #     # indices for keyboard row
# #     # 0 1
# #     # 1 2
# #     # 2 3
# #     # 3 4
# #     # 4 5
# #     # 5 6
# #     # 6
# #     # 7 7
# #     # 8 8
# #     # 9 9
# #     # 10 0
# #     # 11 .
# #     # 12 00
# #     # 13 Clear
