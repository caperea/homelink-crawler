CITY = 'beijing'
BASE_URL='http://%s.homelink.com.cn/ershoufang/' % CITY
ESTATE_URL = BASE_URL + '%s.shtml'
DIST_SFX = '%s/'
PAGE_SFX = 'pg%d/'

NUM_WORKERS = 5
ITEM_PER_PAGE = 12

def crawl_item_count(url):
    import urllib2
    import lxml.html as x
    
    try:
        raw = urllib2.urlopen(url).read()
    except:
        return 0
    doc = x.document_fromstring(raw)
    entries = doc.xpath('/html/body/div[3]/span')
    if len(entries) != 1:
        return 0
    return int(entries[0].text)

def crawl_page_listing(url):
    import urllib2
    import lxml.html as x
    from models import Listing
    
    try:
        raw = urllib2.urlopen(url).read()
    except:
        print 'ERROR: urllib2.urlopen(%s).read:' % url
        return
    doc = x.document_fromstring(raw)
    links = doc.xpath('//h3/span/a/@href')
    listing = [link.split('/')[-1].split('.')[0] for link in links]
    for i in listing:
        item = Listing(hlid = i)
        try:
            item.save()
        except:
            pass

def crawl_full_listing(url=BASE_URL):
    from multiprocessing import Pool

    n_entries = crawl_item_count(url)
    n_pages = int(n_entries / ITEM_PER_PAGE + 1)
    print n_pages, 'pages'
    pool = Pool(NUM_WORKERS)
    pool.map(crawl_page_listing, [url + PAGE_SFX % p for p in range(1, n_entries+1)])

def crawl_districts():
    import urllib2
    import lxml.html as x
    from models import District
    try:
        raw = urllib2.urlopen(BASE_URL).read().decode('utf8')
    except:
        print 'ERROR: urllib2.urlopen(%s).read().decode(\'utf8\'):' % BASE_URL
        return
    doc = x.document_fromstring(raw)
    desc = doc.xpath('/html/body/div[4]/dl[1]//a')
    hlid = doc.xpath('/html/body/div[4]/dl[1]//a/@href')
    desc = [d.text for d in desc[1:]]
    hlid = [l.split('/')[-2] for l in hlid[1:]]
    for arg in zip(hlid, desc):
        dist = District(hlid=arg[0], desc=arg[1])
        try:
            dist.save()
        except:
            pass

def crawl_subdistricts():
    import urllib2
    import lxml.html as x
    from models import District, Subdistrict
    dists = District.objects.all()
    for dist in dists:
        try:
            raw = urllib2.urlopen(BASE_URL + DIST_SFX % dist.hlid).read().decode('utf8')
        except:
            print 'ERROR: urllib2.urlopen(%s).read().decode(\'utf8\'):' % BASE_URL
            continue
        doc = x.document_fromstring(raw)
        subdists = doc.xpath('/html/body/div[4]/dl[1]/div[2]/ul/li/a')
        for subdist in subdists[1:]:
            sd = Subdistrict(hlid='b'+subdist.attrib['href'].split('/')[-2].split('b')[-1], desc=subdist.text, dist=dist)
            try:
                sd.save()
            except:
                pass
