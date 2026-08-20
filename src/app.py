from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import os

# Initialize the Flask application that will serve the prediction API
app = Flask(__name__)

# Allow the frontend to communicate with this API from a different origin
CORS(app)

# Get the root directory of the project based on the current file location
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

# Build the path to the trained machine learning model
MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "extra_trees_model_compressed.joblib"
)

# Load the complete trained pipeline, including preprocessing and the Extra Trees model
model = joblib.load(MODEL_PATH)

# Confirm that the model was loaded successfully when the API starts
print("Model loaded successfully.")
print(f"Model path: {MODEL_PATH}")

# These are the features the API expects from the frontend for every prediction
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

# Return a simple response to confirm that the API is running correctly
@app.route("/")
def home():
    return jsonify({
        "status": "healthy",
        "message": "Airbnb Price Prediction API is running",
        "model": "Extra Trees Regressor"
    })

# Receive Airbnb listing details and return the predicted nightly price
@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get the Airbnb listing details sent by the frontend as JSON
        data = request.get_json()

        # Stop the request early if no input data was provided
        if not data:
            return jsonify({
                "error": "No input data provided"
            }), 400

        # Check whether all features required by the trained model are present
        missing_features = [
            feature
            for feature in REQUIRED_FEATURES
            if feature not in data
        ]

        # Return a clear error message if any required feature is missing
        if missing_features:
            return jsonify({
                "error": "Missing required features",
                "missing_features": missing_features
            }), 400

        # Convert the incoming JSON data into a DataFrame for the ML pipeline
        input_data = pd.DataFrame([data])

        # Recreate the same engineered feature used during model training
        input_data["location_interaction"] = (
            input_data["latitude"]
            * input_data["longitude"]
        )

        # Define the complete set of features expected by the trained model
        model_features = REQUIRED_FEATURES + [
            "location_interaction"
        ]

        # Keep only the required features in the expected column order
        input_data = input_data[model_features]

        # Pass the prepared listing data through the trained ML pipeline
        prediction = model.predict(input_data)

        # Convert the prediction to a float and prevent negative prices
        predicted_price = max(
            0,
            float(prediction[0])
        )

        # Return the predicted nightly price as a JSON response
        return jsonify({
            "predicted_price": round(
                predicted_price,
                2
            )
        })

    # Return a server error if something unexpected happens during prediction
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

# Run the API server only when this file is executed directly
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )