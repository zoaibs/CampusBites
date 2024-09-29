import json
import random
from sklearn.ensemble import RandomForestRegressor
import numpy as np
from LLMnutritiongen import *
import argparse
import sys

# Load dining hall menu data from a JSON file
def load_menu_data(json_file, dining_hall, meal_type):
    print("Attempting to load menu data...")
    menu = getMeal(dining_hall, meal_type)
    print(menu)
    if menu is None:
        print("Failed to load menu data. Please check the LLMnutritiongen module and the AI model's response.")
        return []  # Return an empty list instead of None
    print(f"Successfully loaded menu with {len(menu)} items.")
    return menu

# Define the user profile
def get_user_profile(weight, weight_goal, gender, height):
    return {'weight': weight, 'weight_goal': weight_goal, 'gender': gender, 'height': height}

# Estimate daily caloric needs using the Mifflin-St Jeor formula
# Estimate daily caloric needs using the Mifflin-St Jeor formula
def check_weight_change_safety(weight, goal_weight, goal_time_weeks):
    weight_goal_diff = int(goal_weight) - int(weight)
    weight_change_per_week = weight_goal_diff / float(goal_time_weeks)

    # Check for safe weight change limits
    if weight_change_per_week > 1:
        return "Warning: Gaining more than 1 kg per week is not advised. Please choose a safer goal."
    elif weight_change_per_week < -1:
        return "Warning: Losing more than 1 kg per week is not advised. Please choose a safer goal."

    return None  # No warning needed
def estimate_daily_calories(user_profile, goal_time_weeks, bmr_scale):
    weight = user_profile['weight']
    gender = user_profile['gender']
    height = user_profile['height']

    print(type(height))

    # Calculate weight difference
    weight_goal_diff = int(user_profile['weight_goal']) - int(weight)

    # Calculate weight change per week
    weight_change_per_week = weight_goal_diff / float(goal_time_weeks)

    # Check for safe weight change limits
    # if weight_change_per_week > 1:
    #     print("Warning: Gaining more than 1 kg per week is not advised. Are you sure you want to proceed?")
    # elif weight_change_per_week < -1:
    #     print("Warning: Losing more than 1 kg per week is not advised. Are you sure you want to proceed?")

    # Base calorie calculation using Mifflin-St Jeor formula
    if gender.upper() == 'MALE':
        bmr = 10 * weight + 6.25 * height - 5 * 25 + 5  # Replace 25 with actual age if needed
    else:
        bmr = 10 * weight + 6.25 * height - 5 * 25 - 161  # Replace 25 with actual age if needed

    # Daily caloric change based on weight goal
    daily_caloric_change = (weight_change_per_week * 7700) / 7  # Daily caloric change
    print(daily_caloric_change)
    # Calculate daily caloric needs based on weight change goal
    bmr = bmr*bmr_scale
    daily_calories = bmr + daily_caloric_change  # Subtract caloric deficit

    print(f"Estimated Daily Calories: {daily_calories:.2f} kcal")
    return daily_calories


# Train a simple random forest model to predict the best meal
def train_model(menu):
    features = []
    labels = []
    
    # Create feature vectors (calories, protein, fat, carbs) and target (total calories)
    for name in menu:
        feature = [name['calories'], name['protein'], name['fat'], name['carbs'], name['fibers'], name['vitamins'], name['minerals']]
        features.append(feature)
        labels.append(name['calories'])  # We'll use total calories as a label for simplicity

    # Convert lists to numpy arrays
    X = np.array(features)
    y = np.array(labels)

    # Train a random forest regressor
    model = RandomForestRegressor(n_estimators=100)
    model.fit(X, y)
    return model

def get_macronutrient_targets(daily_calories):
    # Define percentage goals for macronutrients
    carb_ratio = 0.40  # 40% of calories from carbs
    protein_ratio = 0.30  # 30% of calories from protein
    fat_ratio = 0.30  # 30% of calories from fat
    fiber_target = 30  # Recommended daily intake of fiber in grams
    vitamin_target = 10  # Recommended overall intake of vitamins (arbitrary unit)
    mineral_target = 10  # Recommended overall intake of minerals (arbitrary unit)

    # Calculate macronutrient calorie targets
    carb_target = daily_calories * carb_ratio / 4  # 4 calories per gram of carbs
    protein_target = daily_calories * protein_ratio / 4  # 4 calories per gram of protein
    fat_target = daily_calories * fat_ratio / 9  # 9 calories per gram of fat

    return carb_target, protein_target, fat_target, fiber_target, vitamin_target, mineral_target

