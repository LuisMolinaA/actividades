import pandas as pd

data = pd.read_csv('D:/dev/MINERIA/act1/data/3_peliculas.csv')
print(data.head())
print(data.describe)
umbral = len(data) * 0.75

data['YEAR'] = data['YEAR'].str.replace('(', '').str.replace(')', '').str.replace(' ', '')
data['YEAR'] = data['YEAR'].str.extract(r'(\d{4})')


data['VOTES'] = data['VOTES'].fillna(method='ffill')
data['VOTES'] = data['VOTES'].str.replace(',', '')
data['VOTES'] = pd.to_numeric(data['VOTES'], errors='coerce')


data.loc[data['STARS'].str.contains('Director:'), 'DIRECTOR'] = data['STARS'].str.extract(r'Director:\s(.*?)\s\|', expand=False)
data['STARS'] = data['STARS'].str.replace('\n', ' ')
data.loc[data['STARS'].str.contains('Stars:'), 'STARS'] = data['STARS'].str.extract(r'Stars:\s(.*)', expand=False)

data = data.dropna(axis=1, thresh=umbral)


print(data.head())

data.to_csv('try.csv', index=False)
