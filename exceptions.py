import scrapy

from scrapy.exceptions import CloseSpider

from cbury_scrapy.items import MyItem

class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["example.com"]
    start_urls = [
        "http://example.com/cgi/search?&startidx=",
    ]

    url_index = 0
    MAX_URLS_TO_GET = 16
    URLS_PER_PAGE = 10
    
    records_remaining = MAX_URLS_TO_GET
    crawl_done = False
    
    da = MyItem()        
    da['key'] = u"test"
        
    def parse(self, response):
        """ Start on search results page from index """ 
        while self.crawl_done != True:
            url = "http://example.com/cgi/search?&start_index=" + str(self.url_index)
            yield scrapy.Request(url, callback=self.parse_results)
            self.url_index += self.URLS_PER_PAGE

    
    def parse_results(self, response):
        # Retrieve all table rows from results page
        for row in response.xpath('//table/tr[@class="datrack_resultrow_odd" or @class="datrack_resultrow_even"]'):
            # extract the Description and Status fields
            
            # extract the link to Item page
            url = r.xpath('//td[@class="datrack_danumber_cell"]//@href').extract_first()
            yield scrapy.Request(url, callback=self.parse_item)

            if self.records_remaining == 0:
                self.crawl_done = True
                raise CloseSpider('Scraped requested number of records.')
            
            self.records_remaining -= 1
        
    def parse_item(self, response):
        # get fields from item page
        # ...   
        yield self.item
