#!/usr/bin/python3
""" a Fabric script (based on the file 1-pack_web_static.py) that distributes..
    ..an archive to your web servers, using the function do_deploy: """


from fabric.api import *
from datetime import datetime
from os.path import exists

# Set the list of servers to deploy to
# <IP web-01>, <IP web-02>
env.hosts = ['3.83.238.226', '34.202.234.56']  
env.user = 'ubuntu'

def do_pack():
    """ Fabric script that generates a .tgz archive from the contents of the...
    ...web_static folder """
    local("sudo mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(date)
    result = local("sudo tar -cvzf {} web_static".format(archive_path))
    if result.succeeded:
        return archive_path
    else:
        return None

def do_deploy(archive_path):
    """ distributes an archive to my web servers
    """
    # Returns False if the file at archive_path doesnt exist
    if exists(archive_path) is False:
        return False  
    # Extract the file name and the name without extension from the archive path
    filename = archive_path.split('/')[-1]

    no_tgz = '/data/web_static/releases/' + "{}".format(filename.split('.')[0])
    
    tmp = "/tmp/" + filename

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Uncompress the archive to the folder /data/web_static/releases/
        run("sudo mkdir -p {}/".format(no_tgz))
        
        # Uncompress the archive to the release directory on the remote servers
        run("sudo tar -xzf {} -C {}/".format(tmp, no_tgz))

        # Delete the archive from the web server
        run("sudo rm {}".format(tmp))
        run("sudo mv {}/web_static/* {}/".format(no_tgz, no_tgz))
        run("sudo rm -rf {}/web_static".format(no_tgz))

        # Delete the symbolic link /data/web_static/current from the web server
        run("sudo rm -rf /data/web_static/current")

        # Create a new the symbolic link /data/web_static/current on the web server
        run("sudo ln -s {}/ /data/web_static/current".format(no_tgz))
        
       # Return True if all operations completed successfully return True

    except:
        return False
