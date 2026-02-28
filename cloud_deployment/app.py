import streamlit as st
import pandas as pd
from PIL import Image
from ultralytics import YOLO
import cv2
import numpy as np
import os

# --- Page Config ---
st.set_page_config(page_title="Omni-Sight AI Dashboard", layout="wide")
st.title("🛡️ Enterprise AI: Vision & Dynamic Pricing Engine")

# --- Pricing Engine Logic ---
class PricingEngine:
    def __init__(self):
        self.base_price = 1000.0
        self.defect_discounts = {
            "scratches": 0.40, "pitted_surface": 0.50, "crazing": 0.35,
            "patches": 0.45, "inclusion": 0.40, "rolled-in_scale": 0.50,
            "Anomaly": 0.60 # Default discount for unknown debris/cracks
        }

    def calculate(self, label):
        discount = self.defect_discounts.get(label, 0.20)
        final_price = self.base_price * (1 - discount)
        action = "Flash Sale" if discount < 1.0 else "Recycle"
        if label == "Perfect": action = "Standard Sale"; final_price = self.base_price
        return final_price, action

engine = PricingEngine()

# --- Hybrid Vision Engine ---
def process_vision(img):
    # 1. YOLO Detection (Confidence 0.15 for high sensitivity)
    model = YOLO("yolov8n.pt") 
    results = model(img, conf=0.15)
    res_img = results[0].plot(boxes=True, labels=True)
    
    detected_label = "Perfect"
    if len(results[0].boxes) > 0:
        class_id = int(results[0].boxes.cls[0])
        detected_label = results[0].names[class_id]

    # 2. OpenCV Anomaly Detection (For cracks/debris YOLO misses)
    open_cv_image = np.array(img)
    gray = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    anomaly_found = False
    for cnt in contours:
        if cv2.contourArea(cnt) > 800: # Sensitivity for debris size
            x, y, w, h = cv2.boundingRect(cnt)
            # Drawing a Blue Box for "Unknown Anomaly"
            cv2.rectangle(res_img, (x, y), (x+w, y+h), (255, 0, 0), 3)
            anomaly_found = True
            if detected_label == "Perfect": detected_label = "Anomaly"

    return res_img, detected_label

# --- Sidebar / Dashboard Stats ---
st.sidebar.header("System Health")
st.sidebar.metric("Vision Engine", "ACTIVE", "Hybrid Mode")
st.sidebar.metric("Pricing Logic", "CONNECTED")

# --- Main UI ---
st.subheader("Live Inspection Pipeline")
uploaded_file = st.file_uploader("Upload Surface Image (Metal/Debris/Cracks)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    with st.spinner("Executing Deep Tissue Scan..."):
        try:
            processed_array, final_label = process_vision(image)
            # Convert BGR (OpenCV) back to RGB for Streamlit
            final_img = Image.fromarray(processed_array[..., ::-1] if len(processed_array.shape)==3 else processed_array)
            
            st.image(final_img, caption=f"Analysis Result: {final_label}", use_container_width=True)
            
            # Pricing Trigger
            price, action = engine.calculate(final_label)
            
            if final_label != "Perfect":
                st.error(f"🚨 ALERT: {final_label} Detected!")
            else:
                st.success("✅ Quality Check Passed.")

            # Business Data Table
            st.subheader("Business Impact Analysis")
            results_df = pd.DataFrame([{
                "Inspection_ID": f"AI_{uploaded_file.name[:4].upper()}",
                "Condition": final_label.upper(),
                "Market_Value": f"₹{price}",
                "Recommended_Action": action
            }])
            st.table(results_df)
            
        except Exception as e:
            st.error(f"System Glitch: {e}")