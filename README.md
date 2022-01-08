# DataScienceProject

## I. Crawl Data 
Start crawl data from 2 website: <br>
- Chotot.com
- Bonbanh.com <br>

Bash script:
```buildoutcfg
cd CrawlData
scrapy crawl bonbanh -o bonbanh.json
scrapy crawl chotot -o chotot.json
python3 crawl_api.py
```
## II. Intergration data
Step 1: Run all 'get_dict.ipynb' file
Detail about preprocessing in 'util\get_dict.ipynb'
Step 2: Run all Integrate 'data.ipynb' file
Detail about preprocessing in 'Processing Data\Integrate data.ipynb'

## III. Preprocess
Step 1: Detail about preprocessing in Preprocess/Preprocess_data.ipynb
Step 2: Run all 'Transform Description.ipynb' to process description
Detail about 'Processing Description\Transform Description.ipynb'
Step 2: Run all 'PCA Description.ipynb' to PCA description
Detail about 'Processing Description\PCA Description.ipynb'


### IV. Model 

#### 1. Ridge Regression 
```buildoutcfg
cd Model
python3 ML.py --model_name 'ridge'
```
#### 2. KNN Regression 
```buildoutcfg
cd Model
python3 ML.py --model_name 'knn'
```
#### 3. Decision Tree Regression 
```buildoutcfg
cd Model
python3 ML.py --model_name 'decision_tree'
```

#### 4. XGBoost
``` bash
cd Model_for_web
pip install -r requirements.txt
uvicorn api:app --port 8000 --host 0.0.0.0
```
Access 0.0.0.0/docs to get doc and request format.

####  5. Random Forest
Detail about modeling in Model\RandomForest.ipynb
