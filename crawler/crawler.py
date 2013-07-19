#!/usr/bin/python2
# -*- coding: utf8 -*-

CITY = 'beijing'
BASE_URL='http://%s.homelink.com.cn/' % CITY
ESTATE_URL = BASE_URL + 'ershoufang/%s.shtml'
DIST_SFX = 'ershoufang/%s/'
PAGE_SFX = 'pg%d/'
COMM_SFX = '%s/xq/'
ESTATE_SFX = 'ershoufang/%s.shtml'

NUM_WORKERS = 3
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
    if encoding:
        raw = raw.decode(encoding)
    return x.document_fromstring(raw)

def subdist_from_hlid(hlid):
    from models import Subdistrict
    # does not handle ObjectDoesNotExist excption here
    return Subdistrict.objects.get(hlid=hlid)

def subdist_from_desc(desc):
    from models import Subdistrict
    return Subdistrict.objects.filter(desc__contains=desc)

def dist_from_hlid(hlid):
    from models import Subdistrict
    # does not handle ObjectDoesNotExist excption here
    return District.objects.get(hlid=hlid)

def dist_from_desc(desc):
    from models import District
    return District.objects.filter(desc__contains=desc)

def mark_need_update(obj):
    from models import Subdistrict
    if 'ALL' == obj:
        obj = Subdistrict.objects.all()
    if '__iter__' in dir(obj):
        for o in obj:
            do_mark_need_update(o)
    else:
        do_mark_need_update(obj)

def do_mark_need_update(dist):
    dist.updated = False
    dist.save()

def do_mark_subdist_need_update(obj):
    obj.updated = False
    obj.save()

def get_estate_count(url):
    doc = doc_from_url(url)
    entries = doc.xpath('/html/body/div[3]/span')
    if len(entries) != 1:
        print 'ERROR:', entries
        return -1
    return int(entries[0].text)

def crawl_estate_in_page_pool_worker(url):
    try:
        return crawl_estate_in_page(url)
    except KeyboardInterrupt, e:
        raise e
    except Exception, e:
        raise e

def crawl_estate_in_page(url):
    from models import RealEstate, Community
    from urllib2 import URLError
    from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
    from MySQLdb import DatabaseError
    try:
        doc = doc_from_url(url)
    except URLError:
        print 'URLError!'
        return
    entries = doc.xpath('//div[@id="listData"]/div')
    ret = 0
    for entry in entries:
        ret += 1
        e = dict()
        c_hlid = entry.xpath('div[2]/ul/li[1]/a/@href')[0][1:-1]
        try:
            e['community'] = Community.objects.get(hlid=c_hlid)
        except ObjectDoesNotExist:
            update_community_detail(c_hlid)
            e['community'] = Community.objects.get(hlid=c_hlid)
        e['hlid'] = entry.xpath('h3/span/a/@href')[0].split('/')[2].split('.')[0]
        # if subdist not found in db, and exception is expected (for now)
        e['subdist'] = subdist_from_hlid(hlid='b' + url.split('/')[4].split('b')[1])
        e['desc'] = entry.xpath('h3/span/a')[0].text
        e['nbedrm'] = int(entry.xpath('div[2]/ul/li[2]/span[1]')[0].text)
        e['nlvnrm'] = int(entry.xpath('div[2]/ul/li[2]/span[2]')[0].text)
        e['area'] = float(entry.xpath('div[2]/ul/li[3]/span')[0].text)
        e['price'] = float(entry.xpath('div[3]/ul/b')[0].text)
        e['floor'], e['facing'], e['decoration'] = entry.xpath('div[2]/p')[0].text.split()[0].split(',')
        e['nvisitor'] = int(entry.xpath('div[4]/span[1]/label')[0].text)
        e['ncomment'] = int(entry.xpath('div[4]/span[2]/label')[0].text)
        e['in_sale'] = True
        features = [f.text.encode('utf8') for f in entry.xpath('div[2]/ol/label')]
        if '免税' in features:
            e['duty_free'] = True
        if '学区房' in features:
            e['edu_district'] = True
        print e['hlid'], e['community'].desc, e['desc'], e['price'], e['area']
        e['updated'] = True
        estate, created = RealEstate.objects.get_or_create(hlid=e['hlid'], defaults=e)
        if not created:
            for k in e:
                setattr(estate, k, e[k])
        try:
            estate.save()
        except DatabaseError:
            try:
                estate.save()
            except DatabaseError:
                from sys import exit
                exit(-1)
            except IntegrityError:
                pass
        except IntegrityError:
            pass
    return ret

def crawl_estate_in_district(dist):
    if '__iter__' in dir(dist):
        for d in dist:
            do_crawl_estate_in_district(d)
    else:
        do_crawl_estate_in_district(dist)

def do_crawl_estate_in_district(dist):
    from multiprocessing import Pool
    from models import District, Subdistrict
    if dist.__class__ is District:
        url = url_from_district(dist)
    elif dist.__class__ is Subdistrict:
        url = url_from_subdistrict(dist)
    else:
        raise TypeError
    n_estates = get_estate_count(url)
    n_pages = (n_estates -1) / ITEM_PER_PAGE + 1
    pool = Pool(NUM_WORKERS)
    # used to be:
    # results = pool.map(crawl_estate_in_page, [url + PAGE_SFX % p for p in range(1, n_pages + 1)])
    p = pool.map_async(crawl_estate_in_page_pool_worker, [url + PAGE_SFX % p for p in range(1, n_pages + 1)])
    try:
        results = p.get(0xFFFF)
    except KeyboardInterrupt:
        pool.terminate()
        results = 0
    n_found = 0
    if results:
        for r in results:
            n_found += r
    print n_estates, '/', n_found
    # attempt to solve 'Too may open files' issue:
    #pool.terminate()
    return n_found == n_estates


def update_estate():
    from models import Subdistrict, RealEstate
    from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
    from time import time
    subdists = Subdistrict.objects.filter(updated=0).order_by('hlid')
    for sd in subdists:
        print sd.dist.desc, sd.desc, sd.hlid
        crawl_estate_in_district(sd)
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

def crawl_estates_detail(dist=None, update=False):
    from models import RealEstate, Subdistrict, District
    from multiprocessing import Pool
    from django.core.exceptions import ObjectDoesNotExist
    
    if not update:
        e = RealEstate.objects.filter(updated=0)
    if '__iter__' in dir(dist): # in case of empty list
        estates = []
        # FIXME: not returning QuerySet!!!
        # FIXME: hence no support for list of dists
        for sd in dist:
            estates += e.filter(subdist=dist)
    elif dist:
        if dist.__class__ == Subdistrict:
            estates = e.filter(subdist=dist)
        elif dist.__class__ == District:
            estates = e.filter(subdist__dist=dist)
        else:
            raise TypeError
    else:
        estates = e
    pool = Pool(NUM_WORKERS)
    p = pool.map_async(update_estate_detail_pool_worker, estates)
    try:
        p.get(0xFFFF)
    except:
        pool.terminate()

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
        features = [f.text.encode('utf8') for f in doc.xpath('/html/body/div[5]/ol/label')]
        if '免税' in features:
            estate.duty_free = True
        if '学区房' in features:
            estate.edu_district = True
        print estate.community.desc, estate.desc, estate.price, estate.area
    estate.updated = True
    estate.save()

def update_estate_detail_pool_worker(estate):
    try:
        update_estate_detail(estate)
    except KeyboardInterrupt, e:
        # TODO: why not raise it?
        pass
