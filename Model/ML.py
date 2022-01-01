from classification import Model
import torch
import pandas as pd
from pandas import DataFrame

import torch
from sklearn.linear_model import Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
import argparse
import pickle
import warnings
warnings.filterwarnings("ignore")


parser = argparse.ArgumentParser()
parser.add_argument('--model_name', type=str, default='ridge')
parser.add_argument('--is_train_time', default=True, type=lambda x: str(x).lower() == 'true')
parser.add_argument('--path_model', type=str, default='decision_tree1.pkl', help='Path to pretrained model')
parser.add_argument('--path_map_feature', type=str, default='map_decision_tree1.pkl')
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

if __name__ == '__main__':
    if arg.is_train_time:
        if arg.model_name == 'ridge':
            ml_algorithm = Pipeline(
                steps=[
                    ("scaler", MinMaxScaler()),
                    ('model', Ridge(alpha=0.2))
                ])
            parameters = [ {'model__alpha': [0,0.2,0.4,0.8] } ]

        elif arg.model_name == 'knn':
            ml_algorithm = Pipeline(steps=[
                ("scaler", MinMaxScaler()),
                ('model', KNeighborsRegressor(n_neighbors=5))
            ])
            parameters = [{'model__n_neighbors': [5, 10, 20, 30, 40]} ]

        elif arg.model_name == 'decision_tree':
            ml_algorithm = Pipeline(steps=[
                ("scaler", MinMaxScaler()),
                ('model', DecisionTreeRegressor(random_state=0))
            ])
            parameters = [{
                'model__max_depth': [10, 20, 30, 50],
                'model__min_samples_split': [1, 3, 10],
                'model__min_samples_leaf': [2, 5, 10],
                'model__max_features': ['auto', 'sqrt']
            }]

        model = Model(ml_algorithm, data_train, data_test, parameters, arg.model_name)
        mse_loss, r2Score = model.build()
        model.grid_search()
        model.save_model(f'{arg.model_name}.pkl', f'map_{arg.model_name}.pkl')
        print(f"Mean squared score: {mse_loss}\nR2 score:{r2Score}\n\n\n")

        model1 = Model(ml_algorithm, data_train_des, data_test_des, parameters, arg.model_name)
        mse_loss1, r2Score1 = model1.build()
        model1.grid_search()
        model1.save_model(f'{arg.model_name}_des.pkl', f'map_{arg.model_name}_des.pkl')
        print(f"Mean squared score: {mse_loss1}\nR2 score:{r2Score1}")

    else:
        with open(arg.path_model, 'rb') as file:
            ml_algorithm = pickle.load(file)

        model = Model(ml_algorithm, is_train_time=False, path_feature_map=arg.path_map_feature)
        predict = model.predict_sample(data_test.head(1))
        print(predict)
