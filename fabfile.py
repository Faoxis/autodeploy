from fablib import init, deploy, rollback
from fab.serverssh import ServerSSH
from fabric.api import puts


def before_init():
    server = ServerSSH(yaml_file=yaml_file)
    server.do('touch something.txt')

import fablib
fablib.before_init = before_init

def after_init():
    puts('hello')



