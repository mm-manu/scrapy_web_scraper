# -*- coding: utf-8 -*-
import scrapy
from items import BrandURL,Product
import csv

class MuellerBrandURLSpider(scrapy.Spider):
    name = 'mueller_url_spider'
    allowed_domains = ['mueller.de']
    start_urls = ['https://shop.mueller.de/parfumerie/marken',
                    'https://shop.mueller.de/naturshop/marken',
                    'https://shop.mueller.de/drogerie/marken',
                    'https://shop.mueller.de/haushalt/marken']
    
    def parse(self, response):
        category = u'undefined'
        if response.url == self.start_urls[0]:
            category = u'Parfüm'
        elif response.url == self.start_urls[1]: 
            category = u'Naturshop'   
        elif response.url == self.start_urls[2]: 
            category = u'Drogerie'  
        elif response.url == self.start_urls[3]: 
            category = u'Haushalt'        
        for url in response.xpath('//div[@class="module module-brands-overview-list"]//a/@href').extract():
            burl = BrandURL()
            burl['url'] = url
            burl['category'] = category            
            yield burl
    
class MuellerProductSpider(scrapy.Spider):
    name = 'mueller_product_spider'
    
    def start_requests(self):
        requests = []
        with open('brand_urls.csv') as urls:
            reader = csv.DictReader(urls)
            for url in reader:
                request = scrapy.Request(url['url'],
                             callback=self.parse)
                request.meta['category'] = url['category']
                request.meta['first_page'] = True
                requests.append(request)
                
        request = scrapy.Request('https://shop.mueller.de/spielwaren/alle-kategorien',
                             callback=self.parse)
        request.meta['category'] = u'Spielwaren'
        request.meta['first_page'] = True
        requests.append(request)
        
        request = scrapy.Request('https://shop.mueller.de/multi-media/filme-tv',
                             callback=self.parse)
        request.meta['category'] = u'Filme'
        request.meta['first_page'] = True
        requests.append(request)
        
        request = scrapy.Request('https://shop.mueller.de/multi-media/musik',
                             callback=self.parse)
        request.meta['category'] = u'Musik'
        request.meta['first_page'] = True
        requests.append(request)
        
        request = scrapy.Request('https://shop.mueller.de/multi-media/games',
                             callback=self.parse)
        request.meta['category'] = u'Games'
        request.meta['first_page'] = True
        requests.append(request)
        
        request = scrapy.Request('https://shop.mueller.de/multi-media/konsolen-zubehor',
                             callback=self.parse)
        request.meta['category'] = u'Konsolen/Zubehör'
        request.meta['first_page'] = True
        requests.append(request)
        
        request = scrapy.Request('https://shop.mueller.de/multi-media/unterhaltungselektronik',
                             callback=self.parse)
        request.meta['category'] = u'Unterhaltungselektronik'
        request.meta['first_page'] = True
        requests.append(request)
        
        request = scrapy.Request('https://shop.mueller.de/buecher/alle-kategorien',
                             callback=self.parse)
        request.meta['category'] = u'Bücher'
        request.meta['first_page'] = True
        requests.append(request)
        
        return requests
        
    def parse(self, response):
        category = response.meta['category']
        first_page = response.meta['first_page']
        for prod_name in response.xpath('//div[@itemprop="name"]/text()').extract():
            product = Product()
            product['name'] = unicode(prod_name.strip().replace('\n','').replace('\r',''))
            product['category'] = category
            yield product 
        
        if first_page:
            last_page = response.xpath('//div[@class="pagination"]/ol').xpath('//a[@class="last"]/text()').extract()
            num_pages = 0
            if last_page:
                print category+' '+str(last_page[0])
                num_pages = int(last_page[0])
            else:
                print category+' '+str(len(response.xpath('//div[@class="pagination"]/ol')))
                num_pages = len(response.xpath('//div[@class="pagination"]/ol'))
            
            self.logger.info(response.url+' >>> '+str(num_pages)+' pages')
            if num_pages > 1:
                for page in range(2,num_pages):
                    request = scrapy.Request(response.url+'?p='+str(page), callback=self.parse)
                    request.meta['category'] = category
                    request.meta['first_page'] = False
                    yield request
        
