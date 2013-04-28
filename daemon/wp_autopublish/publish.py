#coding=utf-8
'''
Created on 2013-3-30

@author: fengclient
'''

import os
import sys
import mimetypes
from random import Random
from argparse import ArgumentParser
from uuid import uuid4
from wordpress_xmlrpc import Client, WordPressPost, WordPressMedia, WordPressUser
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts, users
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

rpc_service_url = r'http://www.52woo.com/xmlrpc.php'
user = 'admin'
password = 'User@123'

account_ids = range(1,8)
r=Random()

def upload(pic):
    (_ , ext) = os.path.splitext(pic)
    wp_client = Client(rpc_service_url, user, password)
    data = {'name':str(uuid4()) + ext, 'type':mimetypes.guess_type(pic)[0]}
    with open(pic, 'rb') as img:
        data['bits'] = xmlrpc_client.Binary(img.read())
    rsp = wp_client.call(media.UploadFile(data))
    return rsp

def publish(pic, title, content):
    '''
    publish a post and set to open to comment and ping(trackback)
    '''
    attachment = upload(pic)
    wp_client = Client(rpc_service_url, user, password)
    post = WordPressPost()
    post.title = title
    post.content = "%s\n\n<a href='%s'><img class='alignnone size-full wp-image-%s' alt='%s' src='%s' /></a>" % (content, attachment['url'], attachment['id'], attachment['file'], attachment['url'])
    #post.tags='test, test2'
    #post.categories=['pet','picture']
    post.thumbnail = attachment['id']
    #change status to publish
    post.id = wp_client.call(posts.NewPost(post))
    post.post_status = 'publish'
    post.comment_status = 'open'
    post.ping_status = 'open'
    post.user = account_ids[r.randint(0, len(account_ids)-1)]
    wp_client.call(posts.EditPost(post.id, post))
    return post.id

def getPost(_id):
    wp_client = Client(rpc_service_url, user, password)
    post = wp_client.call(posts.GetPost(_id, WordPressPost.definition.keys()))
    return post

if __name__ == '__main__':
    #parser = ArgumentParser(description='auto publisher')
    #parser.add_argument('count', nargs='?', type=int, help='count of new posts')
    #ns = parser.parse_args()
    #if ns.count:
    #    quickpost(ns.count)
    #else:
    #    parser.print_help()
    #p1 = getPost(4)
    #p2 = getPost(177)
    #import pdb;pdb.set_trace()
    publish(r'/cygdrive/c/Users/fengclient/Pictures/a.png','test','helloworld')
    pass
    