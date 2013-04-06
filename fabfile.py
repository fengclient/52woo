#!/usr/bin/python
from fabric.api import *
import os

env.hosts = ['xiaoftang@192.168.111.130']

user = 'xiaoftang'
package_name = 'wantu.tar.gz'

def wantu():
    deploy('daemon')

def deploy(path='*'):
    parent = os.path.dirname(env.real_fabfile)
    local_path = parent
    remote_path = '/data/wantu'
    with lcd(local_path):
        local('rm %s -f' % (package_name))
        local('tar -czf %s %s' % (package_name, path))
        put(package_name, '/tmp/%s' % (package_name))
    with cd(remote_path):
        sudo('tar -xzf /tmp/%s' % (package_name))
        sudo('chown xiaoftang:xiaoftang %s -R -f' % (remote_path))

def restart_wantu_workers():
    #sudo('service httpd wantu_workers')
    pass

if __name__ == "__main__":
    wantu()
