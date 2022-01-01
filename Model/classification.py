from pandas import DataFrame
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
import pickle


class Model:
    def __init__(self, model, data_train: DataFrame, data_test: DataFrame):
        self.model = model
        self.list_feature = ['origin', 'status', 'car_mileage', 'car_color', 'car_seats', 'gear', 'car_year',
                             'car_price', 'style', 'model', 'fuel', 'brand_name', 'region_name', 'month', 'year']
        self.data_train = self.make_df(data_train)
        self.data_test = self.make_df(data_test)
        self.map_features = {}
        self.convert_feature()
        self.x_train, self.y_train = self.get_data(self.data_train)
        self.x_test, self.y_test = self.get_data(self.data_test)

    def make_df(self, df: DataFrame):
        df = df[self.list_feature]
        df.car_price = np.log(df.car_price / 1e6)
        df = df[df.car_mileage < 1e6]
        return df.reset_index(drop=True)

    def convert_feature(self):
        for column_name in self.list_feature:
            if self.data_train[column_name].dtype == 'object':
                list_categorical = set(self.data_train[column_name])
                map_f = {category: i for i, category in enumerate(list_categorical)}
                self.data_train[column_name] = self.data_train[column_name].map(map_f)
                self.data_test[column_name] = self.data_test[column_name].map(map_f)

                if self.data_test[column_name].isnull().values.any():
                    mode_value = self.data_train[column_name].mode().values[0]
                    self.data_test[column_name].fillna(mode_value, inplace=True)

                self.map_features[column_name] = map_f

    def get_data(self, df: DataFrame):
        y = df.car_price.values
        df_temp = df.drop(['car_price'], axis=1)
        return df_temp.values, y

    def save_model(self, model_name: str):
        with open('map_features.pkl', 'wb') as file:
            pickle.dump(self.map_features, file, protocol=pickle.HIGHEST_PROTOCOL)

        print("Save map feature done")

        with open(model_name, 'wb') as file:
            pickle.dump(self.model, file, pickle.HIGHEST_PROTOCOL)

        print("Save model done")

    def build(self):
        self.model.fit(self.x_train, self.y_train)
        predict = self.model.predict(self.x_test)
        mse_score = mean_squared_error(self.y_test, predict)
        r2 = r2_score(self.y_test, predict)
        return mse_score, r2
