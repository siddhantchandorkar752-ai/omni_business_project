import streamlit as st
import pandas as pd
from PIL import Image
import cv2
import numpy as np
from ultralytics import YOLO

st.set_page_config(page_title="Omni-Sight AI: Final Fix", layout="wide")
st.title("🛡️ Enterprise AI: Vision & Dynamic Pricing Engine")

# --- SMART PRICING LOGIC ---
def get_business_impact(label, anomaly_score):
    base_price = 1000.0
    # Agar anomaly_score zyada hai, toh discount badhao
    if label == "Perfect" and anomaly_score < 5:
        return base_price, "Standard Sale", "Grade A"
    else:
        # Dynamic Discount based on how much mess is detected
        discount = min(0.9, 0.2 + (anomaly_score * 0.05)) 
        final_price = base_price * (1 - discount)
        return final_price, "Flash Sale / Reject", "Grade B/C"

# --- SUPER SENSITIVE VISION ENGINE ---
def analyze_frame(img):
    # Image ko process karne ke liye taiyar karein
    open_cv_image = np.array(img.convert('RGB'))
    res_img = open_cv_image.copy()
    gray = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2GRAY)
    
    # Texture Detection: Ye har ek crack aur malbe ko highlight karega
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 30, 100) # Bahut sensitive settings
    
    # Bounding Boxes dhoondhna
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    anomaly_count = 0
    for cnt in contours:
        if cv2.contourArea(cnt) > 100: # Chote defects bhi pakdega
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(res_img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            anomaly_count += 1

    label = "Anomaly" if anomaly_count > 5 else "Perfect"
    return res_img, label, anomaly_count

st.subheader("Live Inspection Pipeline (Precision Mode)")
uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    with st.spinner("AI Engine: Scanning every pixel..."):
        try:
            processed_img, status, score = analyze_frame(image)
            st.image(processed_img, caption=f"Detection Score: {score} anomalies found", use_container_width=True)
            
            # Business Logic
            final_price, action, grade = get_business_impact(status, score)
            
            if status != "Perfect":
                st.error(f"🚨 ALERT: Surface Anomalies Detected ({grade})")
            else:
                st.success("✅ Quality Verified (Grade A)")

            # Results Table
            st.table(pd.DataFrame([{
                "Inspection_ID": uploaded_file.name[:5].upper(),
                "Detected_Grade": grade,
                "Dynamic_Price": f"₹{final_price}",
                "Market_Action": action
            }]))
            
        except Exception as e:
            st.error(f"System Error: {e}")