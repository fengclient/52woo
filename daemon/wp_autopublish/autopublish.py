#coding=utf-8
'''
Created on 2013-3-30

@author: fengclient
'''
import os
import sys
from argparse import ArgumentParser
from publish import publish
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from wantu_crawler import wantudal

def quickpost(count):
    rows = wantudal.get_available_rows(count)
    for row in rows:
        postid = publish(row.savedpath, row.description, row.description)
        if postid:
            wantudal.set_published(row.url)
            print '[row_id:%d] is published as [post_id:%s]' % (row.id, postid)
        else:
            print '[row_id:%d] is failed to be published' % (row.id)

if __name__ == '__main__':
    parser = ArgumentParser(description='auto publisher')
    parser.add_argument('count', nargs='?', type=int, help='count of new posts')
    ns = parser.parse_args()
    if ns.count:
        quickpost(ns.count)
    else:
        parser.print_help()
    
