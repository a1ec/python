import scrapy

from cbury_scrapy.items import CburyItem

class CburySpider(scrapy.Spider):
    name = "cbury"
    allowed_domains = ["datrack.canterbury.nsw.gov.au"]
    start_urls = [
        "http://datrack.canterbury.nsw.gov.au/cgi/datrack.pl?search=search&startidx=",
    ]

    # parse: get the next list to parse
    # parse_da_list: request list page
    # parse_da_item: requset da item details
    def parse(self, response):
        #yield scrapy.Request(url, callback=self.parse_da_list)
        i = 0
        while i < 60:
            url = "http://datrack.canterbury.nsw.gov.au/cgi/datrack.pl?search=search&startidx=" + str(i)
            i += 10
            yield scrapy.Request(url, callback=self.parse_da_list)
    """        
        def parse(self, response):
            # list view - get next page link
            url = response.xpath("//*[text() = 'Next']//@href").extract()[0]
            yield scrapy.Request(url, callback=self.parse_da_list)
    """

    def parse_da_list(self, response):
        # follow each da link
        for href in response.xpath('//td[@class="datrack_danumber_cell"]//@href'):
            # url = response.urljoin(href.extract())
            url = href.extract()
            yield scrapy.Request(url, callback=self.parse_da_item)


    def parse_da_item(self, response):
        item = CburyItem()

        item['da_no'] = response.xpath("//*[contains(text(), 'Application No:')]/following-sibling::td/text()").extract()
        item['date_lodged'] = response.xpath("//*[contains(text(), 'Date Lodged:')]/following-sibling::td/text()").extract()
        item['desc'] = response.xpath("//*[contains(text(), 'Description:')]/following-sibling::td/text()").extract()
        item['est_cost'] = response.xpath("//*[contains(text(), 'Estimated Cost:')]/following-sibling::td/text()").extract()
        item['status'] = response.xpath("//*[contains(text(), 'Status:')]/following-sibling::td/text()").extract()
        
        yield item
