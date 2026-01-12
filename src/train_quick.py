import pandas as pd
import numpy as np
import pickle
import xgboost as xgb
from sklearn.metrics import roc_auc_score, accuracy_score
from src.data_processing import load_data, identify_label_column, preprocess_data, get_target, split_data

def train_quick(filepath='brazilian-malware.csv'):
    print("Quick training with XGBoost...")
    # 1. Load
    df = load_data(filepath)
    label_col = identify_label_column(df)
    
    # 2. Preprocess (Fit Mode)
    X, encoders, scaler = preprocess_data(df, label_col=label_col)
    y = get_target(df, label_col)
    
    feature_names = list(X.columns)
    
    # 3. Split
    X_train, X_test, y_train, y_test = split_data(X, y)
    
    # 4. Train XGBoost (Best Performer)
    model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
    model.fit(X_train, y_train)
    
    # 5. Evaluate
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    
    acc = accuracy_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_proba)
    
    print(f"XGBoost - Acc: {acc:.4f}, AUC: {auc:.4f}")
    
    # 6. Save
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("Model saved to model.pkl")
    
    with open('model_metadata.pkl', 'wb') as f:
        pickle.dump({
            'feature_names': feature_names,
            'encoders': encoders,
            'scaler': scaler
        }, f)
    print("Model metadata saved to model_metadata.pkl")

if __name__ == "__main__":
    train_quick()
