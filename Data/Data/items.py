import scrapy
from scrapy.item import Field

class Car(scrapy.Item):
    url = Field(default=None)
    title = Field(default=None)
    price = Field(default=None)
    description = Field(default=None)
    seller = Field(default=None)
    # chat_response_ratio = Field = Field(default=None)

    brand_name = Field(default=None)
    car_model = Field(default=None)
    year_of_manufacture = Field(default=None)
    km_number = Field(default=None)
    status = Field(default=None)
    gear = Field(default=None)
    fuel = Field(default=None)
    origin = Field(default=None)
    style = Field(default=None)
    number_seat = Field(default=None)
