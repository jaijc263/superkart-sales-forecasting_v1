import os
import pandas as pd
import joblib
from flask import Flask, request, jsonify

# Initialize Flask App
app = Flask(__name__)

# Define path to model
MODEL_PATH = 'superkart_model.joblib'

# Load the serialized model pipeline
try:
    model = joblib.load(MODEL_PATH)
    print('Model loaded successfully.')
except Exception as e:
    print(f'Error loading the model: {str(e)}')
    model = None

@app.route('/', methods=['GET'])
def home():
    return 'Welcome to the SuperKart Sales Forecasting API!'

@app.route('/v1/predict', methods=['POST'])
def predict():
    # Endpoint for online inference of a single record
    if model is None:
        return jsonify({'error': 'Model is not loaded on server.'}), 500
    
    try:
        # Get JSON payload from request
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No input data provided'}), 400
            
        # Convert to Pandas DataFrame (single row)
        df_input = pd.DataFrame([data])
        
        # Predict total sales
        prediction = model.predict(df_input)[0]
        
        return jsonify({'prediction': float(prediction)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/v1/predictbatch', methods=['POST'])
def predict_batch():
    # Endpoint for batch inference via uploaded CSV file
    if model is None:
        return jsonify({'error': 'Model is not loaded on server.'}), 500
        
    try:
        # Check if file is uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected for uploading'}), 400
            
        # Read uploaded CSV directly into Pandas DataFrame
        df_input = pd.read_csv(file)
        
        # Apply model pipeline for predictions
        predictions = model.predict(df_input)
        
        # Return predictions as dictionary mapping index to predicted value
        result = {str(i): float(pred) for i, pred in enumerate(predictions)}
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Run Flask server
    app.run(host='0.0.0.0', port=7860, debug=True)