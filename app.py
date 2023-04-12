import pickle
from flask import Flask,request,app,jsonify,render_template
import numpy as np
import pandas as pd

app = Flask(__name__)

#Load  the model
regModel = pickle.load(open('regModel.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/predict_api',methods=['POST'])
def predict_api():
    data = request.json['data']
    print(data)
    print(np.array(list(data.values())).reshape(1,-1))
    new_data = scaler.transform(np.array(list(data.values())).reshape(1,-1))
    output=regModel.predict(new_data)
    print(output[0])
    return jsonify(output[0])

@app.route('/predict',methods=['POST'])
def predict():
    data = [float(x) for x in request.form.values()]
    print(data)
    new_data = scaler.transform(np.array(data).reshape(1,-1))
    output = regModel.predict(new_data)[0]
    return render_template("home.html",prediction_text="The house cost you is {}".format(output))

if __name__ == '__main__':
    app.run(debug=True)