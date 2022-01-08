# DataScienceProject

## I. Crawl Data 
Start crawl data from 2 website: <br>
- Chotot.com
- Bonbanh.com <br>

Bash script:
```buildoutcfg
cd CrawlData
scrapy crawl bonbanh
scrapy crawl chotot
```
## II. Model 

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
#### 1. Decision Tree Regression 
```buildoutcfg
cd Mode
python3 ML.py --model_name 'decision_tree'
```
