from flask import Flask, render_template, request
#import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('rfc.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    #Fuel_Type_Diesel=0
    if request.method == 'POST':
        nov = int(request.form['nov'])
        atc = float(request.form['claimtotal'])
        aic = int(request.form['claiminjury'])
        apc = int(request.form['claimprop'])
        avc = int(request.form['claimvehi'])
        age = int(request.form['age'])
        pd = int(request.form['policy'])
        pap = float(request.form['policyann'])
        
        DamageType=request.form['DamageType']
        
        if(DamageType == 'MinorDamage'):
            MinorDamage = 1
            TrivialDamage = 0
            TotalLoss = 0
        elif(DamageType == 'TrivalDamage'):
            MinorDamage = 0
            TrivialDamage = 1
            TotalLoss = 0
        else:
            MinorDamage = 0
            TrivialDamage = 0
            TotalLoss = 1
        #'Minor Damage', 'Total Loss', 'Trivial Damage'
        
        prediction=model.predict([[nov,atc,aic,apc,avc,age,pd,pap,MinorDamage,TotalLoss,TrivialDamage]])
        if prediction == 0:
            return render_template('index.html',prediction_texts="No Fraud")
        else:
            return render_template('index.html',prediction_texts="Fraud Transaction.")
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)

