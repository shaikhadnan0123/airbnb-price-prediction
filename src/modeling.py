import os
import json
import joblib
import pandas as pd
import numpy as np

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

from data_cleaning import load_and_clean_data


# =================================
# PREPARE DATA
# =================================

def prepare_data(df):

    df = df.copy()

    # -----------------------------
    # FEATURE ENGINEERING
    # -----------------------------

    # Interaction between latitude and longitude
    df["location_interaction"] = (
        df["latitude"] * df["longitude"]
    )

    # -----------------------------
    # FEATURES AND TARGET
    # -----------------------------

    X = df.drop("price", axis=1)
    y = df["price"]

    # -----------------------------
    # CATEGORICAL FEATURES
    # -----------------------------

    categorical_features = [
        "neighbourhood_group",
        "neighbourhood",
        "room_type"
    ]

    # -----------------------------
    # NUMERICAL FEATURES
    # -----------------------------

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

    # -----------------------------
    # PREPROCESSING
    # -----------------------------

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False
                ),
                categorical_features
            ),
            (
                "numerical",
                "passthrough",
                numerical_features
            )
        ],
        remainder="drop"
    )

    # -----------------------------
    # MODEL PIPELINE
    # -----------------------------

    model_pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor
            ),
            (
                "model",
                TransformedTargetRegressor(
                    regressor=ExtraTreesRegressor(
                        n_estimators=50,
                        max_depth=16,
                        min_samples_leaf=3,
                        random_state=42,
                        n_jobs=-1
                    ),
                    func=np.log1p,
                    inverse_func=np.expm1
                )
            )
        ]
    )

    # -----------------------------
    # TRAIN / TEST SPLIT
    # -----------------------------

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    return (
        X_train,
        X_test,
        y_train,
        y_test,
        model_pipeline
    )


# =================================
# TRAIN MODEL
# =================================

def train_model(model_pipeline, X_train, y_train):

    model_pipeline.fit(
        X_train,
        y_train
    )

    return model_pipeline


# =================================
# EVALUATE MODEL
# =================================

