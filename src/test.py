import pandas as pd


def check_csv(restaurant_list_filepath="../assets/restaurant_list.csv"):
    df = pd.read_csv(restaurant_list_filepath)
    print(df.head())


check_csv()
