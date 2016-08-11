# coding: utf-8
import yaml
from fabric.api import env, puts

from fab.serverssh import ServerSSH

# Функция для перебора всех хостов в yaml-файле
def _get_hosts(filename):
    with open(filename) as f:
        config = yaml.load(f.read())
        for host in config['HOSTS']:
            yield host

# Функция для вывода собщения об обязательном входном параметре
def _puts_not_yaml_message(func_name):
    puts('Enter path to yaml file like that:')
    puts('fab {func_name}:production.yaml'.format(func_name=func_name))


# ---------------------------- Инициализация окружения ---------------------------------------- #
def init(yaml_file=None, service=None):
    if not yaml_file:
        _puts_not_yaml_message('init')
        return

    try:
        before_init()
    except NameError:
        pass

    hosts = _get_hosts(yaml_file)
    try:
        while True:
            host = next(hosts)
            server = ServerSSH(yaml_file, host)
            server.delete_dir()
            server.create_dir()
            server.do('sudo apt-get install git')
            server.init()
            server.pip_install_requirements()
            if service:
                server.control_service(service=service, action='start')
            else:
                server.control_service(action='start')
            # if not service:
            #     raise Exception('My exception here!')
    except StopIteration:
        pass

    try:
        after_init()
    except NameError:
        pass
# -------------------------------------------------------------------------------------------------- #

# -------------------------------- Обовление окружения --------------------------------------------- #
def deploy(yaml_file=None, service=None):
    if not yaml_file:
        _puts_not_yaml_message('deploy')
        return

    try:
        before_deploy()
    except NameError:
        pass

    hosts = _get_hosts(yaml_file)
    try:
        while True:
            host = next(hosts)
            server = ServerSSH(yaml_file, host)
            server.deploy()
            server.venv_update()
            server.pip_install_requirements()
            if service:
                server.control_service(service=service, action='restart')
            else:
                server.control_service(action='restart')
    except StopIteration:
        pass

    try:
        after_deploy()
    except NameError:
        pass
# -------------------------------------------------------------------------------------------------- #


# ------------------------------------ Откат окружения --------------------------------------------- #
def rollback(yaml_file=None, service=None, hash=None):
    if not yaml_file:
        _puts_not_yaml_message('rollback')
        return

    try:
        before_rollback()
    except NameError:
        pass

    hosts = _get_hosts(yaml_file)
    try:
        while True:
            host = next(hosts)
            server = ServerSSH(yaml_file, host)
            server.rollback(hash)
            server.venv_update()
            server.pip_install_requirements()
            if service:
                server.control_service(service=service, action='restart')
            else:
                server.control_service('restart')

    except StopIteration:
        pass

    try:
        after_rollback()
    except NameError:
        pass
# -------------------------------------------------------------------------------------------------- #



