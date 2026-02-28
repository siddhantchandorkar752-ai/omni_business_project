# 🛡️ Omni-Sight AI: Enterprise Defect & Dynamic Pricing Engine

**A Production-Ready Hybrid Vision System for Industrial Quality Control**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge.svg)](https://omnibusinessproject-bdbhb4fxkeghedjlyv8u9x.streamlit.app)

## 🚀 Project Overview
Omni-Sight AI is not just a defect detector; it's a **Business Intelligence tool**. It uses a hybrid Computer Vision pipeline to identify surface defects (cracks, debris, scratches) and automatically calculates the financial impact in real-time.

### ✨ Key Features
- **Hybrid Vision Engine:** Combines **YOLOv8 Deep Learning** for object recognition and **OpenCV Adaptive Thresholding** for micro-texture anomaly detection.
- **Dynamic Pricing Logic:** Automatically triggers discounts (Flash Sales) or Rejection protocols based on the severity of the detected anomaly.
- **Synthetic Data Generation:** Leveraged **GANs (Generative Adversarial Networks)** to augment the training dataset, improving model robustness against rare defects.
- **Live Cloud Dashboard:** Fully responsive executive dashboard deployed via Streamlit Cloud.

---

## 🛠️ Tech Stack
| Category | Technology |
| :--- | :--- |
| **Language** | Python 3.13 |
| **Deep Learning** | Ultralytics YOLOv8, PyTorch |
| **Image Processing** | OpenCV (Adaptive Thresholding, Canny Edge) |
| **Frontend/Cloud** | Streamlit, GitHub CI/CD |
| **Data Science** | NumPy, Pandas, GANs |

---

## 🏗️ Architecture
1. **Input:** User/Conveyor Belt camera uploads a surface image.
2. **Analysis:** The Hybrid Engine scans for known patterns (YOLO) and unknown textures (OpenCV).
3. **Decision:** Pricing Engine calculates `Market_Value = Base_Price * (1 - Anomaly_Score)`.
4. **Output:** Real-time visual bounding boxes and business action recommendations.

---

## 📸 Screenshots
> *Upload your project screenshots here to show the Bounding Boxes in action!*

---

## 🚦 Getting Started
1. Clone the repo: `git clone https://github.com/siddhantchandorkar752-ai/omni_business_project.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run locally: `streamlit run cloud_deployment/app.py`

---

## 👨‍💻 Developer
**Parth**
*Data Science Enthusiast | AI Vision Architect*
[LinkedIn Profile Link] | [Portfolio Link]
