from fabric.state import env

from fablib import init, deploy, rollback

# fablib.before_init = lambda: 'Hello there'

def before_init():
    return 'Hello there'


