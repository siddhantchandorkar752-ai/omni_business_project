import streamlit as st
import pandas as pd
from PIL import Image
from ultralytics import YOLO
import numpy as np
import os

st.set_page_config(page_title="Business Brain Dashboard", layout="wide")
st.title("Enterprise Defect & Dynamic Pricing Engine")

class PricingEngine:
    def __init__(self):
        self.base_price = 1000.0
        self.discounts = {
            "scratches": 0.40, "pitted_surface": 0.50, "crazing": 0.35,
            "patches": 0.45, "inclusion": 0.40, "rolled-in_scale": 0.50,
            "Grade_A_Perfect": 0.0
        }

    def calculate_price(self, detection_class):
        discount = self.discounts.get(detection_class, 0.25) # Default 25% if something detected
        return self.base_price * (1 - discount)

    def get_action(self, detection_class):
        if detection_class == "Grade_A_Perfect": return "Standard Sale"
        return "Flash Sale - Defect Detected"

engine = PricingEngine()

st.subheader("Live Vision Inspection Feed")
uploaded_file = st.file_uploader("Upload Image for Deep Analysis", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    with st.spinner("AI Engine: Intensifying Scan..."):
        try:
            # GURU TRICK: Hum confidence threshold (conf=0.15) kam kar rahe hain 
            # taaki model har suspicious crack/debris par box banaye
            model = YOLO("yolov8n.pt") 
            results = model(image, conf=0.15, iou=0.45) # Sensitivity increased
            
            # --- FORCED BOUNDING BOX LOGIC ---
            res_img_array = results[0].plot(labels=True, boxes=True, conf=True) 
            res_img = Image.fromarray(res_img_array[..., ::-1]) 
            
            st.image(res_img, caption="AI Analysis: Deep Defect Mapping Enabled", use_container_width=True)
            
            # Dynamic Decision Making
            if len(results[0].boxes) > 0:
                class_id = int(results[0].boxes.cls[0])
                detected_class = results[0].names[class_id]
                st.warning(f"🚨 Defect(s) Identified: {len(results[0].boxes)} areas flagged.")
            else:
                detected_class = "Grade_A_Perfect"
                st.success("✅ Surface Integrity Verified.")
            
            final_price = engine.calculate_price(detected_class)
            action = engine.get_action(detected_class)
            
            st.subheader("AI Business Action Triggered")
            df = pd.DataFrame([{
                "Item_ID": f"ITEM_{uploaded_file.name[:5].upper()}",
                "Status": "DETECTION ACTIVE",
                "Original_Price": f"₹{engine.base_price}",
                "Final_Price": f"₹{final_price}",
                "Action": action
            }])
            st.dataframe(df, use_container_width=True)
            
        except Exception as e:
            st.error(f"Inference Error: {e}")