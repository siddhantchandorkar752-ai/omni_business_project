import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Business Brain Dashboard", layout="wide")
st.title("Enterprise Defect & Dynamic Pricing Engine")

col1, col2, col3 = st.columns(3)
col1.metric("Total Inspected Today", "1,042", "+12")
col2.metric("Grade B (Flash Sale triggers)", "84", "-2")
col3.metric("Revenue Recovered", "₹58,800", "+8%")

st.subheader("Live Detection Feed")
st.info("YOLOv8 Vision Engine Active. Waiting for camera stream...")

data = {
    "Item_ID": ["ITEM_8470", "ITEM_8471", "ITEM_8472", "ITEM_8473"],
    "Quality": ["Grade_A_Perfect", "Grade_A_Perfect", "Grade_B_Minor", "Grade_C_Reject"],
    "Original_Price": [1000, 1000, 1000, 1000],
    "Final_Price": [1000, 1000, 700, 0],
    "Action": ["Standard Sale", "Standard Sale", "Flash Sale - 30% Off", "Recycle Pipeline"]
}
df = pd.DataFrame(data)

st.subheader("Dynamic Pricing Logs")
st.dataframe(df, use_container_width=True)