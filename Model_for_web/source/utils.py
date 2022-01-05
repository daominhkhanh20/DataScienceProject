import pandas as pd

def process_dataframe(dataframe):
  dataframe["car_name"] = dataframe["brand_name"] + pd.Series([" "]*dataframe.shape[0]) + dataframe["model"]
#   target = dataframe.car_price.apply(lambda x: math.log(x)).values.tolist()
  country = pd.get_dummies(dataframe.origin, prefix="country")
  status = dataframe["status"].apply(lambda x: 1 if x=="Đã sử dụng" else 0)
  color = pd.get_dummies(dataframe.car_color, prefix="color")
  gear = pd.get_dummies(dataframe.gear, prefix="gear")
  style = pd.get_dummies(dataframe["style"], prefix="style")
  region = pd.get_dummies(dataframe.region_name, prefix="region")
  name = pd.get_dummies(dataframe.car_name, prefix="name")
  fuel = pd.get_dummies(dataframe.fuel, prefix='fuel')
  status = pd.DataFrame({"status": status})
  features = pd.concat([country, status, color, gear, style, region, name, fuel], axis=1)
  features['car_mileage'] = dataframe.car_mileage.apply(lambda x: float(x)/1e3)
  features['car_seats'] = dataframe.car_seats.apply(lambda x: int(str(x).split('.')[0]))
  features['car_year'] = dataframe.car_year.apply(lambda x: float(str(x).split('.')[0]) / 2000)
  return features