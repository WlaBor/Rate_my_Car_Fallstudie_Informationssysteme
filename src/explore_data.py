import pandas as pd

path = r"C:\Users\wladi\dev\fallstudie_informationssysteme\src\data\continuous_factory_process.csv"

dataframe = pd.read_csv(path)

dtypes = dataframe.dtypes

summary = dataframe.describe()
