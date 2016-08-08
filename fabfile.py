# coding: utf-8
import os

from fabric.api import run, env, cd, roles
from settings.default_settings import *
from settings.secret_settings import *

# Списком можно перечислить несколько серверов, которые у вас считаются "продакшеном"
env.roledefs[SERVER] = [USER + '@' + HOST + ':' + str(PORT)]


def change_server_state(action='restart'):
    run('echo {password} | sudo -S service {server_name} {action}'.format(server_name=WORK_SERVER,
                                                                          password=PASSWORD,
                                                                          action=action))
    # sudo('service {server_name} {action}'.format(server_name=WORK_SERVER, action=action),
    #      user=USER, shell=False)


def do(action):
    production_env()
    with cd(env.project_root):
        run(action)


def pip(action):
    production_env()
    with cd(env.project_root):
        run('{pip} {action}'.format(pip=env.pip, action=action))


def python(action):
    production_env()
    with cd(env.project_root):
        run('{python} {action}'.format(python=env.python, action=action))


def production_env():
    """Окружение для продакшена"""
    env.key_filename = PATH_KEY
    env.user = USER  # На сервере будем работать из под пользователя
    env.password = PASSWORD
    env.project_root = PATH  # Путь до каталога проекта (на сервере)
    env.python = PYTHON
    env.pip = PIP


def venv_update():
    production_env()
    with cd(env.project_root):
        run('rm -rf venv')
        run('virtualenv venv')
        run('{pip} install -r {requirements}'.format(pip=env.pip, requirements=VENV_REQUIREMENTS))


@roles(SERVER)
def init():
    run('mkdir -p {}'.format(PATH))
    production_env()
    with cd(env.project_root):
        run('git init')
        # run('git remote set-url origin {repository}'.format(repository=REPOSITORY+'.git'))
        run('git remote add origin {repository}'.format(repository=REPOSITORY))
        run('echo {password} | sudo -S apt-get -y install virtualenv'.format(password=PASSWORD))
        run('virtualenv venv')


@roles(SERVER)
def change():
    production_env()
    with cd(env.project_root):
        run('git remote set-url origin {repository}'.format(repository=REPOSITORY))


@roles(SERVER)
def deploy():
    production_env()  # Инициализация окружения
    with cd(env.project_root):  # Заходим в директорию с проектом на сервере
        run('git pull {branch} {fetch}'.format(branch='origin', fetch='master'))  # Пуляемся из репозитория
        control_service(action='restart')


@roles(SERVER)
def rollback():
    production_env()
    with cd(env.project_root):
        run('git reset --hard HEAD^')
        control_service(action='restart')



# @roles(SERVER)
# def create_dir():
# do('mkdir something')
# python('hello.py')
# pip('install SQLAlchemy')


@roles(SERVER)
def control_service(service=WORK_SERVER, action='restart'):
    production_env()
    run('echo {password} | sudo -S service {server_name} {action}'.format(server_name=service,
                                                                          password=PASSWORD,
                                                                          action=action))



