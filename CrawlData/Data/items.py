import scrapy
from scrapy.item import Field

class Car(scrapy.Item):
    url = Field(default=None)
    title = Field(default=None)
    price = Field(default=None)
    description = Field(default=None)
    seller = Field(default=None)
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


class BonBanh(scrapy.Item):
    url = Field(default=None)
    title = Field(default=None)
    description = Field(default=None)
    seller = Field(default=None)
    seller_address = Field(default=None)
    origin = Field(default=None)
    status = Field(default=None)
    car_model = Field(default=None)
    km_number = Field(default=None)
    exterior_color = Field(default=None)
    interior_color = Field(default=None)
    number_door = Field(default=None)
    number_seat = Field(default=None)
    refueling_system = Field(default=None)
    engine = Field(default=None)
    gear = Field(default=None)
    actuator = Field(default=None)
    fuel_comsumption = Field(default=None)
    