import pandas as pd

data = pd.read_csv('D:/dev/MINERIA/act2/data/1_trabajos.csv')
print(data.head())
print(data.describe)
umbral = len(data) * 0.75

data = data.dropna(axis=1, thresh=umbral)


print(data.head())

data.to_csv('try.csv', index=False)
