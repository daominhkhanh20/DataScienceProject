from scrapy import Spider, Request
from ..items import Car
import re 

class Chotot(Spider):
    name = 'chotot'
    start_url = "https://xe.chotot.com/mua-ban-oto?page={}"
    page_index = 1

    def start_requests(self):
        yield Request(url=self.start_url.format(self.page_index), callback=self.parse)
    
    def parse(self, response):
        
        list_urls = response.xpath('//*[@class="AdItem_wrapperAdItem__1hEwM  AdItem_big__2Sqod"]/a/@href').getall()
        if len(list_urls) > 0:
            for url in list_urls:
                url_page=response.urljoin(url)
                yield Request(url=url_page, callback=self.parse_content)
            if self.page_index < 1500:
                self.page_index += 1
                yield Request(url=self.start_url.format(self.page_index), callback=self.parse)
    
    def parse_content(self, response):
        item = Car()
        item['url'] = response.url
        item['title'] = response.xpath('//*[@itemprop="name"]/text()').getall()[-1]
        item['price'] = response.xpath('//*[@itemprop="price"]/text()').get()
        item['description'] = response.xpath('//*[@itemprop="description"]/text()').get()
        item['seller'] = re.findall('(?<=account_name)[:"]+[\w\s]+["]', response.text)[0][2:]

        item['brand_name'] = response.xpath('//*[@itemprop="carbrand"]/text()').get()
        item['car_model'] = response.xpath('//*[@itemprop="carmodel"]/text()').get()
        item['year_of_manufacture'] = response.xpath('//*[@itemprop="mfdate"]/text()').get()
        item['km_number'] = response.xpath('//*[@itemprop="mileage_v2"]/text()').get()
        item['status'] = response.xpath('//*[@itemprop="condition_ad"]/text()').get()
        item['gear'] = response.xpath('//*[@itemprop="gearbox"]/text()').get()
        item['fuel'] = response.xpath('//*[@itemprop="fuel"]/text()').get()
        item['origin'] = response.xpath('//*[@itemprop="carorigin"]/text()').get()
        item['style'] = response.xpath('//*[@itemprop="cartype"]/text()').get()
        item['number_seat'] = response.xpath('//*[@itemprop="carseats"]/text()').get()
        yield item
        