def evaluate_model(model, X_test, y_test):

    predictions = model.predict(X_test)

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    mse = mean_squared_error(
        y_test,
        predictions
    )

    rmse = mse ** 0.5

    r2 = r2_score(
        y_test,
        predictions
    )

    print("\nModel Evaluation Results:")
    print(f"Mean Absolute Error (MAE): {mae:.2f}")
    print(f"Mean Squared Error (MSE): {mse:.2f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
    print(f"R² Score: {r2:.4f}")

    metrics = {
        "mae": round(float(mae), 2),
        "mse": round(float(mse), 2),
        "rmse": round(float(rmse), 2),
        "r2_score": round(float(r2), 4)
    }

    return metrics


# =================================
# ANALYZE PREDICTION ERRORS
# =================================

def analyze_errors(model, X_test, y_test):

    predictions = model.predict(X_test)

    results = X_test.copy()

    results["actual_price"] = y_test.values
    results["predicted_price"] = predictions

    results["absolute_error"] = abs(
        results["actual_price"]
        - results["predicted_price"]
    )

    results["percentage_error"] = (
        results["absolute_error"]
        / results["actual_price"]
    ) * 100

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


# =================================
# ANALYZE PERFORMANCE BY PRICE RANGE
# =================================

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

    # Since our project focuses on listings <= $500,
    # these ranges represent the complete project scope.
    bins = [0, 100, 200, 500]

    labels = [
        "Budget ($0-$100)",
        "Mid-range ($100-$200)",
        "High ($200-$500)"
    ]

    results["price_range"] = pd.cut(
        results["actual_price"],
        bins=bins,
        labels=labels,
        include_lowest=True
    )

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


# =================================
# INSPECT EXPENSIVE LISTINGS
# =================================

def inspect_expensive_listings(df):

    thresholds = [500, 1000, 2000]

    for threshold in thresholds:

        subset = df[
            df["price"] > threshold
        ]

        print(
            f"\nListings priced above "
            f"${threshold}: {len(subset)}"
        )

        if len(subset) == 0:
            continue

        print("\nRoom type breakdown:")
        print(
            subset["room_type"].value_counts()
        )

        print("\nTop neighbourhoods:")
        print(
            subset["neighbourhood"]
            .value_counts()
            .head(5)
        )

        print("\nMinimum nights stats:")
        print(
            subset["minimum_nights"]
            .describe()
        )

        print("\nAvailability stats:")
        print(
            subset["availability_365"]
            .describe()
        )


# =================================
# FEATURE IMPORTANCE
# =================================

def show_feature_importance(model, top_n=20):

    # Get fitted preprocessor
    preprocessor = model.named_steps[
        "preprocessor"
    ]

    # Get fitted Extra Trees model
    # inside TransformedTargetRegressor
    regressor = model.named_steps[
        "model"
    ].regressor_

    # Get feature names after preprocessing
    feature_names = (
        preprocessor.get_feature_names_out()
    )

    # Get importance values
    importances = (
        regressor.feature_importances_
    )

    # Create DataFrame
    importance_df = pd.DataFrame({
        "feature": feature_names,
        "importance": importances
    })

    # Sort highest importance first
    importance_df = importance_df.sort_values(
        by="importance",
        ascending=False
    )

    print("\nTop Feature Importances:\n")

    print(
        importance_df
        .head(top_n)
        .to_string(index=False)
    )

    return importance_df


# =================================
# SAVE MODEL
# =================================

def save_model(model, file_path):

    os.makedirs(
        os.path.dirname(file_path),
        exist_ok=True
    )

    joblib.dump(
        model,
        file_path
    )

    print(
        f"\nModel saved successfully to:\n"
        f"{file_path}"
    )


def save_metrics(metrics, total_listings, file_path):

    os.makedirs(
        os.path.dirname(file_path),
        exist_ok=True
    )

    metrics_data = {
        "model": "ExtraTreesRegressor",
        "total_listings": int(total_listings),
        "price_scope": "$10-$500",
        "mae": round(float(metrics["mae"]), 2),
        "mse": round(float(metrics["mse"]), 2),
        "rmse": round(float(metrics["rmse"]), 2),
        "r2_score": round(float(metrics["r2_score"]), 4)
    }

    with open(file_path, "w") as file:
        json.dump(
            metrics_data,
            file,
            indent=4
        )

    print(
        f"\nMetrics saved successfully to:\n{file_path}"
    )
# =================================
# MAIN PROGRAM
# =================================

if __name__ == "__main__":

    # -----------------------------
    # FILE PATHS
    # -----------------------------

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

    # -----------------------------
    # LOAD AND CLEAN DATA
    # -----------------------------

    print("Loading and cleaning data...")

    df = load_and_clean_data(
        raw_data_path
    )

    # Remove invalid prices
    df = df[
        df["price"] > 0
    ].copy()

    # -----------------------------
    # ORIGINAL DATA ANALYSIS
    # -----------------------------

    print("\nOriginal price statistics:")

    print(
        df["price"].describe()
    )

    print("\nInspecting expensive listings...")

    # Important:
    # We inspect the full valid dataset BEFORE
    # applying the project scope.
    inspect_expensive_listings(df)

    # -----------------------------
    # APPLY PROJECT SCOPE
    # -----------------------------

    print(
        "\nApplying project scope..."
    )

    print(
        "Keeping typical NYC Airbnb "
        "listings priced at $500 or below."
    )

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

    # -----------------------------
    # SAVE SCOPED DATASET
    # -----------------------------

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

    # -----------------------------
    # PREPARE DATA
    # -----------------------------

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

    # -----------------------------
    # TRAIN MODEL
    # -----------------------------

    print(
        "\nTraining the Extra Trees model..."
    )

    model = train_model(
        model_pipeline,
        X_train,
        y_train
    )

    # -----------------------------
    # EVALUATE MODEL
    # -----------------------------

    print(
        "\nEvaluating the model..."
    )

    metrics = evaluate_model(
        model,
        X_test,
        y_test
    )

    # -----------------------------
    # ERROR ANALYSIS
    # -----------------------------

    print(
        "\nAnalyzing prediction errors..."
    )

    error_results = analyze_errors(
        model,
        X_test,
        y_test
    )

    # -----------------------------
    # PRICE RANGE ANALYSIS
    # -----------------------------

    print(
        "\nAnalyzing performance "
        "by price range..."
    )

    price_results, range_analysis = (
        analyze_price_ranges(
            model,
            X_test,
            y_test
        )
    )

    # -----------------------------
    # FEATURE IMPORTANCE
    # -----------------------------

    print(
        "\nAnalyzing feature importance..."
    )

    feature_importance = show_feature_importance(
        model,
        top_n=20
    )

        # -----------------------------
    # SAVE MODEL
    # -----------------------------

    print(
        "\nSaving the trained model..."
    )

    save_model(model, model_save_path)

    print(
        f"\nCompressed model saved successfully to:\n"
        f"{model_save_path}"
    )

    # Display model file size
    model_size_mb = os.path.getsize(model_save_path) / (1024 * 1024)

    print(
        f"Model size: {model_size_mb:.2f} MB"
    )

    # -----------------------------
    # FINAL SUMMARY
    # -----------------------------

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