import numpy as np
from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

app.config['MONGO_URI'] = 'mongodb+srv://test:test@cluster0.wduwzu0.mongodb.net/mydb?retryWrites=true&w=majority'

mongo = PyMongo(app)
Collection_1 = mongo.db.Collection_1

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    '''
    for rendering results on HTML
    '''
    features = [int(x) for x in request.form.values()]

    # re-arranging the list as per data set
    feature_list = [features[4]] + features[:4] + features[5:11][::-1] + features[11:17][::-1] + features[17:][::-1]
    features_arr = [np.array(feature_list)]

    prediction = model.predict(features_arr)

    print(features_arr)
    #newdb.insert_one(d)
    print("features is :",features)
    default_payment=prediction.tolist()
    New_database={'Gender':features[0],
                 'Education':features[1],
                 'Marrital Status':features[2],
                 'Age':features[3],
                 'Limit Balance':features[4],
                 'PAY_1':features[5],
                 'PAY_2':features [6],
                 'PAY_3':features [7],
                 'PAY_4':features [8],
                 'PAY_5':features [9],
                 'PAY_6':features [10],
                 'BILL_AMT1':features [11],
                 'BILL_AMT2':features [12],
                 'BILL_AMT3':features [13],
                 'BILL_AMT4':features [14],
                 'BILL_AMT5':features [15],
                 'BILL_AMT6':features [16],
                 'PAY_AMT1':features[17],
                 'PAY_AMT2':features[18],
                 'PAY_AMT3':features [19],
                 'PAY_AMT4':features[20],
                 'PAY_AMT5':features[21],
                 'PAY_AMT6':features[22],
                 'Prediction':default_payment[0]}
    Collection_1.insert_one(New_database)
   
    print("prediction value: ", prediction)

    result = ""
    if prediction == 1:
        result = "The credit card holder will be Defaulter in the next month"
    else:
        result = "The Credit card holder will not be Defaulter in the next month"

    return render_template('index.html', prediction_text = result)


if __name__ == '__main__':
    app.run(debug=True)
