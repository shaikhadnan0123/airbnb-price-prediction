import matplotlib.pyplot as plt
import seaborn as sns


def plot_price_distribution(df):
    plt.figure(figsize=(8,5))
    sns.histplot(df["price"], bins=50)
    plt.title("Distribution of Airbnb Prices")
    plt.show()


def plot_room_type(df):
    plt.figure(figsize=(8,5))
    sns.boxplot(x="room_type", y="price", data=df)
    plt.title("Room Type vs Airbnb Price")
    plt.show()


if __name__ == "__main__":
    print("Visualization module loaded successfully!")