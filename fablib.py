# coding: utf-8
import yaml
from fabric.api import env, run

from fab.serverssh import ServerSSH

env.hosts = []


def before_init():
    pass


def after_init():
    pass


def before_deploy():
    pass


def after_deploy():
    pass


def before_rollback():
    pass


def after_rollback():
    pass


def get_hosts(filename):
    with open(filename) as f:
        config = yaml.load(f.read())
        for host in config['HOSTS']:
            yield host
            # env.hosts += [host]


def init(service=None):
    before_init()
    hosts = get_hosts(env.rcfile)
    try:
        while True:
            host = next(hosts)
            server = ServerSSH(env.rcfile, host)
            server.create_dir()
            server.do('sudo apt-get install gcc')
            server.do('sudo apt-get install build-essential autoconf libtool pkg-config python-opengl python-imaging ' +
                      'python-pyrex python-pyside.qtopengl idle-python2.7 qt4-dev-tools qt4-designer libqtgui4 ' +
                      'libqtcore4 libqt4-xml libqt4-test libqt4-script libqt4-network libqt4-dbus python-qt4 ' +
                      'python-qt4-gl libgle3 python-dev libxml2-dev libxslt1-dev libevent-dev')
            server.init()
            server.pip_install_requirements()
            if not service:
                server.control_service(service=service, action='start')
    except StopIteration:
        pass
    after_init()


def deploy(service=None):
    before_deploy()
    server = ServerSSH(env.rcfile)
    server.deploy()
    if not service:
        server.control_service(service=service, action='restart')
    after_deploy()


def rollback(service=None):
    before_rollback()
    server = ServerSSH(env.rcfile)
    server.rollback()
    if not service:
        server.control_service(service=service, action='restart')
    after_rollback()
