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

def add_question_answer(question, answer):
  correct_answers.append(gimkit_question(question, answer))

def get_response():
  response = driver.find_element_by_xpath(response_text).text[0]
  if response == "+":
    return(True)
  elif response == "-":
    clicker(view_correct_answer)
    return(driver.find_element_by_xpath(correct_answer_text).text)

def answer_question():
  question = get_question()
  answers = get_answers()
  for i in range(len(correct_answers)):
    if correct_answers[i].question == question:
      clicker(answer_choice % (answers.index(correct_answers[i].answer)+1))
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
  clicker(correct_continue_button)

def delay():
  sleep_time = uniform(0.5, 1.5)
  print(f"Sleeping for {sleep_time}s")
  sleep(sleep_time)
  print("Resuming")

def play():
  WebDriverWait(driver, 300).until(EC.element_to_be_clickable((By.XPATH, three_lines_button)))
  print("Game is starting...")
  while True:
    answer_question()
    delay()
      
