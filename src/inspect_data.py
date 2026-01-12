import pandas as pd
import numpy as np

def inspect():
    df = pd.read_csv('brazilian-malware.csv', header=None, nrows=1000)
    print(f"Shape: {df.shape}")
    
    # Check for binary columns
    for col in df.columns:
        unique = df[col].dropna().unique()
        if len(unique) <= 2:
            print(f"Column {col} unique values: {unique}")
            
    # Print head
    print(df.head())

if __name__ == "__main__":
    inspect()
