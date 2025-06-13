from flask import Blueprint, jsonify, request, session
from tools.core import LogisticRegressionInference, MinMaxScalerInference
from auth.login import login_user, logout_user, is_logged_in
from database.config import get_db

import numpy as np

user_routes = Blueprint('user', __name__, url_prefix='/user')

logreg = LogisticRegressionInference()
minmax = MinMaxScalerInference()


@user_routes.post("/prediction")
def predict():

    if not is_logged_in():
        return jsonify({
                    "success": False,
                    "message": "Unauthorized"}
                ), 401
    
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
    
    db = get_db()
    changer = {"No":0,
               "Yes":1}
    
    try:

        data['Stage Fear'] = changer[data['Stage Fear']]
        data['Drained After Socializing'] = changer[data['Drained After Socializing']]
        data = {i: data[i] for i in checker}

        prediction = list(data.values())
        prediction = minmax.transform(prediction)
        prediction, percentage = logreg.predict(prediction)

        label_changer = {0: 'Introvert',
                         1: 'Extrovert'}
        
        if prediction == 0:
            percentage = 1 - percentage

        percentage = round(percentage, 4) * 100
        prediction = label_changer[prediction]
        
        with db.cursor() as cursor:

            query = """
                    INSERT INTO user_form
                        (user_id,
                        time_spent_alone,
                        stage_fear,
                        social_event_attendance,
                        going_outside,
                        drained_after_socializing,
                        friends_circle_size,
                        post_frequency,
                        personality,
                        percentage)
                    VALUES
                        (%s, %s, %s, %s, %s,
                         %s, %s, %s, %s, %s)
                    ;
                    """
            data['Stage Fear'] = bool(data['Stage Fear'])
            data['Drained After Socializing'] = bool(data['Drained After Socializing'])

            elements = tuple(
                        [session["user_id"]] + list(data.values()) + [prediction, percentage]
                        )
            
            print(percentage)

            cursor.execute(query,
                           elements)

        db.commit()

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
    
@user_routes.post('/login')
def login():

    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({
                    "success": False,
                    "message": "Missing credentials"}
                ), 400

    if login_user(username, password):
        return jsonify({
                    "success": True,
                    "message": f"Log in success, welcome {username}"}
                ), 200
    
    else:
        return jsonify({
                    "success": False,
                    "message": "Invalid credentials"}
                ), 401

@user_routes.post('/logout')
def logout():

    logout_user()
    return jsonify({
                    "success": True,
                    "message": "You have been logged out"}
                ), 200