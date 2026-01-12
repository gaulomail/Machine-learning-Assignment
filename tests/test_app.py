import pytest
import pickle
import numpy as np
import os
from src.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    # Ensure env vars or mocks
    with app.test_client() as client:
        yield client

def test_health_check_no_model(client):
    rv = client.get('/health')
    assert rv.status_code in [200, 503]

def test_predict_no_model(client):
    rv = client.post('/predict', data={'features': '1,2,3'})
    # Should fail because model not loaded
    assert rv.status_code == 503

def test_predict_manual_flow():
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    
    model = LogisticRegression()
    X = np.array([[0,0], [1,1]])
    y = np.array([0, 1])
    model.fit(X, y)
    
    scaler = StandardScaler()
    scaler.fit(X)
    
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
        
    with open('model_metadata.pkl', 'wb') as f:
         pickle.dump({
             'feature_names': ['f1', 'f2'], 
             'encoders': {}, 
             'scaler': scaler
         }, f)
        
    import src.app
    src.app.load_resources()
    
    with src.app.app.test_client() as client:
        # Match feature length (2)
        rv = client.post('/predict', data={'features': '0, 0'})
        assert rv.status_code == 200
        json_data = rv.get_json()
        assert 'prediction' in json_data
        assert 'probability' in json_data
        
    # Cleanup
    if os.path.exists('model.pkl'): os.remove('model.pkl')
    if os.path.exists('model_metadata.pkl'): os.remove('model_metadata.pkl')
