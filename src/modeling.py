# Core libraries for file handling, model saving, and data preprocessing
import os
import json
import joblib
import pandas as pd
import numpy as np

# Scikit-learn components used for preprocessing, training, and evaluation
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline

# Import the custom function used to load and clean the raw Airbnb dataset
from data_cleaning import load_and_clean_data

# PREPARE DATA
def prepare_data(df):
# Work on a seperate copy so the original dataframe remains unchanged
    df = df.copy()
# Create a simple location feature using latitude and longitude This gives the model an additional way to capture location-related patterns
    df["location_interaction"] = (
        df["latitude"] * df["longitude"]
    )
# Sepearte the input features from the target variable we want to predict 
    X = df.drop("price", axis=1)
    y = df["price"]
# These features contain categories, so they need to be encoded before training 
    categorical_features = [
        "neighbourhood_group",
        "neighbourhood",
        "room_type"
    ]
# These numerical features can be pased directly to the model
    numerical_features = [
        "latitude",
        "longitude",
        "minimum_nights",
        "number_of_reviews",
        "reviews_per_month",
        "calculated_host_listings_count",
        "availability_365",
        "location_interaction"
    ]

# Preprocessing
# Apply different preprocessing steps to categorical and numerical features
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
# Convert categorical values into numerical columns unknown categories are ignored to avoid prediction-time errors
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False
                ),
                categorical_features
            ),
# Keep numerical features unchanged 
            (
                "numerical",
                "passthrough",
                numerical_features
            )
        ],
# Drop any column that are not included in the selected feature lists
        remainder="drop"
    )

# Model Pipeline 
# Combine preprocessing and model training into a single pipeline
# This ensures the same transformations are applied during training and prediction
    model_pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor
            ),
            (
                "model",
# Apply a log transformation to the target because Airbnb prices are skewed
# Predictions are automatically converted back to the original price scale
                TransformedTargetRegressor(
# Use Extra Trees to capture complex and non-linear relationships in the data
                    regressor=ExtraTreesRegressor(
                        n_estimators=50,    # Number of trees used in the ensemble
                        max_depth=16,       # Limit tree depth to control model complexity
                        min_samples_leaf=3, # Require at least 3 samples in each leaf
                        random_state=42,    # Keep results reproducible 
                        n_jobs=-1           # Use all available CPU cores for faster training
                    ),
                    func=np.log1p,
                    inverse_func=np.expm1
                )
            )
        ]
    )
# Reserve 20% of the data for evaluating how well the model performs on unseen listings
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42 # Keep the split consistent across different runs
    )
    return (
        X_train,
        X_test,
        y_train,
        y_test,
        model_pipeline
    )

def train_model(model_pipeline, X_train, y_train):
# Train the complete pipeline, including preprocessing and the Extra Trees model
    model_pipeline.fit(
        X_train,
        y_train
    )
# Return the trained pipeline so it can be used for evaluation and predictions
    return model_pipeline

def evaluate_model(model, X_test, y_test):
# Generate predictions for the unseen test data
    predictions = model.predict(X_test) 
