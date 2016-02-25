import scrapy

from cbury_scrapy.items import DA

# retrieves text in td after that containing label
def td_text_after(label, response):
    return response.xpath("//*[contains(text(), '" + label + "')]/following-sibling::td//text()").extract()

class scr_session:
    def __init__(self):
        # date_started = time.now()
        # entries returned
        pass

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
        labels_d = { 'da_no': 'Application No:', 'date_lodged': 'Date Lodged:',
                     'desc_full': 'Description:', 'est_cost': 'Estimated Cost:',
                     'status': 'Status:', 'date_determined': 'Date Determined:', 
                     'decision': 'Decision:'}

        # map our da fields with those in the td elements from the page
        for i in labels_d:
            da[i] = td_text_after(labels_d[i], response)

        da['lga'] = u"Canterbury Council"
        da['url'] = response.url
        
        # TODO get people
        p = Person()
        p['name_no'] = ""
        p['full_name'] = ""
        
        yield da
