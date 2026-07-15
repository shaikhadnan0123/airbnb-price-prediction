import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


def prepare_data(df):
    X = df.drop("price", axis=1)
    y = df["price"]

    X = pd.get_dummies(
        X,
        columns=[
            "neighbourhood_group",
            "neighbourhood",
            "room_type"
        ],
        drop_first=True
    )

    return train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )


def train_model(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model


if __name__ == "__main__":
    print("Modeling module loaded successfully!")