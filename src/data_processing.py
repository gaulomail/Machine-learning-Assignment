import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import os

def load_data(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    df = pd.read_csv(filepath, low_memory=False)
    print(f"Dataset shape: {df.shape}")
    return df

def identify_label_column(df):
    if 'Label' in df.columns:
        return 'Label'
    raise ValueError("Could not find 'Label' column.")

def preprocess_data(df, label_col=None, encoders=None, scaler=None):
    """
    Preprocess data.
    Returns: X, encoders, scaler
    """
    # 1. Drop Label if present
    if label_col and label_col in df.columns:
        X = df.drop(columns=[label_col])
    else:
        X = df.copy()
        
    # 2. Drop useless columns
    cols_to_drop = ['TimeDateStamp', 'FirstSeenDate', 'ImportedDlls', 'ImportedSymbols', 'SHA1']
    X = X.drop(columns=[c for c in cols_to_drop if c in X.columns], errors='ignore')
    
    # 3. Handle Encodings & Scaling
    if encoders is None:
        encoders = {}
        fit_mode = True
    else:
        fit_mode = False
    
    if scaler is None and fit_mode:
        scaler = StandardScaler()
    
    # Separation
    numeric_cols = X.select_dtypes(include=[np.number]).columns
    non_numeric_cols = X.select_dtypes(exclude=[np.number]).columns
    
    # Fill NA in numeric
    X[numeric_cols] = X[numeric_cols].fillna(0)
    
    # Scale Numeric
    if fit_mode:
        X[numeric_cols] = scaler.fit_transform(X[numeric_cols])
    else:
        if scaler:
            X[numeric_cols] = scaler.transform(X[numeric_cols])
            
    # Encode Non-Numeric
    for col in non_numeric_cols:
        if fit_mode:
            le = LabelEncoder()
            X[col] = X[col].astype(str)
            X[col] = le.fit_transform(X[col])
            encoders[col] = le
        else:
            if col in encoders:
                le = encoders[col]
                X[col] = X[col].astype(str)
                # Handle unseen
                classes = set(le.classes_)
                X[col] = X[col].apply(lambda x: le.transform([x])[0] if x in classes else 0) 
            else:
                pass
                
    return X, encoders, scaler

def get_target(df, label_col):
    return df[label_col]

def split_data(X, y):
    return train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
