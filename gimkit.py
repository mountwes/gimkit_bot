from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep
from random import uniform
from xpaths import *
from gimkit_question import gimkit_question

chromedriver_location = "/usr/bin/chromedriver"
driver = webdriver.Chrome(chromedriver_location)
wait = WebDriverWait(driver, 10)

correct_answers = []
money = 0
streak_level = 1
next_streak_level_money = 20  # determine automatically

def clicker(xpath):
  wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
  driver.find_element_by_xpath(xpath).click()

def typer(xpath, string):
  wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
  driver.find_element_by_xpath(xpath).send_keys(string)

def join_game(code, name):
  gimkit = "https://www.gimkit.com/live"
  #driver.maximize_window()
  driver.get(gimkit)
  typer(game_code_input, code)
  clicker(join_game_button_1)
  sleep(3)  # fix hard coded sleep values, wait until element is interactable
  typer(name_input, name)
  clicker(join_game_button_2)
  print("Joined game.")

def get_question():
  return(driver.find_element_by_xpath(question_text).text)

def get_answers():
  answers = []
  for i in range(4):
    answers.append(driver.find_element_by_xpath(answer_choice % (i+1)).text)
  return(answers)

def get_response():
  response = driver.find_element_by_xpath(response_text).text[0]
  if response == "+":
    return(True)
  elif response == "-":
    clicker(view_correct_answer)
    return(driver.find_element_by_xpath(correct_answer_text).text)

def get_money():
  money_string = driver.find_element_by_xpath(money_text).text
  return(int(money_string.replace("-", "").replace("$", "").replace(",", "")))  # don't remove negative sign

def add_question_answer(question, answer):
  correct_answers.append(gimkit_question(question, answer))

def answer_question():
  question = get_question()
  answers = get_answers()
  for i in range(len(correct_answers)):
    if correct_answers[i].question == question:
      clicker(answer_choice % (answers.index(correct_answers[i].answer)+1))  # add unique id to questions, search all answers to questions that match
      sleep(0.5)  # fix so that program waits until element is interactable
      clicker(correct_continue_button)
      return(0)
  clicker(answer_choice % 1)
  sleep(0.5)  # fix so that program waits until element is interactable
  response = get_response()
  if response == True:
    add_question_answer(question, answers[0])
    clicker(correct_continue_button)
    return(0)
  elif len(response) > 0:
    add_question_answer(question, str(response))
  try:
    clicker(correct_continue_button)
  except:
    clicker(incorrect_continue_button)
  return(1)

def shop():
  global money
  global next_streak_level_money
  global streak_level
  if streak_level < 10:
    if money >= next_streak_level_money:
      clicker(three_lines_button)
      clicker(shop_button)
      clicker(streak_bonus_button)
      if streak_level < 9:
        clicker(streak_level_text % (streak_level+2))
        money_string = driver.find_element_by_xpath(streak_level_money_text).text
        next_streak_level_money = int(money_string[9:].replace("-", "").replace("$", "").replace(",", ""))
      clicker(streak_level_text % (streak_level+1))
      clicker(buy_button)
      clicker(continue_to_questions_button)
      streak_level += 1

def delay():
  sleep_time = uniform(0.5, 1.5)
  print(f"Sleeping for {sleep_time}s")
  sleep(sleep_time)
  print("Resuming")

def play():
  global money
  WebDriverWait(driver, 300).until(EC.element_to_be_clickable((By.XPATH, three_lines_button)))
  print("Game is starting...")
  while True:
    money = get_money()
    print(f"Money: ${money}")
    to_shop = answer_question()
    if to_shop == 0:
      shop()
    delay()
    # handle end of game
    # claps
