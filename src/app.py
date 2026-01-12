import os
import pickle
import pandas as pd
import numpy as np
from flask import Flask, request, render_template, jsonify
# Assumes running with python -m src.app from root
from src.data_processing import preprocess_data, identify_label_column

app = Flask(__name__)
# Get the project root directory (one level up from this file)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'model.pkl')
META_PATH = os.path.join(BASE_DIR, 'model_metadata.pkl')
model = None
encoders = None
scaler = None
feature_names = None

def load_resources():
    global model, encoders, scaler, feature_names
    
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        print("Model loaded.")
    else:
        print("Model not found.")
        
    if os.path.exists(META_PATH):
        with open(META_PATH, 'rb') as f:
            meta = pickle.load(f)
            encoders = meta.get('encoders')
            scaler = meta.get('scaler')
            feature_names = meta.get('feature_names')
        print("Metadata loaded.")
    else:
        print("Metadata not found.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health', methods=['GET'])
def health():
    if model:
        return jsonify({'status': 'healthy', 'model_loaded': True}), 200
    return jsonify({'status': 'unhealthy', 'model_loaded': False}), 503

@app.route('/predict', methods=['POST'])
def predict():
    if not model or feature_names is None:
        return jsonify({'error': 'Model or metadata not loaded'}), 503

    try:
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            # Load CSV
            df = pd.read_csv(file, low_memory=False)
            
            label_col = None
            if 'Label' in df.columns:
                label_col = 'Label'
                
            # Preprocess using saved encoders and scaler
            X, _, _ = preprocess_data(df, label_col=label_col, encoders=encoders, scaler=scaler)
            
        else:
            # Manual Input
            features_str = request.form.get('features')
            if not features_str:
                return jsonify({'error': 'No features provided'}), 400
                
            # Split and treat as strings initially
            # Supporting comma-separated values with optional leading/trailing spaces
            data = [x.strip() for x in features_str.split(',') if x.strip()]
            
            if len(data) != len(feature_names):
                 return jsonify({'error': f'Expected {len(feature_names)} features, got {len(data)}'}), 400

            # Create DataFrame
            df_manual = pd.DataFrame([data], columns=feature_names)
            
            for col in df_manual.columns:
                try:
                    df_manual[col] = pd.to_numeric(df_manual[col])
                except ValueError:
                    pass # Keep as string
            
            # Preprocess
            X, _, _ = preprocess_data(df_manual, label_col=None, encoders=encoders, scaler=scaler)
        
        # Ensure Validation
        missing_cols = set(feature_names) - set(X.columns)
        if missing_cols:
             return jsonify({'error': f'Missing features: {missing_cols}'}), 400
             
        X = X[feature_names] # Enforce order
        
        preds = model.predict(X)
        try:
            probs = model.predict_proba(X)[:, 1]
        except:
            probs = [0.0] * len(preds)
            
        results = []
        for i, (pred, prob) in enumerate(zip(preds, probs)):
            results.append({
                'row': i,
                'prediction': int(pred),
                'probability': float(prob),
                'malware': bool(pred == 1)
            })
            
        if 'file' not in request.files:
            return jsonify(results[0])
        else:
            return jsonify({'results': results})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    load_resources()
    app.run(host='0.0.0.0', port=5000)
