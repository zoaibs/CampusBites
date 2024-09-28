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
        gender = request.form.get("gender")
        weight = request.form.get("weight")
        goal_weight = request.form.get("goal_weight")
        goal_time = request.form.get("goal_time")
        dining_hall = request.form.get("dining_hall")
        meal_type = request.form.get("meal_type")
        main.main()
        # Sample logic for generating meal suggestion based on meal type
        meal_suggestions = {
            "breakfast": ("Oatmeal with fruits", 300),
            "lunch": ("Grilled chicken salad", 450),
            "dinner": ("Quinoa with steamed veggies", 500)
        }

        # Get the suggested meal and calories for the selected meal type
        suggested_meal, calories = meal_suggestions.get(meal_type, ("Unknown", 0))
        
        # Redirect to the meal suggestion page with the user's data
        return redirect(url_for("meal_suggestion", meal=suggested_meal, calories=calories))
    
    return render_template("form.html")

@app.route("/meal_suggestion")
def meal_suggestion():
    # Get the meal and calories from the URL parameters
    meal = request.args.get("meal")
    calories = request.args.get("calories")
    
    return render_template("meal_suggestion.html", meal=meal, calories=calories)

if __name__ == "__main__":
    app.run(debug=True)
