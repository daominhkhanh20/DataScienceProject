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
### Step 1: Decoding feature in website chotot
Detail about preprocessing in 'util\get_dict.ipynb' <br>
### Step 2: Integrate data <br>
Detail about preprocessing in 'Processing Data\Integrate data.ipynb' <br>

## III. Preprocess
### Step 1: Detail about preprocessing in Preprocess/Preprocess_data.ipynb <br>
### Step 2: Processing description <br>
Detail about preprocessing in 'Processing Description\Transform Description.ipynb' <br>
### Step 3: PCA with vector embedding after Bert model <br>
Detail about preprocessing in 'Processing Description\PCA Description.ipynb' <br>


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
