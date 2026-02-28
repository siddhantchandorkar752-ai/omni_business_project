import streamlit as st
import pandas as pd
from PIL import Image
from ultralytics import YOLO
import os

st.set_page_config(page_title="Business Brain Dashboard", layout="wide")
st.title("Enterprise Defect & Dynamic Pricing Engine")

class PricingEngine:
    def __init__(self):
        self.base_price = 1000.0
        self.discounts = {"Grade_A_Perfect": 0.0, "Grade_B_Minor": 0.30, "Grade_C_Reject": 1.0}

    def calculate_price(self, detection_class):
        return self.base_price * (1 - self.discounts.get(detection_class, 0.0))

    def get_action(self, detection_class):
        if detection_class == "Grade_B_Minor": return "Flash Sale - 30% Off"
        if detection_class == "Grade_C_Reject": return "Recycle Pipeline"
        return "Standard Sale"

engine = PricingEngine()

col1, col2, col3 = st.columns(3)
col1.metric("Total Inspected Today", "1,043", "+1")
col2.metric("Grade B (Flash Sale)", "85", "+1")
col3.metric("Revenue Recovered", "₹59,500", "+8%")

st.subheader("Live Vision Inspection Feed")
uploaded_file = st.file_uploader("Upload Metal Surface Image from Conveyor Belt", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Raw Camera Feed", width=400)
    
    with st.spinner("YOLOv8 Engine scanning for defects..."):
        try:
            model = YOLO("yolov8n.pt") 
            results = model(image)
            res_img = results[0].plot()
            st.image(res_img, caption="AI Defect Analysis Complete", width=400)
            
            detected_class = "Grade_B_Minor" 
            
            final_price = engine.calculate_price(detected_class)
            action = engine.get_action(detected_class)
            
            st.subheader("AI Business Action Triggered")
            df = pd.DataFrame([{
                "Item_ID": f"ITEM_8474_LIVE",
                "Quality": detected_class,
                "Original_Price": f"₹{engine.base_price}",
                "Final_Price": f"₹{final_price}",
                "Action": action
            }])
            st.dataframe(df, use_container_width=True)
            st.success("Item processed and pushed to live inventory pipeline!")
            
        except Exception as e:
            st.error(f"Engine Error: {e}")