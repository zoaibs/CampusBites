import google.generativeai as genai
import os
from scrapemenu import *

genai.configure(api_key="AIzaSyAjwSb3D1loKnHrlb6NxzjcnC1nSHjOCCk")

model = genai.GenerativeModel("gemini-1.5-flash")

def getMeal(dining_hall, meal):
    menu_items = scrapeMenu(dining_hall, meal)
    #print(menu_items)
    custom_prompt = f"I have an incomplete python dict of food menu items. I want you to fill in the missing information in grams. All nutritional details are currently set to zero. Make them correct and send me back JUST the complete dict. Here is the dict: {menu_items}"

    response = model.generate_content(custom_prompt)

    return response.text