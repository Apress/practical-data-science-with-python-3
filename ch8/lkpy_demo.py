from itertools import tee

import pandas as pd

from lenskit import batch
from lenskit import crossfold as xf
from lenskit.algorithms import funksvd, item_knn, user_knn
from lenskit.metrics import topn

ratings = pd.read_csv('data/ratings.csv')
ratings.rename({'userId': 'user', 'movieId': 'item'}, axis = 'columns', inplace = True)
print(ratings.head())

xf_dataset_batch, xf_dataset_test = tee(xf.partition_users(ratings[['user', 'item', 'rating']], 5, xf.SampleFrac(0.2)))
truth = pd.concat([test for _, test in xf_dataset_test], ignore_index = True)

runner = batch.MultiEval('result', False, nprocs = 4)
runner.add_algorithms(
    [item_knn.ItemItem(10), item_knn.ItemItem(20), item_knn.ItemItem(30)],
    False,
    ['nnbrs']
)
runner.add_algorithms(
    [user_knn.UserUser(10), user_knn.UserUser(20), user_knn.UserUser(30)],
    True,
    ['nnbrs']
)
runner.add_algorithms(
    [funksvd.FunkSVD(40, damping = 0), funksvd.FunkSVD(50, damping = 5), funksvd.FunkSVD(60, damping = 10)],
    False,
    ['features', 'damping']
)
runner.add_datasets(xf_dataset_batch)
runner.run()

runs = pd.read_parquet('result/runs.parquet', 
                       columns = ('AlgoClass','RunId','damping','features','nnbrs'))
runs.rename({'AlgoClass': 'Algorithm'}, axis = 'columns', inplace = True)

def extract_config(x):
    from math import isnan
    
    damping, features, nnbrs = x
    result = ''
    if not isnan(damping):
        result = "damping=%.2f " % damping
    if not isnan(features):
        result += "features=%.2f " % features
    if not isnan(nnbrs):
        result += "nnbrs=%.2f" % nnbrs    
    return result.strip()

runs['Configuration'] = runs[['damping','features','nnbrs']].apply(extract_config, axis = 1)
runs.drop(columns = ['damping','features','nnbrs'], inplace = True)

recs = pd.read_parquet('result/recommendations.parquet')
recs = recs.merge(runs, on = 'RunId')
recs.drop(columns = ['RunId'], inplace = True)
print(recs.head(10))

user_dcg = recs.groupby(['Algorithm', 'Configuration', 'user']).rating.apply(topn.dcg)
user_dcg = user_dcg.reset_index(name='DCG')
ideal_dcg = topn.compute_ideal_dcgs(truth)
user_ndcg = pd.merge(user_dcg, ideal_dcg)
user_ndcg['nDCG'] = user_ndcg.DCG / user_ndcg.ideal_dcg
user_ndcg = user_ndcg.groupby(['Algorithm', 'Configuration']).nDCG.mean()

%matplotlib inline
user_ndcg.plot.bar()