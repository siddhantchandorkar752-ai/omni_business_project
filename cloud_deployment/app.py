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
        # Mapping common metal defects to discount logic
        self.discounts = {
            "scratches": 0.40,      
            "pitted_surface": 0.50,
            "crazing": 0.35,
            "patches": 0.45,
            "inclusion": 0.40,
            "rolled-in_scale": 0.50,
            "Grade_A_Perfect": 0.0
        }

    def calculate_price(self, detection_class):
        discount = self.discounts.get(detection_class, 0.10)
        return self.base_price * (1 - discount)

    def get_action(self, detection_class):
        discount = self.discounts.get(detection_class, 0.0)
        if discount >= 0.50: return "Recycle Pipeline"
        if discount > 0.0: return f"Flash Sale - {int(discount*100)}% Off"
        return "Standard Sale"

engine = PricingEngine()

# Dashboard Stats
col1, col2, col3 = st.columns(3)
col1.metric("Total Inspected Today", "1,043", "+1")
col2.metric("Grade B (Flash Sale)", "85", "+1")
col3.metric("Revenue Recovered", "₹59,500", "+8%")

st.subheader("Live Vision Inspection Feed")
uploaded_file = st.file_uploader("Upload Metal Surface Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    with st.spinner("YOLOv8 Engine scanning for defects..."):
        try:
            # GURU MANTRA: Yahan hum apne Step 8 waale trained weights use kar rahe hain
            # Agar weights file nahi milti toh default load hoga
            model_path = "models/yolo_vision_weights/weights/best.pt"
            if os.path.exists(model_path):
                model = YOLO(model_path)
            else:
                model = YOLO("yolov8n.pt") 

            # Running Inference
            results = model(image)
            
            # --- BOUNDING BOX LOGIC ---
            # results[0].plot() apne aap detected objects par boxes aur labels banata hai
            res_img_array = results[0].plot() 
            res_img = Image.fromarray(res_img_array[..., ::-1]) # BGR to RGB conversion
            
            st.image(res_img, caption="AI Analysis with Bounding Boxes", use_container_width=True)
            
            # Extracting detected class
            if len(results[0].boxes) > 0:
                class_id = int(results[0].boxes.cls[0])
                detected_class = results[0].names[class_id]
            else:
                detected_class = "Grade_A_Perfect"
            
            final_price = engine.calculate_price(detected_class)
            action = engine.get_action(detected_class)
            
            st.subheader("AI Business Action Triggered")
            df = pd.DataFrame([{
                "Item_ID": f"ITEM_{uploaded_file.name[:5].upper()}",
                "Detected_Defect": detected_class,
                "Final_Price": f"₹{final_price}",
                "Action": action
            }])
            st.dataframe(df, use_container_width=True)
            
        except Exception as e:
            st.error(f"Inference Error: {e}")