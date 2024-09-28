from flask import Flask, render_template, request, redirect, url_for
import main2
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
        
        # Sample logic for generating meal suggestion based on meal type

        meal_data = main2.process_user_data(height, weight, goal_weight, goal_time, sex, dining_hall, meal_type)
        
        
        
        # Redirect to the meal suggestion page with the user's data
        return redirect(url_for("meal_suggestion", meal=meal_data, calories=200))

    return render_template("form.html")

@app.route("/meal_suggestion")
def meal_suggestion():
    # Get the meal and calories from the URL parameters
    meal = request.args.get("meal")
    calories = request.args.get("calories")
    
    return render_template("meal_suggestion.html", meal=meal, calories=calories)

if __name__ == "__main__":
    app.run(debug=True)
