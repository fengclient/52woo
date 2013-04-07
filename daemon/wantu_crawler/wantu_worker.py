#coding=utf-8
'''
Created on 2013-3-31

@author: fengclient
'''
import sys
import os
import json
import traceback
import logging
from urllib2 import HTTPError
from urllib import urlencode
from urlparse import urlsplit, urlunsplit, urlparse, urljoin, parse_qs, SplitResult
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
from gearman.constants import *
from gearman.client import GearmanClient
from gearman.worker import GearmanWorker
from common import JSONDataEncoder, md5sum
from pyhttplib import httplib
import config
import wantudal

#site-specific parsing logic
def is_album_index(url):
    return True if urlparse(url)[2].startswith(u'/search/album') else False

def is_album_page(url):
    return True if urlparse(url)[2].startswith(u'/album') else False

def is_detail_page(url):
    return True if urlparse(url)[2].startswith(u'/detail') else False

def is_pic_page(url):
    return True if urlparse(url)[2].endswith(u'.jpg') else False

def find_next_indexes(soup):
    '''
    next page for an album index or an album page
    '''
    indexes = soup.findAll('a', 'pix-navi-page')
    urls = []
    if indexes:
        max_p = max([int(tag.string) for tag in indexes if tag.string.isdigit()])
        result = urlsplit(httplib.html_unescape(indexes[0]['href']))
        query_dict = parse_qs(result.query)
        for p in range(1, max_p + 1):
            query_dict['p'] = p
            result = SplitResult(result.scheme, result.netloc, result.path,
                                 urlencode(query_dict, doseq=True), result.fragment)
            urls.append(result.geturl())
    return urls

def get_album_from_index(soup):
    return [a['href'] for a in soup.findAll('a', 'pix-set-link')]

def get_detail_from_album(soup, url):
    '''
    <script id="pix-waterfall-data" type="application/json">
    {
      "success": 1,
      "msg": "",
      "data": {
             "waterfall": [
             {"picPath":"http://img04.taobaocdn.com/imgextra/i4/15896018282515631/T1DEjEXjBcXXXXXXXX_!!281385896-0-pix.jpg",
             "id":18742273,"link":"/detail/18742273?wantu_c=chongwu&u=52511109",
             "height":314,"width":200,"desc":"",
             "info":{"type":1,"nick":"蓝牙月","albumName":"&#23456;&#29289;","albumId":17327808,
                     "userId":52511109,"avatar":"i4/T1oM4_Xh8xXXartXjX.gif",
                     "time":"2012-08-16 17:01:05","userLink":"/52511109",
                     "albumLink":"/album/17327808?u=52511109"},
             "like":0,"collect":0,"comments":0,"picType":0,"favStatus":false}]
          }
    }
    </script>
    '''
    #TODO: do we need a small picture? a.img['src']
    waterfalls = json.loads(soup.find('script', id='pix-waterfall-data').string)['data']['waterfall']
    return [urljoin(url, p['link']) for p in waterfalls]

def get_content_from_detail(soup, url):
    '''
    <script id="pix-json-set-info" type="application/json">
    {
        "albumId": 17327808,
        "likeStatus": false,
        "categoryId":"11",
        "categoryEname":"chongwu",
        "prevAlbumUrl": "",
        "nextAlbumUrl": "/detail/52085246?u=60786793" 
    }
    </script>
    '''
    picId = urlsplit(url).path.split('/')[-1]
    userId = parse_qs(urlsplit(url).query)['u'][0]
    albumId = json.loads(soup.find('script', id='pix-json-set-info').string)['albumId']
    ajax_url = 'http://wantu.taobao.com/ajax/PicDetailAjax.do?picId=%s&userId=%s&albumId=%s&t=1365154666759&_method=read'
    ajax_url = ajax_url % (picId, userId, albumId)
    resp = json.loads(httplib.urlopen(ajax_url)[2].decode('gbk'))
    picture = resp['data']['models'][0]['picPath']
    description = httplib.html_unescape(resp['data']['models'][0]['desc'])
    return (picture, description)

#used for pipeline work
gm_client = GearmanClient([config.job_server])
gm_client.data_encoder = JSONDataEncoder

def submit_html_job(url):
    func_name = 'worker_process_html'
    job_req = gm_client.submit_job(func_name, url, unique=md5sum(url),
                                 background=True, wait_until_complete=False)
    return job_req.job.unique

