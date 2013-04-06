#coding=utf-8
'''
Created on 2012-5-20

@author: fengclient
'''
import sys
from gearman.client import GearmanClient
from gearman.worker import GearmanWorker
from gearman.job import GearmanJob
from gearman.constants import *
from common import JSONDataEncoder
import config

def check_request_status(job_request):
    if job_request.complete:
        print "Job %s finished!  Result: %s - %s" % (job_request.job.unique, job_request.state, job_request.result)
    elif job_request.timed_out:
        print "Job %s timed out!" % job_request.job.unique
    elif job_request.state == JOB_UNKNOWN:
        print "Job %s connection failed!" % job_request.job.unique

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'usage: work_and_move_out.py dirpath'
        sys.exit(-1)
    else:
        gm_client = GearmanClient([config.job_server])
        gm_client.data_encoder = JSONDataEncoder
        job_req = gm_client.submit_job('worker_process_html', sys.argv[1])
        print sys.argv[1], 'is submitted'
        check_request_status(job_req)
    
