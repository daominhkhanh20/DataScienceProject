from pandas import DataFrame
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score, make_scorer
import pickle
import numpy as np
from sklearn.model_selection import RandomizedSearchCV
import os


def score_evaluate_function(actual, prediction):
    return mean_squared_error(actual, prediction)


grid_scorer = make_scorer(score_evaluate_function, greater_is_better=True)


class Model:
    def __init__(self, model,
                 data_train: DataFrame = None,
                 data_test: DataFrame = None,
                 parameters: list = None,
                 model_name: str = None,
                 is_train_time: bool = True,
                 path_feature_map: str = None
                 ):
        self.model = model
        self.list_feature = ['origin', 'status', 'car_mileage', 'car_color', 'car_seats', 'gear', 'car_year',
                             'car_price', 'style', 'model', 'fuel', 'brand_name', 'region_name', 'month', 'year']
        if is_train_time:
            self.data_train = self.make_df(data_train)
            self.data_test = self.make_df(data_test)
            self.map_features = {}
            self.convert_feature()
            self.model_name = model_name
            self.parameters = parameters
            self.x_train, self.y_train = self.get_data(self.data_train)
            self.x_test, self.y_test = self.get_data(self.data_test)
        else:
            self.list_feature.remove('car_price')
            with open(path_feature_map, 'rb') as file:
                self.map_features = pickle.load(file)

    def grid_search(self):
        grid_search = RandomizedSearchCV(self.model, param_distributions=self.parameters, scoring=grid_scorer,
                                         cv=5)
        grid_search.fit(self.x_train, self.y_train)
        print(grid_search.best_params_)

    def make_df(self, df: DataFrame):
        df = df[self.list_feature]
        df.car_price = np.log(df.car_price / 1e6)
        df = df[df.car_mileage < 1e6]
        return df.reset_index(drop=True)

    def convert_feature(self):
        self.map_features['mode'] = []
        for column_name in self.list_feature:
            if self.data_train[column_name].dtype == 'object':
                list_categorical = set(self.data_train[column_name])
                map_f = {category: i for i, category in enumerate(list_categorical)}
                self.data_train[column_name] = self.data_train[column_name].map(map_f)
                self.data_test[column_name] = self.data_test[column_name].map(map_f)
                mode_value = self.data_train[column_name].mode().values[0]
                self.map_features['mode'].append(mode_value)
                if self.data_test[column_name].isnull().values.any():
                    self.data_test[column_name].fillna(mode_value, inplace=True)

                self.map_features[column_name] = map_f

    def get_data(self, df: DataFrame):
        y = df.car_price.values
        df_temp = df.drop(['car_price'], axis=1)
        return df_temp.values, y

    def predict_sample(self, df: DataFrame):
        df = df[self.list_feature]
        categorical_name = list(self.map_features.keys())
        categorical_name.remove('mode')
        for idx, column_name in enumerate(categorical_name):
            df[column_name] = df[column_name].map(self.map_features[column_name])
            if df[column_name].isnull().values.any():
                df[column_name].fillna(self.map_features['mode'][idx], inplace=True)
        x = df.values
        predict_price = self.model.predict(x)
        return np.exp(predict_price) * 1e6

    def save_model(self, model_name: str, map_feature_name: str):
        path = f'Pickle/{self.model_name}/'
        if os.path.exists(path) is False:
            os.makedirs(path, exist_ok=True)

        with open(path + map_feature_name, 'wb') as file:
            pickle.dump(self.map_features, file, protocol=pickle.HIGHEST_PROTOCOL)

        print("Save map feature done")

        with open(path + model_name, 'wb') as file:
            pickle.dump(self.model, file, pickle.HIGHEST_PROTOCOL)

        print("Save model done")

    def build(self):
        self.model.fit(self.x_train, self.y_train)
        predict = self.model.predict(self.x_test)
        mse_score = mean_squared_error(self.y_test, predict)
        r2 = r2_score(self.y_test, predict)
        return mse_score, r2
