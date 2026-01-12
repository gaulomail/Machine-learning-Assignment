import pytest
import pandas as pd
import numpy as np
from src.data_processing import preprocess_data, split_data, identify_label_column

def test_identify_label_column_success():
    df = pd.DataFrame({
        'A': [1, 2, 3],
        'Label': [0, 1, 0]
    })
    label_col = identify_label_column(df)
    assert label_col == 'Label'

def test_preprocess_data():
    df = pd.DataFrame({
        'A': [1, 2, 3], # Numeric
        'B': ['a', 'b', 'c'], # Categorical
        'Label': [0, 1, 0]
    })
    
    # Fit mode
    X, encoders, scaler = preprocess_data(df, label_col='Label')
    
    assert X.shape == (3, 2) # A and B (encoded)
    assert 'Label' not in X.columns
    assert 'B' in encoders
    assert scaler is not None

def test_split_data():
    X = pd.DataFrame({'a': range(10)})
    y = pd.Series([0, 1] * 5)
    
    X_train, X_test, y_train, y_test = split_data(X, y)
    
    assert len(X_train) == 8
    assert len(X_test) == 2
    assert len(y_train) == 8
    assert len(y_test) == 2
