import sys
import fablib
from fablib import init, deploy, rollback, clear
from fab.serverssh import ServerSSH
from fabric.api import puts


# def before_init():
#     return 'echo "Hello there" >> hello.txt'

def after_init():
    return 'echo "Bye there" >> hello.txt'


fablib.before_init.append(lambda: 'echo "Hello from init" >> hello.txt')
fablib.before_deploy.append(lambda: 'echo "Hello from deploy" >> hello.txt')
fablib.before_rollback.append(lambda: 'echo "Hello from rollback" >> hello.txt')

fablib.after_init.append(lambda: 'echo "Bye from init" >> bye.txt')
fablib.after_deploy.append(lambda: 'echo "Bye from deploy" >> bye.txt')
fablib.after_rollback.append(lambda: 'echo "Bye from rollback" >> bye.txt')


