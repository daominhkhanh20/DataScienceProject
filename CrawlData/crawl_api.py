import requests 
import json
import pandas as pd 
from tqdm import tqdm
url = "https://gateway.chotot.com/v1/public/ad-listing?&key_param_included=true&cg=2010&o={}"

df = []
for i in tqdm(range(0, 35000, 20)):
    data = requests.get(url.format(i)).content
    data = json.loads(data)['ads']
    if len(data) >0:
        df.extend(data)
    else:
        break


df =pd.DataFrame(df)
df.to_csv('data.csv', index=False)
