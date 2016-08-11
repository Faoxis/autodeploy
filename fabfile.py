import fablib

from fab.serverssh import ServerSSH
from fablib import init, deploy, rollback
from fabric.api import puts



def before_init():
    server = ServerSSH(yaml_file)

def after_init():
    puts('hello')


