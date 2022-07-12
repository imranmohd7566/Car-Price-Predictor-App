# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 21:37:34 2022

@author: home
"""

from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
model = pickle.load(open('rf_reg_model.pkl', 'rb'))

@app.route('/',methods=['GET'])
def Home():
    return render_template('index1.html')

standard_to = StandardScaler()

@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Other=0
    Owner_Type_Other=0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        #Present_Price=float(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])
        #Kms_Driven2=np.log(Kms_Driven)
        Owner_Type_Second=request.form['Owner_Type_Second']
        if(Owner_Type_Second=='Second'):
                Owner_Type_Second=1
        elif (Owner_Type_Second=='More Than 2'):
            Owner_Type_Second=2
        else:
            Owner_Type_Second=0
        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol=='Petrol'):
                Fuel_Type_Petrol=0
        elif (Fuel_Type_Petrol=='Diesel'):
            Fuel_Type_Petrol=1
        else:
            Fuel_Type_Petrol=2
        Year=2020-Year
        Seller_Type=request.form['Seller_Type']
        if(Seller_Type=='Individual'):
            Seller_Type=1
        else:
            Seller_Type=0	
        Transmission=request.form['Transmission_Manual']
        if(Transmission=='Manual'):
            Transmission=1
        else:
            Transmission=0
        prediction=model.predict([[Kms_Driven,Fuel_Type_Petrol, Seller_Type, Transmission, Owner_Type_Second, Year]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car between {0} and {1}".format(round(output-85000), round(output+85000)))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)