from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import os

# -----------------------------
# CREATE FLASK APP
# -----------------------------

app = Flask(__name__)
CORS(app)


# -----------------------------
# PROJECT PATHS
# -----------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "extra_trees_model.joblib"
)


# -----------------------------
# LOAD TRAINED MODEL
# -----------------------------

model = joblib.load(MODEL_PATH)

print("Model loaded successfully.")
print(f"Model path: {MODEL_PATH}")


# -----------------------------
# REQUIRED INPUT FEATURES
# -----------------------------

REQUIRED_FEATURES = [
    "neighbourhood_group",
    "neighbourhood",
    "room_type",
    "latitude",
    "longitude",
    "minimum_nights",
    "number_of_reviews",
    "reviews_per_month",
    "calculated_host_listings_count",
    "availability_365"
]


# -----------------------------
# HOME ROUTE
# -----------------------------

@app.route("/")
def home():

    return jsonify({
        "status": "healthy",
        "message": "Airbnb Price Prediction API is running",
        "model": "Extra Trees Regressor"
    })


# -----------------------------
# PREDICTION ROUTE
# -----------------------------

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # Receive JSON data
        data = request.get_json()

        # Check if JSON was provided
        if not data:
            return jsonify({
                "error": "No input data provided"
            }), 400

        # Check for missing features
        missing_features = [
            feature
            for feature in REQUIRED_FEATURES
            if feature not in data
        ]

        if missing_features:
            return jsonify({
                "error": "Missing required features",
                "missing_features": missing_features
            }), 400

        # Create DataFrame
        input_data = pd.DataFrame([data])

        # -----------------------------
        # FEATURE ENGINEERING
        # Must match training
        # -----------------------------

        input_data["location_interaction"] = (
            input_data["latitude"]
            *
            input_data["longitude"]
        )

        # -----------------------------
        # SELECT EXPECTED FEATURES
        # -----------------------------

        model_features = REQUIRED_FEATURES + [
            "location_interaction"
        ]

        input_data = input_data[
            model_features
        ]

        # -----------------------------
        # MAKE PREDICTION
        # -----------------------------

        prediction = model.predict(
            input_data
        )

        predicted_price = max(
            0,
            float(prediction[0])
        )

        return jsonify({
            "predicted_price": round(
                predicted_price,
                2
            )
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# -----------------------------
# RUN APPLICATION
# -----------------------------

if __name__ == "__main__":

    app.run(
        debug=True,
        port=5000
    )