def submit_pic_job(url):
    func_name = 'worker_process_pic'
    job_req = gm_client.submit_job(func_name, url, unique=md5sum(url),
                                 background=True, wait_until_complete=False)
    return job_req.job.unique

def worker_process_html(gearman_worker, gearman_job):
    url = gearman_job.data
    if wantudal.is_processed(url):
        logging.debug('%s is skipped as it was processed already' % (url))
        return
    logging.debug('processing %s' % (url))
    #this web is encoded by gbk
    html_doc = httplib.urlopen(url)[2].decode('gbk')
    soup = BeautifulSoup(html_doc, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
    if is_album_index(url):
        albums = get_album_from_index(soup)
        logging.debug('%d albums are found' % (len(albums)))
        more_indexes = find_next_indexes(soup)
        logging.debug('%d sub indexes are found' % (len(more_indexes)))
        wantudal.save_url(url, pagetype=wantudal.PageType.AlbumIndex, isfinished=1)
        for album in albums:
            wantudal.save_url(album, pagetype=wantudal.PageType.AlbumPage, referrerurl=url, isfinished=0)
            submit_html_job(album)
        for index in more_indexes:
            wantudal.save_url(index, pagetype=wantudal.PageType.AlbumIndex, referrerurl=url, isfinished=0)
            submit_html_job(index)
    elif is_album_page(url):
        details = get_detail_from_album(soup, url)
        logging.debug('%d details are found' % (len(details)))
        more_indexes = find_next_indexes(soup)
        logging.debug('%d sub indexes are found' % (len(more_indexes)))
        wantudal.save_url(url, pagetype=wantudal.PageType.AlbumPage, isfinished=1)
        for detail in details:
            wantudal.save_url(detail, pagetype=wantudal.PageType.DetailPage, referrerurl=url, isfinished=0)
            submit_html_job(detail)
        for index in more_indexes:
            wantudal.save_url(index, pagetype=wantudal.PageType.AlbumPage, referrerurl=url, isfinished=0)
            submit_html_job(index)
    elif is_detail_page(url):
        pic, description = get_content_from_detail(soup, url)
        wantudal.save_url(url, pagetype=wantudal.PageType.DetailPage, isfinished=1)
        wantudal.save_url(pic, pagetype=wantudal.PageType.PicturePage, referrerurl=url, description=description, isfinished=0)
        submit_pic_job(pic)
    else:
        logging.debug('unknown resource')

def worker_process_pic(gearman_worker, gearman_job):
    url = gearman_job.data
    if wantudal.is_processed(url):
        logging.debug('%s is skipped as it was processed already' % (url))
        return
    logging.debug('processing %s' % (url))
    try:
        content = httplib.urlopen(url)[2]
    except HTTPError, e:
        logging.debug('http error: %s' % (e.code))
        return
    name = urlparse(url).path.split('/')[-1]
    filepath = os.path.join(config.root_dir)
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    filepath = os.path.join(filepath, name)
    with open(filepath, 'wb') as f:
        f.write(content)
    logging.debug('%s is saved' % (filepath))
    wantudal.save_url(url, pagetype=wantudal.PageType.PicturePage, savedpath=filepath, isfinished=1)
    
class SafeGearmanWorker(GearmanWorker):
    '''
    copied from http://packages.python.org/gearman/1to2.html#worker
    worker with exception logging and JSON encoder
    '''
    data_encoder = JSONDataEncoder
    
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    fh = logging.FileHandler(config.log_filename)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
        
    strm_out = logging.StreamHandler(sys.__stdout__)
    strm_out.setFormatter(formatter)    
    logger.addHandler(strm_out)

    def on_job_exception(self, current_job, exc_info):
        logging.debug("Job failed, CAN stop last gasp GEARMAN_COMMAND_WORK_FAIL")
        logging.error('exception: %s' % (traceback.format_exception(*exc_info)))
        logging.debug('%s,type:%s' % (self, super(SafeGearmanWorker, self))) 
        return super(SafeGearmanWorker, self).on_job_exception(current_job, exc_info)
    
    def after_poll(self, any_activity):
        logging.debug('after_pull,any_activity=%s' % (any_activity))
        return True

if __name__ == '__main__':
    worker = SafeGearmanWorker([config.job_server])
    worker.set_client_id('wantu_worker_client_id')
    worker.register_task('worker_process_html', worker_process_html)
    worker.register_task('worker_process_pic', worker_process_pic)
    worker.work()
