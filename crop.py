# -*- coding: utf-8 -*-
"""crop.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1hrFCgEkiWx35ZfRbkFKsIduKttZhs91h
"""

import numpy as np
import pandas as pd
df=pd.read_csv("/content/Crop_recommendationV2_kaggle.csv")
df

pip install pandas scikit-learn xgboost

# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report, log_loss

# Load the dataset
df = pd.read_csv('Crop_recommendationV2_kaggle.csv')

# Features and target
X = df.drop('label', axis=1)
y = df['label']

# Encode target labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Function to train & evaluate model
def evaluate_model(model, model_name):
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)

    acc = accuracy_score(y_test, y_pred)
    loss = log_loss(y_test, y_pred_proba)
    report = classification_report(y_test, y_pred, target_names=le.classes_)

    print(f"\n==== {model_name} ====")
    print(f"Accuracy: {acc:.4f}")
    print(f"Log Loss: {loss:.4f}")
    print("Classification Report:")
    print(report)

# Initialize models
rf_model = RandomForestClassifier(n_estimators=200, random_state=42)
xgb_model = XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', n_estimators=100, max_depth=5, random_state=42)
svc_model = SVC(kernel='rbf', probability=True, random_state=42)

# Evaluate models
evaluate_model(rf_model, "Random Forest")
evaluate_model(xgb_model, "XGBoost")
evaluate_model(svc_model, "SVC")

!pip install gradio

# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import gradio as gr

# Load the dataset
df = pd.read_csv('Crop_recommendationV2_kaggle.csv')

# Features and target
X = df.drop('label', axis=1)
y = df['label']

# Encode target labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train RandomForestClassifier
rf_model = RandomForestClassifier(n_estimators=200, random_state=42)
rf_model.fit(X_train_scaled, y_train)

# Gradio Prediction Function
def predict_crop(temperature, humidity, rainfall, soil_moisture, ph):
    # Prepare input
    input_data = [[temperature, humidity, ph, rainfall, soil_moisture]]
    input_scaled = scaler.transform(input_data)

    # Predict
    pred_encoded = rf_model.predict(input_scaled)[0]
    pred_label = le.inverse_transform([pred_encoded])[0]

    return f"🌾 Predicted Best Crop: **{pred_label}**"

# Gradio Interface
interface = gr.Interface(
    fn=predict_crop,
    inputs=[
        gr.Number(label="Temperature (°C)"),
        gr.Number(label="Humidity (%)"),
        gr.Number(label="Rainfall (mm)"),
        gr.Number(label="Soil Moisture (%)"),
        gr.Number(label="pH")
    ],
    outputs=gr.Textbox(label="Recommended Crop"),
    title="🌾 Crop Recommendation System",
    description="Enter the soil and climate parameters to predict the most suitable crop.",
)

# Launch Gradio App
interface.launch()

