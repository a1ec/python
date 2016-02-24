import scrapy

from cbury_scrapy.items import DA

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
        # get number of records
        num_records = int(response.xpath('//span[@class="datrack_count"]//text()').extract()[0].split()[-1])

        while i < 10:
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
        # parsing DA item happens here
        da = DA()
       
        da['da_no'] = response.xpath("//*[contains(text(), 'Application No:')]/following-sibling::td/text()").extract()
        da['lga'] = u"Canterbury Council"
        # TODO URL, get from response.url?
        # da['da_url'] = response.xpath("//*[contains(text(), 'Application No:')]/following-sibling::td/text()").extract()
        
        # TODO clean this up, method for next sibling
        da['date_lodged'] = response.xpath("//*[contains(text(), 'Date Lodged:')]/following-sibling::td/text()").extract()
        
        da['desc_full'] = response.xpath("//*[contains(text(), 'Description:')]/following-sibling::td/text()").extract()
        da['est_cost'] = response.xpath("//*[contains(text(), 'Estimated Cost:')]/following-sibling::td/text()").extract()
        da['status'] = response.xpath("//*[contains(text(), 'Status:')]/following-sibling::td/text()").extract()

        da['date_determined'] = response.xpath("//*[contains(text(), 'Date Determined:')]/following-sibling::td/text()").extract()        
        da['decision'] = response.xpath("//*[contains(text(), 'Decision:')]/following-sibling::td/text()").extract()
        
        #da['date_scr_modified'] = response.xpath("//*[contains(text(), 'Decision:')]/following-sibling::td/text()").extract()
        yield da
