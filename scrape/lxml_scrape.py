# scrape_cbury_da_list.py
from lxml import html
import requests
from time import strftime
import re

# base url of cbury council DA list
url = "http://datrack.canterbury.nsw.gov.au/cgi/datrack.pl?search=search&startidx="
RESULTS_PER_PAGE = 10

def write_list_csv(l):
    import csv

    fname = strftime("%Y-%m-%d %H:%M:%S") + ".csv"
    with open(fname, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(l)

def get_da_all(l):
    npages = get_qty_da_results() / RESULTS_PER_PAGE
    i = 0
    l = []
    while i < 30:
      l += get_da_list(i)
      i += RESULTS_PER_PAGE

def get_da_list(start=0):    
    tree = get_html_from(url + str(start))
    
    # get all DA no. date and links
    da_no = tree.xpath('//td[@class="datrack_danumber_cell"]//text()')
    # get href attribute of all td with class datrack_danumber_cell 
    da_url = tree.xpath('//td[@class="datrack_danumber_cell"]//@href')
    lodged_date = tree.xpath('//td[@class="datrack_lodgeddate_cell"]//text()')

    # get tr classes with name datrack_resultrow_label* so we get both odd and even
    desc = tree.xpath('//tr[starts-with(@class, "datrack_resultrow_label")]/td//text()')

    # get address details, keep separate to make queries more friendly later
    house_no = tree.xpath('//td[@class="datrack_houseno_cell"]//text()')
    street = tree.xpath('//td[@class="datrack_street_cell"]//text()')
    town = tree.xpath('//td[@class="datrack_town_cell"]//text()')

    est_cost = []
    desc_full = []
    time_now = []
    for i in da_url:
        tree = get_html_from(i)
        desc_full += tree.xpath("//*[contains(text(), 'Description:')]/following-sibling::td/text()")
       # tmp_str = re.sub('[$,]', '',
       #           tree.xpath("//*[contains(text(), 'Estimated Cost:')]/following-sibling::td//text()"))
        # TODO strip $ and , from cost string
        est_cost += tree.xpath("//*[contains(text(), 'Estimated Cost:')]/following-sibling::td//text()")
        # TODO fix bug not output time properly
        time_now += strftime("%Y-%m-%d %H:%M:%S")
    # compile separate lists into one list of tuples
    dal = zip(time_now, da_no, lodged_date, est_cost, da_url, house_no, street, town, desc)
    # print dal
    return dal

def get_html_from(url):
    print "GET:", url
    page = requests.get(url)
    return html.fromstring(page.content)
    
def get_qty_da_results():
    tree = get_html_from(url)
    # get no. results for wide search
    # get last integer of div datrack_countheader
    return int(tree.xpath('//span[@class="datrack_count"]//text()')[0].split()[-1])

#gn = get_qty_da_results
#ga = get_da_all

wcsv = write_list_csv
dal = []
gp = get_da_list

dal = gp()
wcsv(dal)

# TODO
# get additional pages

#get_page_da(start, r
def join_addr_fields(house_no, street, town):
    addr = []
    for (i,j,k) in zip(house_no, street, town):
        addr.append("{} {} {}".format(i, j, k))

