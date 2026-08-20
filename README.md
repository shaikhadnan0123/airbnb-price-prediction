# 🗽 NYC Airbnb Price Predictor

<div align="center">

### From raw NYC Airbnb data to a fully deployed Machine Learning application 🚀

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-Machine%20Learning-orange?logo=scikitlearn)](https://scikit-learn.org/)
[![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react)](https://react.dev/)
[![Flask](https://img.shields.io/badge/Flask-API-black?logo=flask)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)](https://www.docker.com/)
[![Render](https://img.shields.io/badge/Backend-Render-46E3B7?logo=render)](https://render.com/)
[![Vercel](https://img.shields.io/badge/Frontend-Vercel-black?logo=vercel)](https://vercel.com/)

<br/>

> **Predicting NYC Airbnb nightly prices using an Extra Trees Regressor trained on real Airbnb listings.**

</div>

---

## ✨ Live Application

### 🌐 Frontend

**Vercel:** `YOUR_VERCEL_URL_HERE`

### ⚙️ Backend API

**Render:** [NYC Airbnb Price Prediction API](https://airbnb-price-prediction-lcnt.onrender.com)

### 🧠 API Status

```json
{
  "message": "Airbnb Price Prediction API is running",
  "model": "Extra Trees Regressor",
  "status": "healthy"
}
```

---

# 🎬 Project Journey

```text
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║   RAW DATA 📊                                             ║
║       ↓                                                    ║
║   DATA CLEANING 🧹                                         ║
║       ↓                                                    ║
║   TARGET ANALYSIS 🎯                                       ║
║       ↓                                                    ║
║   FEATURE ENGINEERING ⚙️                                   ║
║       ↓                                                    ║
║   MULTIPLE ML MODELS 🤖                                    ║
║       ↓                                                    ║
║   MODEL EVALUATION 📈                                      ║
║       ↓                                                    ║
║   EXTRA TREES SELECTED 🌳                                  ║
║       ↓                                                    ║
║   FLASK API 🚀                                             ║
║       ↓                                                    ║
║   DOCKER 🐳                                               ║
║       ↓                                                    ║
║   RENDER DEPLOYMENT ☁️                                     ║
║       ↓                                                    ║
║   REACT FRONTEND ⚛️                                        ║
║       ↓                                                    ║
║   VERCEL DEPLOYMENT ▲                                      ║
║                                                            ║
║              🎉 LIVE MACHINE LEARNING APP 🎉               ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

<div align="center">

### 🟢 Data → Model → API → Frontend → Cloud → Live

</div>

---

# 🎯 Project Overview

This project predicts the **nightly price of Airbnb listings in New York City**.

The application uses a machine learning model trained on NYC Airbnb data and allows users to enter listing information such as:

* 📍 Neighbourhood Group
* 🏘️ Neighbourhood
* 🏠 Room Type
* 🌐 Latitude
* 🌐 Longitude
* 🌙 Minimum Nights
* ⭐ Number of Reviews
* 📊 Reviews Per Month
* 👤 Host Listings Count
* 📅 Availability Throughout the Year

The trained model processes these features and returns an estimated nightly Airbnb price.

---

# 🧠 Machine Learning Model

Several regression models were explored during the project:

| Model                        | Purpose                    |
| ---------------------------- | -------------------------- |
| 📏 Linear Regression         | Baseline model             |
| 🌲 Random Forest Regressor   | Ensemble learning          |
| 📈 HistGradientBoosting      | Gradient boosting approach |
| 🌳 **Extra Trees Regressor** | ⭐ Final selected model     |

The final deployed model is:

## 🌳 Extra Trees Regressor

The model was saved using:

```text
models/extra_trees_model.joblib
```

---

# 📊 Final Model Performance

| Metric        |                Score |
| ------------- | -------------------: |
| MAE           |           **$38.55** |
| RMSE          |           **$61.63** |
| R² Score      |           **0.5083** |
| R² Percentage |            **50.8%** |
| Price Scope   | **$10 – $500/night** |
| Listings Used |           **47,840** |

### What does this mean?

On average, the model's prediction differs from the actual listing price by approximately:

> 💵 **$38.55**

The model performs differently across price ranges:

| Price Range           |     MAE |
| --------------------- | ------: |
| Budget ($0–$100)      |  $20.71 |
| Mid-range ($100–$200) |  $35.92 |
| High ($200–$500)      | $100.86 |

This analysis helped reveal an important insight:

> **Predicting high-priced Airbnb listings is significantly more difficult because premium properties have greater variation and fewer comparable examples.**

---

# 🎯 Target Variable Journey

One of the biggest learning experiences in this project was understanding the **target variable**.

The target variable is:

```python
price
```

Initially, the dataset contained extreme values:

```text
Minimum Price: $10
Maximum Price: $10,000
```

Some listings had unusually high prices, which created a heavily skewed distribution.

Instead of blindly training the model on everything, the data was investigated carefully.

The final project scope became:

```text
$10 – $500 per night
```

After applying this scope:

```text
Total Listings: 47,840
Minimum Price: $10
Maximum Price: $500
Average Price: $131.56
```

This was an important lesson:

> 🎯 **Machine learning is not only about choosing an algorithm. Understanding the target variable can completely change the quality and meaning of a project.**

---

# ⚙️ Feature Engineering

The model uses numerical and categorical features.

One engineered feature was:

```python
location_interaction = latitude * longitude
```

This feature is automatically calculated before prediction.

The frontend sends the original listing information:

```text
Latitude
Longitude
        ↓
location_interaction
        ↓
Extra Trees Model
        ↓
Predicted Price
```

---

# 🔥 Feature Importance

The most influential feature discovered by the Extra Trees model was:

```text
Room Type → Entire home/apt
```

Other important features included:

* 🗽 Manhattan
* 📍 Longitude
* 📍 Latitude
* 🧮 Location Interaction
* 📅 Availability
* 🌙 Minimum Nights
* ⭐ Reviews Per Month
* 📝 Number of Reviews
* 👤 Host Listings Count

This showed that **property type and location play a major role in Airbnb pricing**.

---

# 🖥️ Application Architecture

```text
                         ┌─────────────────────┐
                         │   React Frontend    │
                         │                     │
                         │  User enters Airbnb │
                         │  listing details    │
                         └──────────┬──────────┘
                                    │
                                    │ POST /predict
                                    ▼
                         ┌─────────────────────┐
                         │     Flask API       │
                         │                     │
                         │ Feature Engineering │
                         │                     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Extra Trees Model   │
                         │                     │
                         │ .joblib             │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Predicted Price 💰  │
                         └─────────────────────┘
```

---

# 🚀 API

The Flask backend provides a prediction endpoint.

### Endpoint

```text
POST /predict
```

### Example Input

```json
{
  "neighbourhood_group": "Manhattan",
  "neighbourhood": "Midtown",
  "room_type": "Entire home/apt",
  "latitude": 40.7549,
  "longitude": -73.9840,
  "minimum_nights": 3,
  "number_of_reviews": 100,
  "reviews_per_month": 1.5,
  "calculated_host_listings_count": 1,
  "availability_365": 180
}
```

### Example Response

```json
{
  "predicted_price": 205.79
}
```

---

# 🐳 Docker

The backend was containerized using Docker.

### Build the Docker image

```bash
docker build -t airbnb-price-api .
```

### Run the container

```bash
docker run -p 5000:5000 airbnb-price-api
```

Then open:

```text
http://127.0.0.1:5000
```

---

# 📂 Project Structure

```text
airbnb-price-prediction/
│
├── data/
│   ├── raw/
│   └── cleaned/
│       ├── cleaned_airbnb.csv
│       └── cleaned_airbnb_typical.csv
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
├── models/
│   ├── extra_trees_model.joblib
│   ├── extra_trees_model_compressed.joblib
│   ├── random_forest_model.joblib
│   ├── hist_gradient_boosting_model.joblib
│   ├── linear_regression_model.joblib
│   └── model_metrics.json
│
├── notebooks/
│   ├── exploration.ipynb
│   └── modeling.ipynb
│
├── src/
│   ├── app.py
│   ├── data_cleaning.py
│   ├── modeling.py
│   └── visualization.py
│
├── Dockerfile
├── .dockerignore
├── requirements.txt
└── README.md
```

---

# 🛠️ Technology Stack

### Machine Learning

* Python
* Pandas
* NumPy
* Scikit-learn

### Visualization

* Matplotlib
* Seaborn

### Backend

* Flask
* Flask-CORS
* Joblib

### Frontend

* React
* Vite
* JavaScript
* CSS

### Deployment

* Docker
* Render
* Vercel
* GitHub

---

# 🧪 Challenges and What I Learned

This project was not a straight line.

There were multiple errors, failed attempts, debugging sessions, and moments where the project needed to be stopped and understood before moving forward.

Some challenges included:

### ❌ Understanding the Target Variable

The original dataset contained prices up to:

```text
$10,000
```

Instead of immediately removing values, the expensive listings were investigated first.

This led to a better understanding of:

* Outliers
* Target distribution
* Project scope
* Model limitations

---

### ❌ Different Model Performance

Training multiple models helped demonstrate that:

> **The most complicated model is not automatically the best model.**

Each model needed to be evaluated using:

* MAE
* MSE
* RMSE
* R² Score

The Extra Trees Regressor was selected as the final model.

---

### ❌ API Errors

During API development, prediction requests initially produced errors because the input needed to match the training pipeline.

The lesson was simple but important:

> **The features used during prediction must match the features used during training.**

This included recreating:

```python
location_interaction
```

inside the API before calling the model.

---

### ❌ Docker Problems

The deployment journey included:

* Docker daemon connection issues
* Missing Dockerfile errors
* Large build contexts
* Slow Docker builds

A `.dockerignore` file was added to prevent unnecessary files such as:

```text
.venv
node_modules
.git
__pycache__
```

from being sent into the Docker build context.

This dramatically improved the build process.

---

### ❌ Connecting Frontend and Backend

The frontend initially communicated with:

```text
http://127.0.0.1:5000
```

This works locally but not after deployment.

The frontend was updated to communicate with the deployed Render API instead.

```text
React Frontend
       ↓
Render API
       ↓
Extra Trees Model
       ↓
Prediction
```

---

# ☁️ Deployment Journey

```text
GitHub
   │
   ├──────────────► Render
   │                 │
   │                 ▼
   │            Flask API
   │                 │
   │                 ▼
   │          ML Model (.joblib)
   │
   └──────────────► Vercel
                     │
                     ▼
               React Frontend
                     │
                     ▼
              🌍 LIVE APPLICATION
```

---

# 🏆 What This Project Taught Me

This project changed my understanding of Machine Learning.

At the beginning, the focus was mainly:

```text
Dataset → Train Model → Get Prediction
```

By the end, the understanding became:

```text
Data Understanding
        ↓
Data Cleaning
        ↓
Target Analysis
        ↓
Feature Engineering
        ↓
Model Experimentation
        ↓
Model Evaluation
        ↓
Error Analysis
        ↓
Model Saving
        ↓
API Development
        ↓
Frontend Development
        ↓
Docker
        ↓
Cloud Deployment
        ↓
Live Application 🚀
```

The biggest lesson:

> ## 🧠 A Machine Learning model is not the final product.
>
> A working system around the model is the real product.

---

# 🌟 The Journey

This project represents more than an Airbnb price prediction model.

It represents the process of learning through mistakes.

There were moments of confusion.

There were API errors.

There were Docker errors.

There were model evaluation problems.

There were deployment problems.

But every error became part of the learning process.

```text
ERROR
  ↓
DEBUG
  ↓
UNDERSTAND
  ↓
FIX
  ↓
LEARN
  ↓
MOVE FORWARD 🚀
```

Seeing the final application deployed online was the moment where the entire journey finally connected.

> **Hard work does not always feel rewarding while you are doing it. Sometimes you only understand how far you have come when you finally look back.**

---

<div align="center">

# 🎉 From Raw Data to a Live ML Application

### Built with curiosity, debugging, persistence, and a lot of learning.

<br/>

### ⭐ If you found this project interesting, consider giving it a star!

<br/>

**Made with ❤️ by Shaikh Adnan**

© 2026 Shaikh Adnan. All rights reserved.

</div>
