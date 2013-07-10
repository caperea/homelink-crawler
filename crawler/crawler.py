CITY = 'beijing'
BASE_URL='http://%s.homelink.com.cn/ershoufang/' % CITY
ESTATE_URL = BASE_URL + '%s.shtml'
PAGE_URL = BASE_URL + 'pg%d/'

ITEM_PER_PAGE = 12

def crawl_total_count():
    import urllib2
    import lxml.html as x
    
    url = BASE_URL
    try:
        raw = urllib2.urlopen(url).read()
    except:
        return 0
    doc = x.document_fromstring(raw)
    count = doc.xpath('/html/body/div[3]/span')
    if len(count) != 1:
        return 0
    return int(count[0].text)

def crawl_page_listing(p):
    import urllib2
    import lxml.html as x
    from models import Listing
    
    url = PAGE_URL % p
    try:
        raw = urllib2.urlopen(url).read()
    except:
        print 'ERROR: urllib2.urlopen(%s).read:' % url
        return
    doc = x.document_fromstring(raw)
    hllinks = doc.xpath('//h3/span/a/@href')
    listing = [link.split('/')[-1].split('.')[0] for link in hllinks]
    c = 0
    for i in listing:
        item = Listing(hlid = i)
        try:
            item.save()
            c += 1
        except:
            pass
    print '%d(%d)' % (p, c)

def crawl_full_listing():
    from MySQLdb import IntegrityError
    from multiprocessing import Pool

    total = int(crawl_total_count() / ITEM_PER_PAGE + 1)
    print total, 'items'
    pool = Pool(5)
    pool.map(crawl_page_listing, range(1,total+1))

def separate_listing(l):
    return [], []
