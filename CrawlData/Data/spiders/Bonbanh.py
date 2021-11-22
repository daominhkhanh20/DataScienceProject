from scrapy import Spider, Request
from ..items import BonBanh
import re 

class Chotot(Spider):
    name = 'bonbanh'
    start_url = "https://bonbanh.com/oto/page,{}"
    page_index = 1

    def start_requests(self):
        yield Request(url=self.start_url.format(self.page_index), callback=self.parse)
    
    def parse(self, response):
        
        list_urls = response.xpath('//li[contains(@class, "car-item")]/a/@href').getall()
        for url in list_urls:
            url_page=response.urljoin(url)
            yield Request(url=url_page, callback=self.parse_content)

        if self.page_index <= 1972:
            self.page_index += 1
            yield Request(url=self.start_url.format(self.page_index), callback=self.parse)
    
    def parse_content(self, response):
        item = BonBanh()
        item['url'] = response.url
        item['title'] = response.xpath('//*[@id="car_detail"]/div[3]/h1/text()').get()
        item['description'] = response.xpath('//*[@id="sgg"]/div/div[1]/div[4]/div/text()').getall()

        seller = response.xpath('//div[@class="contact-txt"]/a/text()').get()
        if seller is None:
            seller = response.xpath('//div[@class="contact-txt"]/span/text()').get()
        item['seller'] = seller
        item['seller_address'] = response.xpath('//*[@id="car_detail"]/div[7]/div[2]/div/text()').getall()[2]
        
        item['origin'] = response.xpath('//div[@class="col"][1]/div[@id="mail_parent"][1]/div[2]/span/text()').get()
        item['status'] = response.xpath('//div[@class="col"][1]/div[@id="mail_parent"][2]/div[2]/span/text()').get()
        item['car_model'] = response.xpath('//div[@class="col"][1]/div[@id="mail_parent"][3]/div[2]/span/text()').get()
        item['km_number'] = response.xpath('//div[@class="col"][1]/div[@id="mail_parent"][4]/div[2]/span/text()').get()
        item['exterior_color'] = response.xpath('//div[@class="col"][1]/div[@id="mail_parent"][5]/div[2]/span/text()').get()
        item['interior_color'] = response.xpath('//div[@class="col"][1]/div[@id="mail_parent"][6]/div[2]/span/text()').get()
        item['number_door'] = response.xpath('//div[@class="col"][1]/div[@id="mail_parent"][7]/div[2]/span/text()').get()
        item['number_seat'] = response.xpath('//div[@class="col"][1]/div[@id="mail_parent"][8]/div[2]/span/text()').get()

        item['engine'] = response.xpath('//div[@class="col"][2]/div[@id="mail_parent"][1]/div[2]/span/text()').get()
        item['refueling_system'] = response.xpath('//div[@class="col"][2]/div[@id="mail_parent"][2]/div[2]/span/text()').get()
        item['gear'] = response.xpath('//div[@class="col"][2]/div[@id="mail_parent"][3]/div[2]/span/text()').get()
        item['actuator'] = response.xpath('//div[@class="col"][2]/div[@id="mail_parent"][4]/div[2]/span/text()').get()
        item['fuel_comsumption'] = response.xpath('//div[@class="col"][2]/div[@id="mail_parent"][5]/div[2]/span/text()').get()
        yield item
        