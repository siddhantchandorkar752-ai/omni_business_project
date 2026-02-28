import streamlit as st
import pandas as pd
from PIL import Image
from ultralytics import YOLO
import cv2
import numpy as np

st.set_page_config(page_title="Omni-Sight AI: Extreme Detection", layout="wide")
st.title("🛡️ Enterprise AI: Vision & Dynamic Pricing Engine")

class PricingEngine:
    def __init__(self):
        self.base_price = 1000.0
        self.discounts = {"scratches": 0.40, "Anomaly": 0.60, "Perfect": 0.0}

    def calculate(self, label):
        discount = self.discounts.get(label, 0.40) # Default heavy discount for any detection
        price = self.base_price * (1 - discount)
        action = "Standard Sale" if label == "Perfect" else "Reject / Flash Sale"
        return price, action

engine = PricingEngine()

def process_vision(img):
    # 1. Convert to OpenCV Format
    open_cv_image = np.array(img.convert('RGB'))
    res_img = open_cv_image.copy()
    gray = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2GRAY)
    
    # 2. EXTREME DETECTION: Adaptive Thresholding
    # Ye deewar ke plaster aur micro-cracks ko highlight karega
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    detected_label = "Perfect"
    count = 0
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 500 < area < 50000: # Filter small noise and large backgrounds
            x, y, w, h = cv2.boundingRect(cnt)
            # Blue Box for any texture anomaly
            cv2.rectangle(res_img, (x, y), (x+w, y+h), (255, 0, 0), 3)
            detected_label = "Anomaly"
            count += 1

    # 3. YOLO Overlay (If it finds specific objects)
    model = YOLO("yolov8n.pt")
    yolo_results = model(img, conf=0.1)
    if len(yolo_results[0].boxes) > 0:
        res_img = yolo_results[0].plot(img=res_img)
        class_id = int(yolo_results[0].boxes.cls[0])
        detected_label = yolo_results[0].names[class_id]

    return res_img, detected_label, count

st.subheader("Live Inspection Pipeline (Extreme Sensitivity)")
uploaded_file = st.file_uploader("Upload Surface Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    with st.spinner("AI Engine: Hunting for Anomalies..."):
        try:
            processed_array, final_label, box_count = process_vision(image)
            st.image(processed_array, caption=f"Analysis Complete: {box_count} areas flagged.", use_container_width=True)
            
            price, action = engine.calculate(final_label)
            
            if final_label != "Perfect":
                st.error(f"🚨 ALERT: {final_label} Detected! Revenue impact triggered.")
            else:
                st.success("✅ Quality Verified.")

            st.table(pd.DataFrame([{
                "ID": uploaded_file.name[:5],
                "Condition": final_label.upper(),
                "Price": f"₹{price}",
                "Action": action
            }]))
            
        except Exception as e:
            st.error(f"System Error: {e}")