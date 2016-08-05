# coding: utf-8
import os
from fabric.api import run, env, cd, roles
from settings.default_settings import *
from settings.secret_settings import *

# Списком можно перечислить несколько серверов, которые у вас считаются "продакшеном"
env.roledefs[SERVER] = [USER + '@' + HOST + ':' + PORT]


def production_env():
    """Окружение для продакшена"""
    env.key_filename = PATH_KEY
    env.user = USER  # На сервере будем работать из под пользователя
    env.password = PASSWORD
    root = PATH
    run('mkdir -p {}'.format(root))
    env.project_root = root  # Путь до каталога проекта (на сервере)
    env.python = os.path.join(PATH, '/venv/bin/python')
    env.pip = os.path.join(PATH, 'myprojects/python/fabtest/venv/bin/pip')


@roles('production')
def init_production():
    production_env()
    with cd(env.project_root):
        run('git init')
        run('git remote rm origin')
        run('git remote add origin {git_url}'.format(REPOSITORY))
        run('echo {password} | sudo -S apt-get -y install virtualenv'.format(password=PASSWORD))
        run('virtualenv venv')


@roles('production')
def deploy_production():
    production_env()  # Инициализация окружения
    with cd(env.project_root):  # Заходим в директорию с проектом на сервере
        run('git pull {branch} {fetch}'.format(branch='origin', fetch='master'))  # Пуляемся из репозитория


@roles('production')
def pip_install():
    production_env()
    run('{pip} install --upgrade -r {filepath}'.format(pip=env.pip,
                                                       filepath=os.path.join(env.project_root, 'requirements.txt')))




