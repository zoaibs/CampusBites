from flask import Flask, render_template, request, redirect, url_for
import main
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        # Get data from the form
        height = request.form.get("height")
        sex = request.form.get("sex")
        weight = request.form.get("weight")
        goal_weight = request.form.get("goal_weight")   
        goal_time = request.form.get("goal_time")
        dining_hall = request.form.get("dining_hall")
        meal_type = request.form.get("meal_type")
        bmr_scale = request.form.get("bmr_scale")
        
        # Sample logic for generating meal suggestion based on meal type
        #print(meal_type)
        warning_message = main.check_weight_change_safety(weight, goal_weight, goal_time)

        if warning_message:
            # If the warning is triggered, re-render the form with the warning message
            return render_template("form.html", warning_message=warning_message)
        meal_data , total_calories, total_protein, total_fat, total_carbs, total_fiber, total_vitamins, total_minerals= main.process_user_data(height, weight, goal_weight, goal_time, sex, dining_hall, meal_type, bmr_scale)
        

        meal_info = {
            "meal": meal_data,
            "total_calories": total_calories,
            "total_protein": total_protein,
            "total_fat": total_fat,
            "total_carbs": total_carbs,
            "total_fiber": total_fiber,
            "total_vitamins": total_vitamins,
            "total_minerals": total_minerals
        }

        return render_template("meal_suggestion.html", meal_info=meal_info)


    
        
        
        # Redirect to the meal suggestion page with the user's data
        

    return render_template("form.html")

@app.route("/meal_suggestion")
def meal_suggestion():
    # Get the meal and calories from the URL parameters
    meal = request.args.get("meal")
    calories = request.args.get("calories")
    return redirect(url_for('form'))

if __name__ == "__main__":
    app.run(debug=True)