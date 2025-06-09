import random
import pandas as pd
from flask import Flask, render_template, request
import sympy as sp
import math
from experts.gear_inch import compute_speed as compute_gear_inch
from experts.tire_pressure import compute_pressure
# At the very top of app.py
import os
os.environ.setdefault('FLASK_APP', 'app.py')


# Initialize Flask app
app = Flask(
    __name__,
    static_folder='static',
    template_folder='templates'
)

jokes_df = pd.read_csv('data/bike_jokes.csv')  # adjust path if needed
joke_list = jokes_df['joke'].tolist()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/community')
def community():
    # Pick a random joke from the CSV
    joke = random.choice(joke_list)
    return render_template('community.html', joke=joke)
    
@app.route('/bike-finder')
def bike_finder():
    return render_template('bike_finder.html')


# 1) Overview page for all expert models
@app.route('/experts')
def experts_overview():
    return render_template('experts_overview.html')

# 2) Pure Kinematic model endpoint
@app.route('/experts/pure_kinematic', methods=['GET', 'POST'])
def experts_pure_kinematic():
    explanation = (
        "We use a simple gear-ratio model:\n"
        "  speed = wheel circumference × (cadence / 60) × (chainring ÷ sprocket)\n"
        "Then we convert from meters/second to km/h."
    )
    result = None
    if request.method == 'POST':
        chainring      = int(request.form['chainring_teeth'])
        sprocket       = int(request.form['sprocket_teeth'])
        cadence_rpm    = float(request.form['cadence'])
        wheel_diameter = float(request.form['wheel_diameter'])

        circumference = math.pi * wheel_diameter
        gear_ratio    = chainring / sprocket
        cadence_rps   = cadence_rpm / 60.0
        speed_m_s     = circumference * cadence_rps * gear_ratio
        speed_kmh     = speed_m_s * 3.6

        result = {
            'speed_kmh':     round(speed_kmh, 1),
            'gear_ratio':    round(gear_ratio, 2),
            'circumference': round(circumference, 2),
            'cadence_rps':   round(cadence_rps, 2),
            'cadence_rpm':   cadence_rpm
        }

    return render_template(
        'experts.html',
        explanation=explanation.replace('\n','<br>'),
        result=result
    )
    
@app.route('/experts/gear_inch', methods=['GET','POST'])
def experts_gear_inch():
    explanation = (
        "Classic Gear‐Inch model:\n"
        "1) Gear Inches = (chainring ÷ sprocket) × wheel diameter (inches)\n"
        "2) Convert to meters per pedal rev and then speed (km/h)."
    )
    result = None
    if request.method == 'POST':
        c = int(request.form['chainring_teeth'])
        s = int(request.form['sprocket_teeth'])
        rpm = float(request.form['cadence'])
        d = float(request.form['wheel_diameter'])
        result = compute_gear_inch(c, s, rpm, d)

    return render_template(
        'experts.html',
        explanation=explanation.replace('\n','<br>'),
        result=result
    )


@app.route('/experts/tire_pressure', methods=['GET','POST'])
def experts_tire_pressure():
    explanation = (
        "We estimate the tire’s contact patch from its volume and circumference, then\n"
        "compute optimal pressure = (weight·g)/area and report it in bar."
    )
    result = None
    if request.method == 'POST':
        W  = float(request.form['weight'])
        TW = float(request.form['tire_width'])
        WD = float(request.form['wheel_diameter'])
        result = compute_pressure(W, TW, WD)

    return render_template(
        'experts_tire_pressure.html',
        explanation=explanation.replace('\n','<br>'),
        result=result
    )



if __name__ == '__main__':
    app.run(debug=True)
