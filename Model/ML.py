from classification import Model
import torch
import os
import random
import pandas as pd
from pandas import DataFrame

import torch
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import Ridge
from sklearn.metrics import make_scorer
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--model_name', type=str, default='ridge')

arg = parser.parse_args()


def make_df_description(df: DataFrame, path_tensor_description: str):
    feature = torch.load(path_tensor_description)
    feature = feature.cpu().numpy()
    print(feature.shape)
    feature_columns = [f'feature{i}' for i in range(feature.shape[1])]
    df_feature = pd.DataFrame(feature, columns=feature_columns)
    return pd.concat((df, df_feature), axis=1)


data_train = pd.read_csv('../Preprocess/train_data.csv')
data_test = pd.read_csv('../Preprocess/test_data.csv')

data_train_des = make_df_description(data_train, '../Description/train_des.pth')
data_test_des = make_df_description(data_test, '../Description/test_des.pth')

if __name__=='__main__':

    if arg.model_name == 'ridge':
        ml_algorithm = Pipeline(
            steps=[
                ("scaler", MinMaxScaler()),
                ('model', Ridge(alpha=0.2))
            ])

    elif arg.model_name == 'knn':
        ml_algorithm = Pipeline(steps=[
            ("scaler", MinMaxScaler()),
            ('model', KNeighborsRegressor(n_neighbors=5))
        ])

    elif arg.model_name == 'decision_tree':
        ml_algorithm = Pipeline(steps=[
            ("scaler", MinMaxScaler()),
            ('model', DecisionTreeRegressor(random_state=0))
        ])

    model = Model(ml_algorithm, data_train, data_test)
    model1 = Model(ml_algorithm, data_train_des, data_test_des)
    mse_loss, r2Score = model.build()
    print(f"Mean squared score: {mse_loss}\nR2 score:{r2Score}")
    mse_loss1, r2Score1 = model1.build()
    print(f"Mean squared score: {mse_loss1}\nR2 score:{r2Score1}")


