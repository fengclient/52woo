#coding=utf-8
'''
Created on 2012-5-20

@author: fengclient
'''
import sys
from argparse import ArgumentParser
from gearman.client import GearmanClient
from gearman.worker import GearmanWorker
from gearman.job import GearmanJob
from gearman.constants import *
from common import JSONDataEncoder
from wantudal import get_unfinished_rows
import config

def check_request_status(job_request):
    if job_request.complete:
        print "Job %s finished!  Result: %s - %s" % (job_request.job.unique, job_request.state, job_request.result)
    elif job_request.timed_out:
        print "Job %s timed out!" % job_request.job.unique
    elif job_request.state == JOB_UNKNOWN:
        print "Job %s connection failed!" % job_request.job.unique

_gm_client=None

def submit(url):
    gm_client = GearmanClient([config.job_server])
    gm_client.data_encoder = JSONDataEncoder
    job_req = gm_client.submit_job('worker_process_html', url)
    print ns.url[0], 'is submitted'
    return job_req

if __name__ == '__main__':
    parser = ArgumentParser(description='client to control wantu workers')
    parser.add_argument('-c', '--continue', dest='_continue', action='store_true', help='continue to process unfinished url by resubmit them')  
    parser.add_argument('-u', '--url', nargs=1, help='the specified url to be submitted')
    ns = parser.parse_args()
   
    if ns._continue:
        rows=get_unfinished_rows(100)
        for row in rows:
            submit(row.url)
    elif ns.url:
        job_req = gm_client.submit_job('worker_process_html', ns.url[0])
        check_request_status(job_req)
    else:
        parser.print_help()
