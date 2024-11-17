from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError
from joblib import load  # To load scalers
import traceback

# Initialize Flask app
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)  # Enable CORS to allow cross-origin requests

# Define the filepath to the model
model_path = os.path.join(os.path.dirname(__file__), 'ML_Model', 'weather_model.h5')

# If 'mse' is the built-in metric, register it manually
custom_objects = {
    'mse': MeanSquaredError()  # Register built-in MSE
}

# Load the model with custom objects
model = load_model(model_path, custom_objects=custom_objects)

# Load scalers
scaler_X_path = os.path.join(os.path.dirname(__file__), 'ML_Model', 'scaler_X.pkl')
scaler_y_path = os.path.join(os.path.dirname(__file__), 'ML_Model', 'scaler_y.pkl')
scaler_X = load(scaler_X_path)
scaler_y = load(scaler_y_path)

# Flask routes
@app.route('/')
def home():
    """
    Serve the Urban Greening project homepage.
    """
    return render_template('urban_greening.html')

@app.route('/weather_prediction')
def weather_prediction():
    """
    Serve the Weather Prediction page.
    """
    return render_template('weather_prediction.html')
@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Handle weather prediction requests.
    """
    try:
        # Parse input JSON
        data = request.json
        year, month, day = int(data['year']), int(data['month']), int(data['day'])

        # Prepare input for model
        new_date = pd.DataFrame({'Year': [year], 'Month': [month], 'Day': [day]})
        new_date_scaled = scaler_X.transform(new_date)

        # Make prediction
        prediction_scaled = model.predict(new_date_scaled)
        prediction = scaler_y.inverse_transform(prediction_scaled)[0]

        
        # Mapping for user-friendly field names and units
        field_mapping = {
            'PRCP': ('Precipitation', 'mm'),
            'SNOW': ('Snowfall', 'mm'),
            'TMAX': ('Temperature Max', '°F'),
            'TMIN': ('Temperature Min', '°F'),
            'TSUN': ('Total Sunshine', 'minutes'),
        }

        # Prepare response and exclude TOBS
        factors = ['PRCP', 'SNOW', 'TMAX', 'TMIN', 'TSUN']  # Exclude TOBS
        predicted_values = {
            field_mapping[factor][0]: f"{round(float(value), 2)} {field_mapping[factor][1]}"
            for factor, value in zip(factors, prediction)
        }
        
        return jsonify({"success": True, "prediction": predicted_values})

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        })

'''
@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Handle weather prediction requests.
    """
    
    try:
        # Parse input JSON
        data = request.json
        year, month, day = int(data['year']), int(data['month']), int(data['day'])

        # Prepare input for model
        new_date = pd.DataFrame({'Year': [year], 'Month': [month], 'Day': [day]})
        new_date_scaled = scaler_X.transform(new_date)

        # Make prediction
        prediction_scaled = model.predict(new_date_scaled)
        prediction = scaler_y.inverse_transform(prediction_scaled)[0]

        # Prepare response
        factors = ['PRCP', 'SNOW', 'TMAX', 'TMIN', 'TOBS', 'TSUN']
        predicted_values = {factor: round(float(value), 2) for factor, value in zip(factors, prediction)}
        return jsonify({"success": True, "prediction": predicted_values})

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        })
    '''

if __name__ == '__main__':
    app.run(debug=True)
'''from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError
from sklearn.preprocessing import StandardScaler

# Initialize Flask app
app = Flask(__name__)

# Define the filepath to the model
model_path = os.path.join(os.path.dirname(__file__), 'ML_Model', 'weather_model.h5')

# If 'mse' is the built-in metric, register it manually:
custom_objects = {
    'mse': MeanSquaredError()  # Register built-in MSE
}

# Load the model with custom objects
model = load_model(model_path, custom_objects=custom_objects)

# Load scalers
scaler_X = ...  # Load the saved scaler for X
scaler_y = ...  # Load the saved scaler for y

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        # Parse input JSON
        data = request.json
        year, month, day = int(data['year']), int(data['month']), int(data['day'])

        # Prepare input for model
        new_date = pd.DataFrame({'Year': [year], 'Month': [month], 'Day': [day]})
        new_date_scaled = scaler_X.transform(new_date)

        # Make prediction
        prediction_scaled = model.predict(new_date_scaled)
        prediction = scaler_y.inverse_transform(prediction_scaled)[0]

        # Prepare response
        factors = ['PRCP', 'SNOW', 'TMAX', 'TMIN', 'TOBS', 'TSUN']
        predicted_values = {factor: round(float(value), 2) for factor, value in zip(factors, prediction)}
        return jsonify({"success": True, "prediction": predicted_values})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
'''