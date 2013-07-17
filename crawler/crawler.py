#!/usr/bin/python2
# -*- coding: utf8 -*-

CITY = 'beijing'
BASE_URL='http://%s.homelink.com.cn/' % CITY
ESTATE_URL = BASE_URL + 'ershoufang/%s.shtml'
DIST_SFX = 'ershoufang/%s/'
PAGE_SFX = 'ershoufang/pg%d/'
COMM_SFX = '%s/xq/'
ESTATE_SFX = 'ershoufang/%s.shtml'

NUM_WORKERS = 5
ITEM_PER_PAGE = 12

def url_from_district(d):
    return BASE_URL + DIST_SFX % d.hlid

def url_from_subdistrict(sd):
    return BASE_URL + DIST_SFX % (sd.dist.hlid + sd.hlid)

def url_from_community_id(hlid):
    return BASE_URL + COMM_SFX % hlid

def url_from_estate(e):
    return BASE_URL + ESTATE_SFX % e.hlid

def doc_from_url(url, encoding='utf8'):
    import urllib2
    import lxml.html as x
    raw = urllib2.urlopen(url).read()
    #try:
    #    raw = urllib2.urlopen(url).read()
    #except:
    #    print 'ERROR: urllib2.urlopen(%s).read:' % url
    #    return []
    if encoding:
        raw = raw.decode(encoding)
    return x.document_fromstring(raw)

def crawl_item_count(url):
    doc = doc_from_url(url)
    entries = doc.xpath('/html/body/div[3]/span')
    if len(entries) != 1:
        print 'ERROR:', entries
        return -1
    return int(entries[0].text)

def crawl_estate_list_in_page(url):
    doc = doc_from_url(url)
    links = doc.xpath('//h3/span/a/@href')
    return [link.split('/')[-1].split('.')[0] for link in links]

def crawl_estate_list_in_district(url=BASE_URL):
    from multiprocessing import Pool

    n_entries = crawl_item_count(url)
    print n_entries,
    n_pages = int(n_entries / ITEM_PER_PAGE + 1)
    pool = Pool(NUM_WORKERS)
    l = pool.map(crawl_estate_list_in_page, [url + PAGE_SFX % p for p in range(1, n_pages + 1)])
    listing = []
    if l:
        for sl in l:
            listing += sl
    print len(listing)
    # attempt to solve 'Too may open files' issue
    pool.terminate()
    return listing

def update_estate_list():
    from models import Subdistrict, RealEstate, EstateZoning
    from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
    from time import time
    subdists = Subdistrict.objects.filter(updated=0).order_by('hlid')
    for sd in subdists:
        print sd.dist.desc, sd.desc, sd.hlid
        l = crawl_estate_list_in_district(url_from_subdistrict(sd))
        for i in l:
            e, c = RealEstate.objects.get_or_create(hlid=i)
            e.save()
            ez, c = EstateZoning.objects.get_or_create(estate=e, subdist=sd)
            ez.save()
        sd.updated = True
        sd.save()

def update_districts():
    from models import District
    doc = doc_from_url(BASE_URL)
    desc = doc.xpath('/html/body/div[4]/dl[1]//a')
    hlid = doc.xpath('/html/body/div[4]/dl[1]//a/@href')
    desc = [d.text for d in desc[1:]]
    hlid = [l.split('/')[-2] for l in hlid[1:]]
    for arg in zip(hlid, desc):
        dist = District(hlid=arg[0], desc=arg[1])
        try:
            dist.save()
            print 'Added new district', dist.desc
        except:
            pass

def update_subdistricts():
    from models import District, Subdistrict
    dists = District.objects.all()
    for dist in dists:
        url = url_from_district(dist)
        doc = doc_from_url(url, 'utf8')
        subdists = doc.xpath('/html/body/div[4]/dl[1]/div[2]/ul/li/a')
        for subdist in subdists[1:]:
            sd = Subdistrict(hlid='b'+subdist.attrib['href'].split('/')[-2].split('b')[-1], desc=subdist.text, dist=dist)
            try:
                sd.save()
                print 'Added new subdistrict', sd.desc
            except:
                pass

def crawl_estates(update=False):
    from models import RealEstate
    from multiprocessing import Pool
    if update:
        estates = RealEstate.objects.all()
    else:
        estates = RealEstate.objects.filter(updated=0)
    #for e in estates:
    #    e = update_estate_detail(e)
    pool = Pool(NUM_WORKERS)
    p = pool.map_async(update_estate_detail_pool_worker, estates)
    try:
        p.get(0xFFFF)
    except KeyboardInterrupt:
        pool.terminate()
        return

def update_community_detail(hlid):
    from models import Community
    doc = doc_from_url(url_from_community_id(hlid))
    comm = Community.objects.get_or_create(hlid=hlid)[0]
    comm.desc = doc.xpath('/html/body/div[3]/div[1]/ul/h1')[0].text
    comm.addr = doc.xpath('/html/body/div[3]/div[3]/div[1]/div[1]/dl[1]/dd[2]')[0].text
    comm.detail = doc.xpath('/html/body/div[3]/div[3]/div[1]/div[2]/div[2]')[0].text.strip()
    #print 'Community:', comm.desc, comm.addr
    print '*',
    comm.save()

def update_estate_detail(estate):
    from models import RealEstate, Community
    from urllib2 import URLError
    from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
    #estate = RealEstate.objects.get_or_create(hlid=estate.hlid)[0]
    print estate.hlid,
    try:
        doc = doc_from_url(url_from_estate(estate))
    except URLError:
        print 'URLError!'
        return
    if '抱歉，没有找到符合您要求的房源！'.decode('utf8') in doc.text_content():
        estate.in_sale = False
        print 'SOLD'
    else:
        c_hlid = doc.xpath('/html/body/div[6]/div[2]/div[2]/ol/li[4]/a[1]/@href')[0][1:-1]
        try:
            estate.community = Community.objects.get(hlid=c_hlid)
        except ObjectDoesNotExist:
            update_community_detail(c_hlid)
            estate.community = Community.objects.get(hlid=c_hlid)
        estate.desc = doc.xpath('/html/body/div[5]/h1')[0].text
        estate.nbedrm = int(doc.xpath('/html/body/div[6]/div[2]/div[2]/ol/li[1]/b[1]')[0].text)
        estate.nlvnrm = int(doc.xpath('/html/body/div[6]/div[2]/div[2]/ol/li[1]/b[2]')[0].text)
        estate.area = float(doc.xpath('/html/body/div[6]/div[2]/div[1]/ul/li[4]')[0].text[1:-2])
        estate.price = float(doc.xpath('/html/body/div[6]/div[2]/div[1]/ul/li[2]/span')[0].text)
        estate.facing = doc.xpath('/html/body/div[6]/div[2]/div[2]/ol/li[2]')[0].text.split('：'.decode('utf8'))[1]
        estate.in_sale = True
        features = [f.text for f in doc.xpath('/html/body/div[5]/ol/label')]
        if '免税'.decode('utf8') in features:
            estate.duty_free = True
        if '学区房'.decode('utf8') in features:
            estate.edu_district = True
        print estate.community.desc, estate.desc, estate.price, estate.area
    estate.updated = True
    estate.save()

def update_estate_detail_pool_worker(estate):
    try:
        update_estate_detail(estate)
    except KeyboardInterrupt:
        pass
