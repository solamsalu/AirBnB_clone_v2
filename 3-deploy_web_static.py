#!/usr/bin/python3
"""
Distributes an archive to my web servers,
using the function deploy
"""
from fabric.api import *
from datetime import datetime
import os

env.hosts = ['52.91.150.219', '54.196.50.77']
env.user = 'ubuntu'


def deploy():
    ''' Deploys archive '''
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)


def do_pack():
    '''
    Generates a tgz archive from the
    contents of the web_static folder
    '''
    try:
        local('sudo mkdir -p versions')
        datetime_format = '%Y%m%d%H%M%S'
        archive_path = 'versions/web_static_{}.tgz'.format(
            datetime.now().strftime(datetime_format))
        local('sudo tar -cvzf {} web_static'.format(archive_path))
        print('web_static packed: {} -> {}'.format(archive_path,
              os.path.getsize(archive_path)))
        return archive_path
    except:
        return None


def do_deploy(archive_path):
    '''
    Deploy archive to web server
    '''
    if not os.path.exists(archive_path):
        return False
    file_name = archive_path.split('/')[1]
    file_path = '/data/web_static/releases/'
    releases_path = file_path + file_name[:-4]
    try:
        put(archive_path, '/tmp/')
        run('sudo mkdir -p {}'.format(releases_path))
        run('sudo tar -xzf /tmp/{} -C {}'.format(file_name, releases_path))
        run('sudo rm /tmp/{}'.format(file_name))
        run('sudo mv {}/web_static/* {}/'.format(releases_path, releases_path))
        run('sudo rm -rf {}/web_static'.format(releases_path))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s {} /data/web_static/current'.format(releases_path))
        print('New version deployed!')
        return True
    except:
        return False
