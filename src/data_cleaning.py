import pandas as pd


def load_and_clean_data(file_path):
    df = pd.read_csv(file_path)

    df = df.drop(
        columns=[
            "id",
            "host_id",
            "host_name",
            "name",
            "last_review"
        ]
    )

    df["reviews_per_month"] = df["reviews_per_month"].fillna(0)

    return df


if __name__ == "__main__":
    file_path = r"C:\Users\adnan\OneDrive\Desktop\Airbnb_price_predction\data\raw\AB_NYC_2019.csv"

    df = load_and_clean_data(file_path)

    print(df.head())
    print(df.shape)