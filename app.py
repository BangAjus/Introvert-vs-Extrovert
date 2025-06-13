from flask import Flask, request, jsonify, redirect, flash
from tools.core import LogisticRegressionInference, MinMaxScalerInference
import numpy as np
import os

from public.routes import public_routes
from user.routes import user_routes

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

app.register_blueprint(public_routes)
app.register_blueprint(user_routes)

if __name__ == '__main__':
    app.run(debug=True,
            port=5000)
