import json
import random
from sklearn.ensemble import RandomForestRegressor
import numpy as np

# Load dining hall menu data from a JSON file
def load_menu_data(json_file):
    with open(json_file, 'r') as file:
        menu = json.load(file)
    return menu

# Define the user profile
def get_user_profile():
    weight = float(input("Enter your current weight (in kg): "))
    weight_goal = float(input("Enter your weight goal (in kg): "))
    gender = input("Enter your gender (M/F): ")
    return {'weight': weight, 'weight_goal': weight_goal, 'gender': gender}

# Estimate daily caloric needs using the Mifflin-St Jeor formula
def estimate_daily_calories(user_profile):
    weight = user_profile['weight']
    gender = user_profile['gender']
    
    if gender.upper() == 'M':
        calories = 10 * weight + 6.25 * 170 - 5 * 25 + 5  # Simplified for males, assuming height and age
    else:
        calories = 10 * weight + 6.25 * 160 - 5 * 25 - 161  # Simplified for females, assuming height and age

    # Adjust based on weight goal (e.g., weight loss reduces daily intake)
    weight_goal_diff = user_profile['weight_goal'] - user_profile['weight']
    if weight_goal_diff < 0:
        calories -= 500  # 500 calorie deficit for weight loss
    elif weight_goal_diff > 0:
        calories += 500  # 500 calorie surplus for weight gain

    return calories

# Train a simple random forest model to predict the best meal
def train_model(menu):
    features = []
    labels = []
    
    # Create feature vectors (calories, protein, fat, carbs) and target (total calories)
    for name in menu:
        feature = [name['calories'], name['protein'], name['fat'], name['carbs']]
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

    # Calculate macronutrient calorie targets
    carb_target = daily_calories * carb_ratio / 4  # 4 calories per gram of carbs
    protein_target = daily_calories * protein_ratio / 4  # 4 calories per gram of protein
    fat_target = daily_calories * fat_ratio / 9  # 9 calories per gram of fat

    return carb_target, protein_target, fat_target

# Recommend a meal based on the user's daily caloric needs
# Recommend a meal based on the user's daily caloric needs
def recommend_meal(model, menu, daily_calories):
    meal = []
    total_calories = 0
    total_protein = 0
    total_fat = 0
    total_carbs = 0
    
    # Get target macronutrient values
    carb_target, protein_target, fat_target = get_macronutrient_targets(daily_calories)
    
    # Filter meals that fit the macronutrient constraints
    filtered_menu = [name for name in menu if (name['protein'] <= protein_target and
                                               name['fat'] <= fat_target and
                                               name['carbs'] <= carb_target)]

    # If no meals fit the criteria, return an empty meal plan
    if not filtered_menu:
        print("No meals match the macronutrient targets.")
        return meal, total_calories, total_protein, total_fat, total_carbs
    
    # Keep adding meals until the total calories meet or exceed the daily requirement
    while total_calories < daily_calories:
        name = random.choice(filtered_menu)
        prediction = model.predict([[name['calories'], name['protein'], name['fat'], name['carbs']]])[0]
        
        meal.append(name)
        total_calories += prediction
        total_protein += name['protein']
        total_fat += name['fat']
        total_carbs += name['carbs']

    return meal, total_calories, total_protein, total_fat, total_carbs


# Display the recommended meal plan
def display_meal(meal, total_calories, total_protein, total_fat, total_carbs):
    print("\nRecommended Meal Plan:")
    for name in meal:
        print(f"{name['name']} - {name['calories']} calories")

    print(f"\nTotal Calories: {total_calories} kcal")
    print(f"Total Protein: {total_protein} g")
    print(f"Total Fats: {total_fat} g")
    print(f"Total Carbs: {total_carbs} g")


# Main execution
if __name__ == "__main__":
    menu = load_menu_data('menu.json')  # Load the menu data
    user_profile = get_user_profile()  # Get user profile
    daily_calories = estimate_daily_calories(user_profile)  # Estimate daily calorie intake
    print(f"Estimated Daily Calories: {daily_calories} kcal")

    # Train a machine learning model using the menu data
    model = train_model(menu)

    # Recommend a meal based on daily caloric needs
    meal, total_calories, total_protein, total_fat, total_carbs = recommend_meal(model, menu, daily_calories)

    # Display the recommended meal plan
    display_meal(meal, total_calories, total_protein, total_fat, total_carbs)



# Main execution
if __name__ == "__main__":
    menu = load_menu_data('menu.json')  # Load the menu data
    user_profile = get_user_profile()  # Get user profile
    daily_calories = estimate_daily_calories(user_profile)  # Estimate daily calorie intake
    print(f"Estimated Daily Calories: {daily_calories} kcal")

    # Train a machine learning model using the menu data
    model = train_model(menu)

    # Recommend a meal based on daily caloric needs
    meal, total_calories, total_protein, total_fat, total_carbs = recommend_meal(model, menu, daily_calories)

    # Display the recommended meal plan
    display_meal(meal, total_calories, total_protein, total_fat, total_carbs)
