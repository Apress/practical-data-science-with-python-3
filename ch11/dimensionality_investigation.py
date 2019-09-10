from sklearn.datasets import fetch_kddcup99
from sklearn.manifold import TSNE
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def retrieve_column_desc():
    import requests

    r = requests.get('https://kdd.ics.uci.edu/databases/kddcup99/kddcup.names')

    column_desc = {}
    for row in r.text.split('\n')[1:]:
        if row.find(':') > 0:
            col_name, col_type = row[:-1].split(':')
            column_desc[col_name] = col_type.strip()
    return column_desc

def get_numeric_columns(column_desc):
    return [name for name in column_desc if column_desc[name] == 'continuous']    

column_desc = retrieve_column_desc()
numeric_columns = get_numeric_columns(column_desc)
print('Number of numeric columns:', len(numeric_columns))

X, _ = fetch_kddcup99(subset='SA', random_state=10, return_X_y=True)
X = pd.DataFrame(X, columns=column_desc.keys())
X[numeric_columns] = X[numeric_columns].apply(pd.to_numeric)

# We need to work on a small sample to get results in any reasonable time frame.
X = X.sample(frac=0.05, random_state=10)

m = TSNE(learning_rate=150, random_state=10)
X_tsne = m.fit_transform(X[numeric_columns])
print('First 10 rows of the TSNE reduced dataset:')
print(X_tsne[:10, :])

X['t-sne_1'] = X_tsne[:, 0]
X['t-sne_2'] = X_tsne[:, 1]

sns.set(rc={'figure.figsize': (10, 10)})
sns.scatterplot(x='t-sne_1', y='t-sne_2',
                hue='protocol_type',
                style='protocol_type',
                data=X[numeric_columns + ['protocol_type', 't-sne_1', 't-sne_2']])
plt.show()