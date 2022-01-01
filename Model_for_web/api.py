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

# with open("model.pth", "rb") as f:
#     model = pickle.load(f)

# train_data = pd.read_csv("train_data.csv")

model = None
train_data = None

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
    region: str = Field(..., help="Region of car, name of the province or city.")
    gear: str = Field(..., help="Type of gear.")
    style: str = Field(..., help="Style of car.")
    car_mileage: float = Field(..., help="Number of km ran, 0.0 with new car.")
    car_seats: int = Field(..., help="Number of seats.")
    car_year: int = Field(..., help="Car manufacture year.")
    fuel: str = Field(..., help="Type of fuel")

class PredictionResponse(BaseModel):
    car_price: float

    @classmethod
    def failed_response(cls):
        return cls(status="failed", data=[])
    
    @classmethod
    def price_response(cls, car_price):
        return cls(status="success", data=car_price)

@app.get("/", response_class=HTMLResponse)
async def hello(request: Request):
    return "Hello, model api."

@app.get("/predict", response_model=PredictionResponse, responses={
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
    "origin": "Thailand",
    "status": "Đã sử dụng",
    "car_color": "Trắng",
    "region": "Hà Nội",
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
    try:
        global model
        global train_data
        if car_detail.origin == "Unknown":
            car_detail.origin = train_data[(train_data.brand_name == car_detail.brand_name)&(train_data.model == car_detail.model)].origin.mode().tolist()[0]
        if car_detail.status == "Unknown":
            car_detail.status = train_data[(train_data.brand_name == car_detail.brand_name)&(train_data.model == car_detail.model)].status.mode().tolist()[0]
        if car_detail.car_color == "Unknown":
            car_detail.car_color = train_data[(train_data.brand_name == car_detail.brand_name)&(train_data.model == car_detail.model)].car_color.mode().tolist()[0]
        if car_detail.region == "Unknown":
            car_detail.region = train_data[(train_data.brand_name == car_detail.brand_name)&(train_data.model == car_detail.model)].region.mode().tolist()[0]
        if car_detail.style == "Unkown":
            car_detail.style = train_data[(train_data.brand_name == car_detail.brand_name)&(train_data.model == car_detail.model)].style.mode().tolist()[0]
        df = pd.DataFrame(car_detail)
        feature = process_dataframe(df)
        result = model.predict(feature)[0]
        return PredictionResponse.price_response(math.exp(result))
    except Exception as e:
        raise e
        return PredictionResponse.failed_response()

@app.get('/health')
async def health_check():
    return JSONResponse(status_code=200)

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000)
