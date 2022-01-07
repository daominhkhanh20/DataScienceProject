import pandas as pd

def process_dataframe(dataframe):
  # feature
  #1
  # dataframe["car_name"] = dataframe["brand_name"] + pd.Series([" "]*data.shape[0]) + data["model"]
  # name = pd.get_dummies(dataframe.car_name, prefix="name")
  brand_name = pd.get_dummies(dataframe.brand_name, prefix="brand_name")
  model = pd.get_dummies(dataframe.model, prefix="model")
  #2
  country = pd.get_dummies(dataframe.origin, prefix="country")
  #3
  color = pd.get_dummies(dataframe.car_color, prefix="color")
  #4
  gear = pd.get_dummies(dataframe.gear, prefix="gear")
  #5
  style = pd.get_dummies(dataframe["style"], prefix="style")
  #6
  region = pd.get_dummies(dataframe.region_name, prefix="region")
  #7
  fuel = pd.get_dummies(dataframe.fuel, prefix='fuel')
  #8
  status = dataframe["status"].apply(lambda x: 1 if x=="Đã sử dụng" else 0)
  status = pd.DataFrame({"status": status})
  #ensemble
  features = pd.concat([country, status, color, gear, style, region, brand_name, model, fuel], axis=1)
  #9
  features['car_mileage'] = dataframe.car_mileage.apply(lambda x: float(x)/1e3)
  #10
  features['car_seats'] = dataframe.car_seats.apply(lambda x: int(str(x).split('.')[0]))
  #11
  features['car_year'] = dataframe.car_year.apply(lambda x: float(str(x).split('.')[0]) / 2000)
  features["name_Unknown"] = pd.Series([0]*dataframe.shape[0])
  return features