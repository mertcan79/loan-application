
import numpy as np
import pandas as pd
from flask import Flask, request, render_template 
from flask_sqlalchemy import SQLAlchemy
import pickle
import os
#import joblib
from ast import Break
import csv
import sys
from pathlib import Path
from qualifier.functions.main import find_qualifying_loans, get_data, get_stats
import qualifier.utils.plotly_layouts as ply
import json
import plotly 

app = Flask(__name__, static_folder='static', template_folder="template")
   
db = SQLAlchemy(app)

#home page
@app.route('/')
def home():
    return render_template('index.html')

#filter the result and return
@app.route('/filter', methods=['POST'])
def filter():

    features=[x for x in request.form.values()]

    #data = pd.DataFrame([np.array(features)], columns = cols)
    gender,married,credit_score, debt, income, loan, home_value=features
    
    df_main = get_data()

    result = find_qualifying_loans(df_main,credit_score, debt, income, loan, home_value)
    
    return render_template('index.html', output='Loans found eligible: {}'.format(result))

@app.route("/stats",  methods=['GET'])
def stats():
    greetings = "This is where you stand"

    feature=request.args.get('feature')
    value = float(request.args.get('value'))
    bank_data = get_data()
    plot = ply.create_plotly(bank_data,feature,value)

    plotly_plot = json.dumps(plot, cls=plotly.utils.PlotlyJSONEncoder)

    where_you_stand = get_stats(bank_data,value,feature)

    return render_template("plot.html", greetings=greetings, plotly_plot= plotly_plot,where_you_stand=where_you_stand)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port,debug=True,use_reloader=False)