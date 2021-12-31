from xgboost.sklearn import XGBRegressor
import pickle
import argparse
import pandas as pd
import math

def predict(model_path, input):
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    return [math.exp(item) for item in model.predict(input)]

def process_dataframe(dataframe):
  dataframe["car_name"] = dataframe["brand_name"] + pd.Series([" "]*dataframe.shape[0]) + dataframe["model"]
#   target = dataframe.car_price.apply(lambda x: math.log(x)).values.tolist()
  country = pd.get_dummies(dataframe.origin, prefix="country")
  status = dataframe["status"].apply(lambda x: 1 if x=="Đã sử dụng" else 0)
  color = pd.get_dummies(dataframe.car_color, prefix="color")
  gear = pd.get_dummies(dataframe.gear, prefix="gear")
  style = pd.get_dummies(dataframe.style, prefix="style")
  region = pd.get_dummies(dataframe.region_name, prefix="region")
  name = pd.get_dummies(dataframe.car_name, prefix="name")
  status = pd.DataFrame({"status": status})
  features = pd.concat([country, status, color, gear, style, region, name], axis=1)
  features['car_mileage'] = dataframe.car_mileage.apply(lambda x: float(x)/1e3)
  features['car_seats'] = dataframe.car_seats.apply(lambda x: int(str(x).split('.')[0]))
  features['car_year'] = dataframe.car_year.apply(lambda x: float(str(x).split('.')[0]) / 2000)
  return features
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", required=True, type=str,
                        help="Model path for prediction")
    parser.add_argument("--input_file", required=True, type=str,
                        help="Input file contain features in csv format.")
    parser.add_argument("--output_file", default="output.txt", type=str,
                        help="Output file for saving result.")
    args = parser.parse_args()
    input = pd.read_csv(args.input_file)
    features = process_dataframe(input).to_numpy()
    prediction = predict(args.model_path, features)
    with open(args.output_file, "w+") as f:
        for item in prediction:
            f.write(str(item) + "\n")
