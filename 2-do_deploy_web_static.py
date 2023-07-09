#!/usr/bin/python3
"""
Distributes an archive to my web servers,
using the function do_deploy
"""
from fabric.api import *
from datetime import datetime
from os.path 

env.hosts = ['52.91.150.219', '54.196.50.77']
env.user = 'ubuntu'

def do_pack():
    """generates a .tgz archive from the contents of the web_static folder
    """
    local("sudo mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(date)
    result = local("sudo tar -cvzf {} web_static".format(archive_path))
    if result.succeeded:
        return archive_path
    else:
        """ return none if not succed """
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
