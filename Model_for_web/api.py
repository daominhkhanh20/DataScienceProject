from fastapi import Body, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi.responses import PlainTextResponse, HTMLResponse, FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from xgboost.sklearn import XGBRegressor
import pickle
from source.utils import process_dataframe
import pandas as pd
import math
import numpy as np

with open("model.pth", "rb") as f:
    model = pickle.load(f)

train_data = pd.read_csv("train_data.csv")

car_name_list = train_data["car_name"].unique()
brand_list = train_data.brand_name.unique().tolist()
model_list = train_data.model.unique().tolist()

with open("default_features.txt") as f:
    default_features = f.read().splitlines()

# model = None
# train_data = None

app = FastAPI(version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class CarDetail(BaseModel):
    brand_name: str = Field(..., help="brand name of car")
    model: str = Field(..., help="")
    origin: str = Field(..., help="Country origin of car.")
    status: str = Field(..., help="Status of car, used or new.")
    car_color: str = Field(..., help="Car color.")
    region_name: str = Field(..., help="Region of car, name of the province or city.")
    gear: str = Field(..., help="Type of gear.")
    style: str = Field(..., help="Style of car.")
    car_mileage: float = Field(..., help="Number of km ran, 0.0 with new car.")
    car_seats: int = Field(..., help="Number of seats.")
    car_year: int = Field(..., help="Car manufacture year.")
    fuel: str = Field(..., help="Type of fuel")

class PredictionResponse(BaseModel):
    status: str
    car_price: float

    @classmethod
    def failed_response(cls):
        return cls(status="failed", car_price=[])
    
    @classmethod
    def price_response(cls, car_price):
        return cls(status="success", car_price=car_price)

@app.get("/", response_class=HTMLResponse)
async def hello(request: Request):
    return "Hello, model api."

@app.post("/predict", response_model=PredictionResponse, responses={
    200: {
        "content": {
            "application/json": {
                "example": {
                    "status": "success",
                    "car_price": 100000000
                }
            }
        }
    }
})
async def predict(car_detail: CarDetail = Body(..., example={
    "brand_name": "Toyota",
    "model": "Camry",
    "origin": "Thái Lan",
    "status": "Đã sử dụng",
    "car_color": "Trắng",
    "region_name": "Hà Nội",
    "gear": "Tự động",
    "style": "Sedan",
    "car_mileage": 13.4e6,
    "car_seats": 4,
    "car_year": 2010,
    "fuel": "Xăng"
})):
    """
    Function for price prediction
    """
    print(type(car_detail))
    try:
        global model
        global train_data
        global default_features
        global car_name_list
        global model_list
        global brand_list

        detail = car_detail.dict()
        detail = {k: [v] for k, v in detail.items()}
        test_data = pd.DataFrame(detail)
        # test_data.car_name = test_data.car_name.apply(lambda x: x if x in car_name_list else "Unknown")
        #2
        test_data.brand_name = test_data.brand_name.apply(lambda x: x if x in brand_list else "Unknown")
        #3
        test_data.model = test_data.model.apply(lambda x: x if x in model_list else "Unknown")
        #4
        test_data.origin = test_data.origin.apply(lambda x: x if x in ['Việt Nam', 'Nước khác', 'Thái Lan', 'Mỹ', 'Đức', 'Hàn Quốc', 'Nhật Bản', 'Ấn Độ', 'Đài Loan', 'Trung Quốc', 'Unknown'] else "Unknown")
        #5
        test_data.car_color = test_data.car_color.apply(lambda x: x if x in ['Bạc', 'Unknown', 'Nâu', 'Xám', 'Trắng', 'Đen', 'Đỏ', 'Xanh', 'Màu khác', 'Cam', 'Vàng', 'Nhiều màu', 'Hồng', 'Tím'] else "Unknown")
        #6
        test_data.gear = test_data.gear.apply(lambda x: x if x in ['Số sàn', 'Tự động', 'Bán tự động', 'Unknown'] else "Unknown")
        #7
        test_data["style"] = test_data["style"].apply(lambda x: x if x in ['Minivan (MPV)', 'Sedan', 'SUV / Cross over', 'Pick-up (bán tải)', 'Kiểu dáng khác', 'Van', 'Hatchback', 'Coupe (2 cửa)', 'Mui trần', 'Unknown'] else "Unknown")
        #8
        test_data.region_name = test_data.region_name.apply(lambda x: x if x in ['Vĩnh Phúc', 'Hà Nội', 'Tp Hồ Chí Minh', 'Unknown', 'Lạng Sơn',
            'Hải Phòng', 'Hải Dương', 'Quảng Ninh', 'Cần Thơ', 'Bình Phước',
            'Bình Dương', 'Nghệ An', 'Bắc Ninh', 'Đồng Nai', 'Đà Nẵng',
            'Long An', 'Gia Lai', 'Thanh Hóa', 'Đắk Lắk', 'Tiền Giang',
            'Bà Rịa - Vũng Tàu', 'Phú Thọ', 'An Giang', 'Tây Ninh', 'Lâm Đồng',
            'Yên Bái', 'Bắc Giang', 'Điện Biên', 'Bình Định', 'Thái Nguyên',
            'Bến Tre', 'Đồng Tháp', 'Vĩnh Long', 'Hà Tĩnh', 'Ninh Bình',
            'Kiên Giang', 'Nam Định', 'Bình Thuận', 'Thái Bình', 'Lào Cai',
            'Trà Vinh', 'Kon Tum', 'Hưng Yên', 'Khánh Hòa', 'Quảng Trị',
            'Quảng Nam', 'Quảng Ngãi', 'Hà Giang', 'Bắc Kạn', 'Thừa Thiên Huế',
            'Hà Nam', 'Quảng Bình', 'Bạc Liêu', 'Lai Châu', 'Tuyên Quang',
            'Ninh Thuận', 'Sơn La', 'Sóc Trăng', 'Phú Yên', 'Hòa Bình',
            'Hậu Giang', 'Đắk Nông', 'Cà Mau', 'Cao Bằng'] else "Unknown")
        #8
        test_data.fuel = test_data.fuel.apply(lambda x: x if x in ['Dầu', 'Xăng', 'Động cơ Hybrid', 'Unknown'] else "Unknown")
        
        features_test = pd.DataFrame(data=np.zeros((test_data.shape[0], len(default_features)), dtype=float), columns=list(default_features))
        features_test_trans = process_dataframe(test_data.reset_index(drop=True))
        for item in list(features_test_trans):
            features_test[item] = features_test_trans[item]
        result = model.predict(features_test.to_numpy())[0]
        print(result)
        return PredictionResponse.price_response(car_price=math.exp(result))
    except Exception as e:
        raise e
        return PredictionResponse.failed_response()

@app.get('/health')
async def health_check():
    return JSONResponse(status_code=200)

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000)
