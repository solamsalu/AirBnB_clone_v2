#!/usr/bin/python3
"""Fabric script that creates and distributes an archive to web servers"""

from os import path
from fabric.api import *

env.hosts = ['3.83.238.226', '34.202.234.56']


def do_deploy(archive_path):
    """Upload and deploy"""
    if not path.exists(archive_path):
        return False
    try:
        # path.exists(archive_path):
        arc_tgz = archive_path.split('/')
        arg_save = arc_tgz[1]
        arc_tgz = arc_tgz[1].split('.')
        arg_tgz = arc_tgz[0]
        put(archive_path, '/tmp')
        direct = '/data/web_static/release/{}'.format(arc_tgz)
        tmp = '/tmp/{}'.format(arg_save)
        run('mkdir -p {}'.format(direct))
        run('tar -xvzf {} -c {}'.format(tmp, direct))
        run('rm {}'.format(tmp))
        run('mv {}/web_static/* {}'.format(direct, direct))
        run('rm -rf {}/web_static/*'.format(direct))
        run('rm -rf /data/web_static/current')
        run('ln -sf {} /data/web_static/current'.format(direct))
        run('sudo service nginx restart')
        return True
    except Exception:
        return False
