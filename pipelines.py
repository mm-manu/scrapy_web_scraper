# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy import signals
from scrapy.exporters import CsvItemExporter


class CSVWriterPipeline(object):
    
    def __init__(self,filename):
        self.filename = filename
        
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        filename = settings.get('OUTPUT_FILE')
        pipeline = cls(filename)
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.file = open(self.filename, 'w+b')
        self.exporter = CsvItemExporter(self.file,include_headers_line=True)
        self.exporter.encoding='utf-8'
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item