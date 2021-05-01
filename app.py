from flask import Flask, request, render_template
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route("/", methods=['GET'])
def Home():
    return render_template('home.html')

@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        
        date = request.form['Date']
        day = int(pd.to_datetime(date, format = "%Y-%m-%dT%H:%M").day)
        month = int(pd.to_datetime(date, format = "%Y-%m-%dT%H:%M").month)
        year = int(pd.to_datetime(date, format = "%Y-%m-%dT%H:%M").year)
        
        Neighbourhood = request.form['City']
        if(Neighbourhood == 'Manhattan'):
            Manhattan = 1
            Brooklyn = 0
            Queens = 0
            Staten_Island = 0
        elif(Neighbourhood == 'Brooklyn'):
            Manhattan = 0
            Brooklyn = 1
            Queens = 0
            Staten_Island = 0
        elif(Neighbourhood == 'Queens'):
            Manhattan = 0
            Brooklyn = 0
            Queens = 1
            Staten_Island = 0   
        elif(Neighbourhood == 'Bronx'):
            Manhattan = 0
            Brooklyn = 0
            Queens = 0
            Staten_Island = 0
        else:
            Manhattan = 0
            Brooklyn = 0
            Queens = 0
            Staten_Island = 1
            
        Room = request.form['Room_Type']
        if(Room == 'Entire_room'):
            Private_room = 0
            Shared_room = 0
        elif(Room == 'Private_room'):
            Private_room = 1
            Shared_room = 0
        else:
            Private_room = 0
            Shared_room = 1
            
        Nights = int(request.form['nights'])
        Availibility = int(request.form['availibility'])
        Nr_reviews = request.form['nr_review']
        Reviews_month = request.form['review_month']
        
        prediction=model.predict([[Nights, Nr_reviews, Reviews_month, Availibility, year, month, day, Brooklyn, Manhattan, Queens, Staten_Island, Private_room, Shared_room]])
        output = np.round(prediction[0],2)
        if(output < 0):
            return render_template('home.html', prediction_text = "No price available")
        else:
            return render_template('home.html', prediction_text = "Estimated Price is ${}".format(output))
            
      
        
    else:
        return render_template('home.html')
            
            
if __name__ == "__main__":
    app.run(debug=True)            
            