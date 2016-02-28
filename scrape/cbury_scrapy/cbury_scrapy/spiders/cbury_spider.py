import scrapy

from cbury_scrapy.items import DA, DA_Person, Person

def td_text_after(label, response):
    """ retrieves text from a td following that containing label e.g.:"""
    """ response.xpath("//*[contains(text(), 'Description:')]/following-sibling::td//text()").extract() """
    return response.xpath("//*[contains(text(), '" + label + "')]/following-sibling::td//text()").extract_first()

class CburySpider(scrapy.Spider):
    name = "cbury"
    allowed_domains = ["datrack.canterbury.nsw.gov.au"]
    start_urls = [
        "http://datrack.canterbury.nsw.gov.au/cgi/datrack.pl?search=search&startidx=",
    ]

    url_start_i = 20
    MAX_URLS_TO_GET = 4
    url_end_i = url_start_i + MAX_URLS_TO_GET
    URLS_PER_PAGE = 10
        
    def parse(self, response):
        """ return DA URLs from search page """ 
        # get number of total records
        num_records = int(response.xpath('//span[@class="datrack_count"]//text()').extract_first().split()[-1])        
        url = "http://datrack.canterbury.nsw.gov.au/cgi/datrack.pl?search=search&startidx=" + str(self.url_start_i)
        yield scrapy.Request(url, callback=self.parse_da_list)

    def parse_da_list(self, response):
        """ follow each DA link """
        for href in response.xpath('//td[@class="datrack_danumber_cell"]//@href'):
            url = href.extract()
            yield scrapy.Request(url, callback=self.parse_da_item)

    def parse_da_item(self, response):
        """ get DA data """
        da = DA()        
        da['lga'] = u"Canterbury Council"
        da['url'] = response.url

        labels = { 'da_no': 'Application No:', 'date_lodged': 'Date Lodged:',
                   'desc_full': 'Description:', 'est_cost': 'Estimated Cost:',
                   'status': 'Status:', 'date_determined': 'Date Determined:', 
                   'decision': 'Decision:', 'officer': 'Responsible Officer:'}

        # map DA fields with those in the folliwng <td> elements on the page
        for i in labels:
            da[i] = td_text_after(labels[i], response)

        # Get people data from 'Names' table, 'Role' heading
        da['names'] = []

        for row in response.xpath('//table/tr[th[1]="Role"]/following-sibling::tr'):    
            da_p = {}
            da_p['role'] = row.xpath('normalize-space(./td[1])').extract_first()            
            da_p['name_no'] = row.xpath('normalize-space(./td[2])').extract_first()
            da_p['full_name'] = row.xpath('normalize-space(./td[3])').extract_first()
            da['names'].append(da_p)

        yield da

    def parse_persons(self, response):        
        # extract people from DA page and Person(s) list for all DAs
        person = []
        p = {}
        
        # Get people data from 'Names' table, 'Role' heading
        for row in response.xpath('//table/tr[th[1]="Role"]/following-sibling::tr'):
            # add persons ID no. and role to DA and full name to Person db 
            p['name_no'] = row.xpath('normalize-space(./td[2])').extract_first()
            p['full_name'] = row.xpath('normalize-space(./td[3])').extract_first()
            people.append(p)
            
        yield people
