# 🏠 Airbnb Price Prediction and Market Analysis

An end-to-end Machine Learning project that predicts Airbnb listing prices in New York City using historical Airbnb data. This project demonstrates the complete data science workflow, including data cleaning, exploratory data analysis (EDA), feature engineering, model building, and evaluation.

---

## 📌 Project Overview

Airbnb hosts often struggle to determine the right price for their listings. Pricing too low results in lost revenue, while pricing too high can reduce bookings.

This project uses historical Airbnb listing data to build a Linear Regression model that predicts the price of a new listing based on its characteristics such as location, room type, reviews, and availability.

---

## 🎯 Objectives

- Clean and preprocess Airbnb data
- Perform Exploratory Data Analysis (EDA)
- Visualize important trends and patterns
- Build a Linear Regression model
- Evaluate model performance using regression metrics
- Organize the project using a modular structure

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Jupyter Notebook
- Joblib

---

## 📂 Project Structure

```text
airbnb-price-prediction/
│
├── data/
│   ├── raw/
│   └── cleaned/
│
├── notebooks/
│   ├── exploration.ipynb
│   └── modeling.ipynb
│
├── src/
│   ├── data_cleaning.py
│   ├── modeling.py
│   └── visualization.py
│
├── models/
│   └── linear_regression_model.pkl
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 📊 Dataset

- **Dataset:** New York City Airbnb Open Data
- **Source:** Kaggle
- **Records:** 48,895 listings
- **Features:** 16

---

## 🔍 Exploratory Data Analysis

The project includes:

- Price Distribution
- Room Type Analysis
- Neighborhood Analysis
- Correlation Heatmap
- Boxplots
- Histograms

---

## 🤖 Machine Learning Model

**Algorithm Used**

- Linear Regression

### Workflow

- Data Cleaning
- Missing Value Handling
- Feature Engineering
- One-Hot Encoding
- Train-Test Split
- Model Training
- Prediction
- Evaluation

---

## 📈 Model Performance

| Metric | Score |
|--------|-------:|
| Mean Absolute Error (MAE) | 68.15 |
| Mean Squared Error (MSE) | 38228.11 |
| Root Mean Squared Error (RMSE) | 195.52 |
| R² Score | 0.136 |

---

## 🚀 Future Improvements

- Random Forest Regressor
- XGBoost Regressor
- Hyperparameter Tuning
- Feature Selection
- Model Deployment using Flask or Streamlit

---

## 📚 Key Concepts Learned

- Data Cleaning
- Feature Engineering
- One-Hot Encoding
- Linear Regression
- Model Evaluation
- Data Visualization
- Python for Data Analysis

---

## 👨‍💻 Author

**Shaikh Adnan**

- GitHub: https://github.com/shaikhadnan0123
- LinkedIn: *(Add your LinkedIn profile URL here)*

---

## ⭐ If you found this project useful, consider giving it a star!
