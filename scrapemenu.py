from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
from datetime import datetime
import json
print("ss")
options = Options()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
options.add_argument("--window-size=600,1080")  # Set a default window size

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=options)

def scrapeMenu(dining_hall, meal):
    menu = []  # LIST TO STORE ALL MENU ITEMS

    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")

    driver.get(f"https://techdining.nutrislice.com/menus-eula")

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'primary'))
    )

    go_to_meal_options_buttons = driver.find_elements(By.CLASS_NAME, "primary")
    go_to_meal_options_button = go_to_meal_options_buttons[0]
    go_to_meal_options_button.click()

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'name'))
    )

    dining_hall_options = driver.find_elements(By.CLASS_NAME, "name")

    for dining_hall_option in dining_hall_options:
        if (dining_hall_option.get_attribute("innerHTML").strip() == dining_hall.strip()):
            dining_hall_option.click()
            break

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'menu-item'))
    )

    meal_options = driver.find_elements(By.CLASS_NAME, "name")

    default_meal_options = ["Breakfast", "Lunch", "Dinner"]

    for meal_option in meal_options:
        if meal_option.get_attribute("innerHTML") in default_meal_options:
            if (meal_option.get_attribute("innerHTML") == meal):
                meal_option.click()
                break

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'ns-icon-down-chevron'))
    )

    collapse_buttons = driver.find_elements(By.CLASS_NAME, "ns-icon-down-chevron")

    for collapse_button in collapse_buttons:
        collapse_button.click()

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'food-name'))
    )

    food_items = driver.find_elements(By.CLASS_NAME, "food-name")

    for food_item in food_items:
        name_of_food = food_item.get_attribute("innerHTML").split("<!----> ")[1]
        menu_item = {
            "name": name_of_food.strip(),
            "calories": 0,
            "protein": 0,
            "fat": 0,
            "carbs": 0,
            "fibers": 0,
            "vitamins": 0,
            "minerals": 0
        }
        menu.append(menu_item)

    return menu