# Recommend a meal based on the user's daily caloric needs
# Recommend a meal based on the user's daily caloric needs
# Recommend a meal based on the user's daily caloric needs
# Recommend a meal based on the user's daily caloric needs and macronutrient balance
def recommend_meal(model, menu, daily_calories):
    meal = []
    total_calories = 0
    total_protein = 0
    total_fat = 0
    total_carbs = 0
    total_fiber = 0
    total_vitamins = 0  # Total vitamins
    total_minerals = 0  # Total minerals

    # Get target macronutrient values
    carb_target, protein_target, fat_target, fiber_target, vitamin_target, mineral_target = get_macronutrient_targets(daily_calories)

    # Allowable deviation from macronutrient target (e.g., 10% tolerance)
    deviation = 0.10

    # Function to calculate macro balance score based on deviation from target macros
    def macro_balance_score(item):
        carb_score = abs((item['carbs'] / (item['calories'] * 4)) - carb_target / daily_calories)
        protein_score = abs((item['protein'] / (item['calories'] * 4)) - protein_target / daily_calories)
        fat_score = abs((item['fat'] / (item['calories'] * 9)) - fat_target / daily_calories)
        return carb_score + protein_score + fat_score

    # Sort menu based on how close they match the macronutrient targets
    sorted_menu = sorted(menu, key=macro_balance_score)

    # Keep adding meals until total calories meet or exceed the daily requirement
    for name in sorted_menu:
        if total_calories >= daily_calories:
            break

        prediction = model.predict([[name['calories'], name['protein'], name['fat'], name['carbs'], name['fibers'], name['vitamins'], name['minerals']]])[0]

        # Only add the meal if the macronutrients are reasonably close to the target
        protein_ratio = (total_protein + name['protein']) / (total_calories + name['calories'])
        fat_ratio = (total_fat + name['fat']) / (total_calories + name['calories'])
        carb_ratio = (total_carbs + name['carbs']) / (total_calories + name['calories'])

        if (abs(protein_ratio - protein_target / daily_calories) <= deviation and
            abs(fat_ratio - fat_target / daily_calories) <= deviation and
            abs(carb_ratio - carb_target / daily_calories) <= deviation):
            
            # Add the meal if within the tolerance
            if name not in meal:
                meal.append(name)
            else:
                print("SKIBIDISKIBIDIDOO - DUPLICATE FOUND")
                idx = meal.index(name)
                if 'two servings' in meal[idx]['name']:
                    meal[idx]['name'] = meal[idx]['name'].replace('two servings', 'three servings')
                elif 'servings' in meal[idx]['name']:
                    # If it already has multiple servings, increase the count
                    count = int(meal[idx]['name'].split()[0])
                    meal[idx]['name'] = meal[idx]['name'].replace(f'{count} servings', f'{count + 1} servings')
                else:
                    # First duplication, rename to "two servings"
                    meal[idx]['name'] = f"two servings of {meal[idx]['name']}"

    # Add the macronutrients and calories to the existing item
                meal[idx]['calories'] += name['calories']
                meal[idx]['protein'] += name['protein']
                meal[idx]['fat'] += name['fat']
                meal[idx]['carbs'] += name['carbs']
                meal[idx]['fibers'] += name['fibers']
                meal[idx]['vitamins'] += name['vitamins']
                meal[idx]['minerals'] += name['minerals']
            total_calories += prediction
            total_protein += name['protein']
            total_fat += name['fat']
            total_carbs += name['carbs']
            total_fiber += name['fibers']
            total_vitamins += name['vitamins']
            total_minerals += name['minerals']

    # In case no meals meet the target, relax the constraint and choose from the best matches
    if not meal:
        print("No meals perfectly match the macronutrient targets. Relaxing constraints.")
        meal = sorted_menu[:3]  # Take top 3 best-matched meals as fallback
        for name in meal:
            
            total_calories += name['calories']
            total_protein += name['protein']
            total_fat += name['fat']
            total_carbs += name['carbs']
            total_fiber += name['fibers']
            total_vitamins += name['vitamins']
            total_minerals += name['minerals']

    return meal, total_calories, total_protein, total_fat, total_carbs, total_fiber, total_vitamins, total_minerals



# Display the recommended meal plan
def display_meal(meal, total_calories, total_protein, total_fat, total_carbs, total_fiber, total_vitamins, total_minerals):
    print("\nRecommended Meal Plan:")
    for name in meal:
        print(f"{name['name']} - {name['calories']} calories")

    print(f"\nTotal Calories: {total_calories} kcal")
    print(f"Total Protein: {total_protein} g")
    print(f"Total Fats: {total_fat} g")
    print(f"Total Carbs: {total_carbs} g")
    print(f"Total Fiber: {total_fiber} g")
    print(f"Total Vitamins: {total_vitamins} (arbitrary units)")
    print(f"Total Minerals: {total_minerals} (arbitrary units)")

def process_user_data(height, weight, goal_weight, goal_time, gender, dining_hall, meal_type, bmr_scale):
    # Load menu data
    bmr_scale = float(bmr_scale)
    height = int(height)
    weight = int(weight)
    goal_weight = int(goal_weight)
    goal_time= int(goal_time)
    menu = load_menu_data('menu.json', dining_hall, meal_type)
    if not menu:
        print("No menu items were loaded. Exiting.")
        return

    # Create a user profile
    user_profile = get_user_profile(weight, goal_weight, gender, height)

    # Convert goal_time from months to weeks
    goal_time_weeks = goal_time * 4  # Assuming 4 weeks in a month

    # Estimate daily caloric needs
    meal_calories = estimate_daily_calories(user_profile, goal_time_weeks, bmr_scale) / 3  # Dividing by 3 for meal planning
    print(f"Estimated Daily Calories: {meal_calories} kcal")

    # Train the model using the loaded menu
    model = train_model(menu)
    if model is None:
        print("Could not train the model. Exiting.")
        return [], 0, 0, 0, 0, 0, 0, 0

    # Recommend a meal based on daily caloric needs
    meal, total_calories, total_protein, total_fat, total_carbs, total_fiber, total_vitamins, total_minerals = recommend_meal(model, menu, meal_calories)

    # Display the recommended meal plan
    display_meal(meal, total_calories, total_protein, total_fat, total_carbs, total_fiber, total_vitamins, total_minerals)
    return meal, total_calories, total_protein, total_fat, total_carbs, total_fiber, total_vitamins, total_minerals

if __name__ == "__main__":
    process_user_data(170, 60, 70, 3, "male", "North Ave Dining Hall", "Dinner", 1.2)
