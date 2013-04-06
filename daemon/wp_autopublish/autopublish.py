#coding=utf-8
'''
Created on 2013-3-30

@author: fengclient
'''

import os
import mimetypes
from uuid import uuid4
from wordpress_xmlrpc import Client, WordPressPost, WordPressMedia
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts

rpc_service_url = r'http://www.52woo.com/xmlrpc.php'
user = 'admin'
password = 'User@123'

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
    '''
    attachment = upload(pic)
    wp_client = Client(rpc_service_url, user, password)
    post = WordPressPost()
    post.title = title
    post.content = '%s\n\n<a href="%s"><img class="alignnone size-full wp-image-%s" alt="%s" src="%s" /></a>' % (content, attachment["url"], attachment["id"], attachment["file"], attachment["url"])
    #post.tags='test, test2'
    #post.categories=['pet','picture']
    post.thumbnail = attachment["id"]
    #change status to publish
    post.id = wp_client.call(posts.NewPost(post))
    post.post_status = 'publish'
    wp_client.call(posts.EditPost(post.id, post))
    return post.id

def getPost(_id):
    wp_client = Client(rpc_service_url, user, password)
    post = wp_client.call(posts.GetPost(_id, WordPressPost.definition.keys()))
    return post
    
if __name__ == '__main__':
    post_id = publish(r'C:\Users\fengclient\Pictures\a.png', 'test title', 'test content')
    print "post_id:", post_id
    print getPost(post_id).content
    pass
