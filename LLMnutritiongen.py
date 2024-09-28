import google.generativeai as genai
import os
from scrapemenu import *

genai.configure(api_key="AIzaSyAjwSb3D1loKnHrlb6NxzjcnC1nSHjOCCk")

model = genai.GenerativeModel("gemini-1.5-flash")

def getMeal(dining_hall, meal):
    # Scrape menu items
    menu_items = scrapeMenu(dining_hall, meal)
    #print("Scraped menu items:", menu_items)

    if not menu_items:
        print("No menu items were scraped. Check the scrapeMenu function.")
        return None

    # Prepare the prompt for the model
    custom_prompt = (
    "I have an incomplete python list of food menu items. "
    "I want you to fill in the missing nutritional information in grams and "
    "provide the complete list of dictionaries in JSON format. "
    "Ensure all numerical quantities are integers. "
    "Do not include any markdown formatting or code block indicators in your response. "
    "Your response should be a valid JSON array of objects, starting with '[' and ending with ']'. "
    "Here is the list: "
    )
    custom_prompt += str(menu_items)
    #print("Custom prompt:", custom_prompt)

    # Generate response from the model
    try:
        response = model.generate_content(custom_prompt)
        #print("Model response:", response.text)

        if not response.text:
            #print("The model returned an empty response.")
            return None

        # Attempt to parse the response as JSON
        completed_menu = json.loads(response.text)
        return completed_menu
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        print(f"Raw response: {response.text}")
        return None
    except Exception as e:
        print(f"An error occurred while generating or processing content: {e}")
        return None
