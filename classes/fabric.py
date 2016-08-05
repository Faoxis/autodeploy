# coding: utf-8
import os
from settings.default_settings import *
# from config.pasrser import JsonParser
# from fabric.api import run, env, cd, roles


class Fabric(object):

    def __init__(self):
        self.git_path = REPOSITORY

        self.git_branch = BRANCH

        self.git_branch = 'master'




    # def initProject
    #     print(roledefs['production'])
    #
    # # Списком можно перечислить несколько серверов, которые у вас считаются "продакшеном"
    # env.roledefs['production'] = ['sebuntu-1@192.168.56.101:22']
    # env.roledefs['test'] = ['samojlov@1']
    #
    # # Параметры, которые будут нужны для инициализации
    # #   Путь до папки с проектом
    # #   Логин
    # #   Хост
    # #   Порт
    # #   Название ветки
    #
    # git_path = 'https://github.com/faoxis/PythonBasicAndApplication.git'
    #
    # def production_env():
    #     """Окружение для продакшена"""
    #     env.key_filename = [os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')]  # Локальный путь до файла с ключами
    #     env.user = env.roledefs['production'][0].split('@')[0]  # На сервере будем работать из под пользователя
    #     env.password = 'njkelfrjq'
    #     root = '/home/sebuntu-1/work/fabtest/'
    #     run('mkdir -p {}'.format(root))
    #     env.project_root = root  # Путь до каталога проекта (на сервере)
    #     env.python = os.path.join(os.environ['HOME'], 'myprojects/python/fabtest/venv/bin', 'python')
    #     env.pip = os.path.join(os.environ['HOME'], 'myprojects/python/fabtest/venv/bin', 'pip')
    #
    # @roles('production')
    # def init_production():
    #     production_env()
    #     with cd(env.project_root):
    #         run('git init')
    #         run('git remote rm origin')
    #         run('git remote add origin {git_url}'.format(git_url=git_path))
    #         run('echo {password} | sudo -S apt-get -y install virtualenv'.format(password=env.password))
    #         run('virtualenv venv')
    #
    # @roles('production')
    # def deploy_production():
    #     production_env()  # Инициализация окружения
    #     with cd(env.project_root):  # Заходим в директорию с проектом на сервере
    #         run('git pull {branch} {fetch}'.format(branch='origin', fetch='master'))  # Пуляемся из репозитория
    #
    # @roles('production')
    # def pip_install():
    #     production_env()
    #     run('{pip} install --upgrade -r {filepath}'.format(pip=env.pip,
    #                                                        filepath=os.path.join(env.project_root, 'requirements.txt')))

if __name__ == '__main__':
    test_fabric = Fabric()
    # production_parser = JsonParser('production.json')
    # production_server = Fabric(productionParser)