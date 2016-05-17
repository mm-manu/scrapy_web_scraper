import scrapy
from scrapy.crawler import CrawlerProcess
from spiders import mueller

def get_brand_URLs():
    settings = scrapy.settings.Settings()
    settings.setmodule('settings',1)
    settings.set(name='USER_AGENT', value='Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)', priority='project')
    settings.set(name='OUTPUT_FILE', value='output/brand_urls.csv')
    settings.set(name='ITEM_PIPELINES', value={'pipelines.CSVWriterPipeline': 1,})
    process = CrawlerProcess(settings)
    process.crawl(mueller.MuellerBrandURLSpider)
    process.start()  

def get_products():
    settings = scrapy.settings.Settings()
    settings.setmodule('settings',1)
    settings.set(name='LOG_LEVEL', value='WARNING')
    settings.set(name='USER_AGENT', value='Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)', priority='project')
    settings.set(name='OUTPUT_FILE', value='output/products.csv')
    settings.set(name='ITEM_PIPELINES', value={'pipelines.CSVWriterPipeline': 1,})
    process = CrawlerProcess(settings)
    process.crawl(mueller.MuellerProductSpider)
    process.start()

get_brand_URLs()
get_products()