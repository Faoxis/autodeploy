# coding: utf-8
import yaml
from fabric.api import puts

from classes.serverssh import ServerSSH

before_init = []
after_init = []
before_deploy = []
after_deploy = []
before_rollback = []
after_rollback = []


# Генератор для перебора всех хостов в yaml-файле
def _get_hosts(filename):
    with open(filename) as f:
        config = yaml.load(f.read())
        return config['hosts']


# Функция для вывода собщения об обязательном входном параметре
def _puts_not_yaml_message(func_name):
    puts('Enter path to yaml file like that:')
    puts('fab {func_name}:production.yaml'.format(func_name=func_name))


# ---------------------------- Инициализация окружения ---------------------------------------- #
def init(yaml_file='config/production.yaml', service=None):
    if not yaml_file:
        _puts_not_yaml_message('init')
        return

    hosts = _get_hosts(yaml_file)
    for host in hosts:
        server = ServerSSH(yaml_file, host)
        server.create_dir()

        for f in before_init:
            server.do(f)

        server.run('sudo apt-get install git')
        server.init()
        server.pip_install_requirements()
        if service:
            server.control_service(service=service, action='start')
        else:
            server.control_service(action='start')
        server.run_migrate_command()

        for f in after_init:
            server.do(f)
# -------------------------------------------------------------------------------------------------- #


# -------------------------------- Обовление окружения --------------------------------------------- #
def deploy(yaml_file='config/production.yaml', service=None):
    if not yaml_file:
        _puts_not_yaml_message('deploy')
        return

    hosts = _get_hosts(yaml_file)
    for host in hosts:
        server = ServerSSH(yaml_file, host)

        for f in before_deploy:
            server.do(f)

        server.deploy()
        server.pip_install_requirements()
        if service:
            server.control_service(service=service, action='restart')
        else:
            server.control_service(action='restart')
        server.run_migrate_command()

        for f in after_deploy:
            server.do(f)
# -------------------------------------------------------------------------------------------------- #


# ------------------------------------ Откат окружения --------------------------------------------- #
def rollback(yaml_file='config/production.yaml', service=None, commit_hash=None):
    if not yaml_file:
        _puts_not_yaml_message('rollback')
        return

    hosts = _get_hosts(yaml_file)
    for host in hosts:
        server = ServerSSH(yaml_file, host)

        for f in before_rollback:
            server.do(f)

        server.rollback(commit_hash)
        server.pip_install_requirements()

        if service:
            server.control_service(service=service, action='restart')
        else:
            server.control_service('restart')
        server.run_migrate_command()

        for f in after_rollback:
            server.do(f)
# -------------------------------------------------------------------------------------------------- #


# --------------------------------- Удаление проекта целиком с сервера ----------------------------- #
def clear(yaml_file='config/production.yaml'):
    hosts = _get_hosts(yaml_file)
    for host in hosts:
        server = ServerSSH(yaml_file, host)
        server.delete_dir()
# -------------------------------------------------------------------------------------------------- #