# Measure the average absolute difference between actual and predicted prices
    mae = mean_absolute_error( # Penalize larger prediction errors more heavily
        y_test,
        predictions
    )
    mse = mean_squared_error(
        y_test,
        predictions
    )
    rmse = mse ** 0.5         # Convert MSE back to the original price scale for easier interpretation
    r2 = r2_score(
        y_test,
        predictions
    )
    print("\nModel Evaluation Results:")
    print(f"Mean Absolute Error (MAE): {mae:.2f}")
    print(f"Mean Squared Error (MSE): {mse:.2f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
    print(f"R² Score: {r2:.4f}")
# Store the evaluation results in a reusable format
    metrics = {
        "mae": round(float(mae), 2),
        "mse": round(float(mse), 2),
        "rmse": round(float(rmse), 2),
        "r2_score": round(float(r2), 4)
    }
    return metrics

def analyze_errors(model, X_test, y_test):
# Analyze individual predictions to understand where the model makes the largest mistakes
    predictions = model.predict(X_test)
# Create a results dataframe so actual values, predictions, and errors can be compared
    results = X_test.copy()
# Add the actual and predicted prices for comparison
    results["actual_price"] = y_test.values
    results["predicted_price"] = predictions
# Calculate the size of the prediction error without considering direction
    results["absolute_error"] = abs(
        results["actual_price"]
        - results["predicted_price"]
    )
# Calculate the error relative to the actual listing price
    results["percentage_error"] = (
        results["absolute_error"]
        / results["actual_price"]
    ) * 100
# Display the listings where the model made the largest prediction errors
    error_columns = [
        "actual_price",
        "predicted_price",
        "absolute_error",
        "percentage_error",
        "room_type",
        "neighbourhood_group",
        "neighbourhood"
    ]
    print("\nLargest Prediction Errors:\n")
    print(
        results[error_columns]
        .sort_values(
            by="absolute_error",
            ascending=False
        )
        .head(10)
        .to_string(index=False)
    )
    return results

# Check whether the model performs differently across budget, mid-range, and high-priced listings
def analyze_price_ranges(model, X_test, y_test):
    predictions = model.predict(X_test)
    results = pd.DataFrame({
        "actual_price": y_test.values,
        "predicted_price": predictions
    })
    results["absolute_error"] = abs(
        results["actual_price"]
        - results["predicted_price"]
    )
# Divide listings into price ranges based on the project's $500 price scope
    bins = [0, 100, 200, 500]
    labels = [
        "Budget ($0-$100)",
        "Mid-range ($100-$200)",
        "High ($200-$500)"
    ]
# Assign each listing to a price category based on its actual price
    results["price_range"] = pd.cut(
        results["actual_price"],
        bins=bins,
        labels=labels,
        include_lowest=True
    )
# Calculate prediction performance separately for each price range
    range_analysis = results.groupby(
        "price_range",
        observed=False
    ).agg(
        listings=("actual_price", "count"),
        average_actual_price=("actual_price", "mean"),
        average_predicted_price=("predicted_price", "mean"),
        mae=("absolute_error", "mean")
    )
    print("\nPrice Range Performance:\n")
    print(
        range_analysis.to_string()
    )
    return results, range_analysis

# Inspect unusually expensive listings before removing them from the project's price scope
def inspect_expensive_listings(df):
# Check how many listings exist above different high-price thresholds
    thresholds = [500, 1000, 2000]
    for threshold in thresholds:
# Select listings above the current price threshold
        subset = df[
            df["price"] > threshold
        ]
        print(
            f"\nListings priced above "
            f"${threshold}: {len(subset)}"
        )
# Skip further analysis if no listings exist in this price range
        if len(subset) == 0:
            continue
# Check which room types are most common among expensive listings
        print("\nRoom type breakdown:")
        print(
            subset["room_type"].value_counts()
        )
# Identify the neighbourhoods that appear most frequently in expensive listings
        print("\nTop neighbourhoods:")
        print(
            subset["neighbourhood"]
            .value_counts()
            .head(5)
        )
# Compare minimum stay requirements for high-priced listings
        print("\nMinimum nights stats:")
        print(
            subset["minimum_nights"]
            .describe()
        )
# Examine how availability differs among expensive listings
        print("\nAvailability stats:")
        print(
            subset["availability_365"]
            .describe()
        )

def show_feature_importance(model, top_n=20):
# Access the fitted preprocessing step from the trained pipeline
    preprocessor = model.named_steps[
        "preprocessor"
    ]
# Extract the trained Extra Trees regressor from TransformedTargetRegressor
    regressor = model.named_steps[
        "model"
    ].regressor_
# Get the final feature names after categorical encoding
    feature_names = (
        preprocessor.get_feature_names_out()
    )
# Retrieve the importance score assigned to each feature by the model
    importances = (
        regressor.feature_importances_
    )
# Combine feature names and importance scores into a readable dataframe
    importance_df = pd.DataFrame({
        "feature": feature_names,
        "importance": importances
    })
# Sort features so the most influential ones appear first
    importance_df = importance_df.sort_values(
        by="importance",
        ascending=False
    )
# Display only the top features for easier interpretation
    print("\nTop Feature Importances:\n")
    print(
        importance_df
        .head(top_n)
        .to_string(index=False)
    )
    return importance_df

def save_model(model, file_path):
# Create the target directory if it does not already exist
    os.makedirs(
        os.path.dirname(file_path),
        exist_ok=True
    )
# Save the complete trained pipeline so preprocessing and prediction stay together
    joblib.dump(
        model,
        file_path
    )
    print(
        f"\nModel saved successfully to:\n"
        f"{file_path}"
    )

def save_metrics(metrics, total_listings, file_path):
# Create the directory for the metrics file if needed
    os.makedirs(
        os.path.dirname(file_path),
        exist_ok=True
    )
# Store the model details and evaluation metrics in a JSON-friendly format
    metrics_data = {
        "model": "ExtraTreesRegressor",
        "total_listings": int(total_listings),
        "price_scope": "$10-$500",
        "mae": round(float(metrics["mae"]), 2),
        "mse": round(float(metrics["mse"]), 2),
        "rmse": round(float(metrics["rmse"]), 2),
        "r2_score": round(float(metrics["r2_score"]), 4)
    }
# Save the evaluation results so they can be accessed without retraining the model
    with open(file_path, "w") as file:
        json.dump(
            metrics_data,
            file,
            indent=4
        )

    print(
        f"\nMetrics saved successfully to:\n{file_path}"
    )

if __name__ == "__main__":
# Define the locations for the raw dataset, cleaned dataset, trained model, and metrics
    raw_data_path = (
        r"C:\Users\adnan\OneDrive\Desktop"
        r"\Airbnb_price_predction\data\raw"
        r"\AB_NYC_2019.csv"
    )
    cleaned_data_dir = (
        r"C:\Users\adnan\OneDrive\Desktop"
        r"\Airbnb_price_predction\data\cleaned"
    )
    model_save_path = (
        r"C:\Users\adnan\OneDrive\Desktop"
        r"\Airbnb_price_predction\models"
        r"\extra_trees_model_compressed.joblib"
    )
    metrics_file_path = (
        r"C:\Users\adnan\OneDrive\Desktop"
        r"\Airbnb_price_predction\models"
        r"\model_metrics.json"
    )

    print("Loading and cleaning data...")
# Load the raw Airbnb dataset and apply the cleaning steps defined in data_cleaning.py
    df = load_and_clean_data(
        raw_data_path
    )
# Remove listings with invalid or non-positive prices
    df = df[
        df["price"] > 0
    ].copy()
# Review the original price distribution before applying the project's price limit
    print("\nOriginal price statistics:")
    print(
        df["price"].describe()
    )
    print("\nInspecting expensive listings...")
# Investigate high-priced listings to understand potential outliers
    inspect_expensive_listings(df)
    print(
        "\nApplying project scope..."
    )
    print(
        "Keeping typical NYC Airbnb "
        "listings priced at $500 or below."
    )
# Limit the dataset to the typical Airbnb listings targeted by this project
# Extremely expensive listings are excluded to keep predictions focused on the $10-$500 range
    df = df[
        df["price"] <= 500
    ].copy()
    print("\nDataset after applying project scope:")
    print(
        f"Number of listings: {len(df)}"
    )
    print(
        f"Minimum price: ${df['price'].min():.2f}"
    )
    print(
        f"Maximum price: ${df['price'].max():.2f}"
    )
    print("\nScoped price statistics:")

    print(
        df["price"].describe()
    )
# APPLY PROJECT SCOPE
    os.makedirs(
        cleaned_data_dir,
        exist_ok=True
    )
    cleaned_file_path = os.path.join(
        cleaned_data_dir,
        "cleaned_airbnb_typical.csv"
    )
    df.to_csv(
        cleaned_file_path,
        index=False
    )
    print(
        "\nScoped dataset saved successfully to:"
    )
    print(
        cleaned_file_path
    )
# Prepare features, preprocessing steps, and the train-test split
    print(
        "\nPreparing features and "
        "splitting data..."
    )
    (
        X_train,
        X_test,
        y_train,
        y_test,
        model_pipeline
    ) = prepare_data(df)
# Train the complete machine learning pipeline
    print(
        "\nTraining the Extra Trees model..."
    )
    model = train_model(
        model_pipeline,
        X_train,
        y_train
    )
    print(
        "\nEvaluating the model..."
    )
    metrics = evaluate_model(
        model,
        X_test,
        y_test
    )
# Examine the largest prediction mistakes to identify where the model struggles
    print(
        "\nAnalyzing prediction errors..."
    )
    error_results = analyze_errors(
        model,
        X_test,
        y_test
    )
    print(
        "\nAnalyzing performance "
        "by price range..."
    )
# Compare model performance across different Airbnb price segments
    price_results, range_analysis = (
        analyze_price_ranges(
            model,
            X_test,
            y_test
        )
    )
# Identify which input features have the strongest influence on the model's predictions
    print(
        "\nAnalyzing feature importance..."
    )
    feature_importance = show_feature_importance(
        model,
        top_n=20
    )
    print(
        "\nSaving the trained model..."
    )
    save_model(model, model_save_path)
    print(
        f"\nCompressed model saved successfully to:\n"
        f"{model_save_path}"
    )
# Check the saved model size to make sure it is practical for deployment
    model_size_mb = os.path.getsize(model_save_path) / (1024 * 1024)

    print(
        f"Model size: {model_size_mb:.2f} MB"
    )
# Print a final summary of the dataset scope and model performance
    print("\n" + "=" * 50)
    print("PROJECT SUMMARY")
    print("=" * 50)
    print(f"Total listings used: {len(df)}")
    print(
        f"Project price scope: "
        f"${df['price'].min():.2f} to "
        f"${df['price'].max():.2f}"
    )
    print(f"MAE: ${metrics['mae']:.2f}")
    print(f"MSE: {metrics['mse']:.2f}")
    print(f"RMSE: ${metrics['rmse']:.2f}")
    print(f"R² Score: {metrics['r2_score']:.4f}")
    print("=" * 50)