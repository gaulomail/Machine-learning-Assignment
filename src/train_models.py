import pandas as pd
import numpy as np
import pickle
import time
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import roc_auc_score, accuracy_score
import xgboost as xgb
import lightgbm as lgb
# from catboost import CatBoostClassifier # Removed due to compatibility issues
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.base import BaseEstimator, ClassifierMixin

# Import data processing
from src.data_processing import load_data, identify_label_column, preprocess_data, get_target, split_data

class PyTorchMLP(BaseEstimator, ClassifierMixin):
    def __init__(self, input_dim=None, hidden_dim=64, epochs=5, batch_size=32, lr=0.001):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.epochs = epochs
        self.batch_size = batch_size
        self.lr = lr
        self.model = None
        self.device = torch.device('cpu') 

    def fit(self, X, y):
        if isinstance(X, pd.DataFrame):
            X = X.values
        if isinstance(y, pd.Series):
            y = y.values
            
        self.input_dim = X.shape[1]
        
        self.model = nn.Sequential(
            nn.Linear(self.input_dim, self.hidden_dim),
            nn.ReLU(),
            nn.Linear(self.hidden_dim, self.hidden_dim),
            nn.ReLU(),
            nn.Linear(self.hidden_dim, 1),
            nn.Sigmoid()
        ).to(self.device)
        
        criterion = nn.BCELoss()
        optimizer = optim.Adam(self.model.parameters(), lr=self.lr)
        
        X_tensor = torch.tensor(X, dtype=torch.float32).to(self.device)
        y_tensor = torch.tensor(y, dtype=torch.float32).view(-1, 1).to(self.device)
        
        dataset = torch.utils.data.TensorDataset(X_tensor, y_tensor)
        dataloader = torch.utils.data.DataLoader(dataset, batch_size=self.batch_size, shuffle=True)
        
        self.model.train()
        for epoch in range(self.epochs):
            for batch_X, batch_y in dataloader:
                optimizer.zero_grad()
                outputs = self.model(batch_X)
                loss = criterion(outputs, batch_y)
                loss.backward()
                optimizer.step()
        return self

    def predict_proba(self, X):
        if self.model is None:
            raise Exception("Model not trained")
        if isinstance(X, pd.DataFrame):
            X = X.values
        self.model.eval()
        with torch.no_grad():
            X_tensor = torch.tensor(X, dtype=torch.float32).to(self.device)
            outputs = self.model(X_tensor)
            prob_1 = outputs.numpy().flatten()
            prob_0 = 1 - prob_1
            return np.vstack([prob_0, prob_1]).T

    def predict(self, X):
        probs = self.predict_proba(X)
        return (probs[:, 1] > 0.5).astype(int)

def train_and_evaluate(filepath='brazilian-malware.csv'):
    # 1. Load
    df = load_data(filepath)
    label_col = identify_label_column(df)
    
    # 2. Preprocess (Fit Mode)
    X, encoders, scaler = preprocess_data(df, label_col=label_col)
    y = get_target(df, label_col)
    
    feature_names = list(X.columns)
    
    # 3. Split
    X_train, X_test, y_train, y_test = split_data(X, y)
    
    # 4. Define Models
    models = {
        'Logistic Regression': LogisticRegression(max_iter=3000), 
        'Decision Tree': DecisionTreeClassifier(),
        'Random Forest': RandomForestClassifier(n_estimators=50, random_state=42),
        'XGBoost': xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42),
        'LightGBM': lgb.LGBMClassifier(verbose=-1, random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=50, random_state=42), # Replaced CatBoost
        'PyTorch MLP': PyTorchMLP(epochs=5)
    }
    
    results = []
    
    # 5. CV Loop
    skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
    
    print("\nStarting Cross-Validation...")
    for name, model in models.items():
        try:
            start_time = time.time()
            
            acc_scores = cross_val_score(model, X_train, y_train, cv=skf, scoring='accuracy')
            auc_scores = cross_val_score(model, X_train, y_train, cv=skf, scoring='roc_auc')
            
            elapsed = time.time() - start_time
            print(f"Model: {name} | Acc: {acc_scores.mean():.4f} (+/- {acc_scores.std():.4f}) | AUC: {auc_scores.mean():.4f} | Time: {elapsed:.2f}s")
            
            results.append({
                'Model': name,
                'Accuracy': acc_scores.mean(),
                'AUC': auc_scores.mean(),
                'ModelObj': model
            })
        except Exception as e:
            print(f"Model {name} failed: {e}")
            import traceback
            traceback.print_exc()

    if not results:
        print("No models trained successfully.")
        return
        
    # 6. Select Best
    best_result = max(results, key=lambda x: x['AUC'])
    print(f"\nBest Model: {best_result['Model']} with AUC: {best_result['AUC']:.4f}")
    
    # 7. Final Train & Test
    best_model = best_result['ModelObj']
    best_model.fit(X_train, y_train)
    
    y_pred = best_model.predict(X_test)
    y_proba = best_model.predict_proba(X_test)[:, 1]
    
    final_acc = accuracy_score(y_test, y_pred)
    final_auc = roc_auc_score(y_test, y_proba)
    
    print(f"Final Test Evaluation - Acc: {final_acc:.4f}, AUC: {final_auc:.4f}")
    
    # 8. Save
    with open('model.pkl', 'wb') as f:
        pickle.dump(best_model, f)
    print("Model saved to model.pkl")
    
    with open('model_metadata.pkl', 'wb') as f:
        pickle.dump({
            'feature_names': feature_names,
            'encoders': encoders,
            'scaler': scaler
        }, f)
    print("Model metadata saved to model_metadata.pkl")

if __name__ == "__main__":
    train_and_evaluate()
