from flask import Blueprint, jsonify, request
from tools.core import LogisticRegressionInference, MinMaxScalerInference
import numpy as np

public_routes = Blueprint('public', __name__, url_prefix='/')

logreg = LogisticRegressionInference()
minmax = MinMaxScalerInference()


@public_routes.get("/prediction")
def predict():

    data = request.get_json()

    if not data:
        return jsonify({
                    "success": False,
                    "message": "Empty JSON"}
                ), 400
    
    checker = ["Time Spent Alone", "Stage Fear", "Social Event Attendance", "Going Outside",
               "Drained After Socializing", "Friend Circle Size", "Post Frequency"]
    
    if sorted(checker) != sorted(data.keys()):
        return jsonify({
                    "success": False,
                    "message": "Missing some or all data needed in JSON"}
                ), 400
    
    changer = {"No":0,
               "Yes":1}
    
    try:
        data['Stage Fear'] = changer[data['Stage Fear']]
        data['Drained After Socializing'] = changer[data['Drained After Socializing']]

        prediction = list(data.values())
        prediction = minmax.transform(prediction)
        prediction, percentage = logreg.predict(prediction)

        label_changer = {0: 'Introvert',
                         1: 'Extrovert'}
        
        if prediction == 0:
            percentage = 1 - percentage

        percentage = round(percentage, 4) * 100
        prediction = label_changer[prediction]

        return jsonify({
                    "success": True,
                    "message": f"Sucessfully predicted the data, you are {percentage}% {prediction}",
                    "result": {
                                "percentage": percentage,
                                "personality": prediction
                            }
                    }
                ), 200

    except Exception as e:
        return jsonify({
                    "success": False,
                    "message": f"{e}"}
                ), 500