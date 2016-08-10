# -*- coding: utf-8 -*-
import yaml
import os
from fabric.api import run, env, cd, puts


class ServerSSH(object):
    # В конструктор класса передается объект класса Settings,
    # который содержит в себе все необходимые настройки
    def __init__(self, yaml_file):
        with open(yaml_file) as f:
            yaml_config = yaml.load(f.read())

        # Сразу же необходимо "сказать" библиотеке fabric о создании новой роли
        env.roledefs[yaml_config['SERVER']] = [yaml_config['USER'] + '@' +
                                               yaml_config['HOST'] + ':' +
                                               str(yaml_config['PORT'])]

        # Инициализация окружения
        env.key_filename = yaml_config['PATH_KEY']
        env.user = yaml_config['USER']
        env.password = yaml_config['PASSWORD']
        env.project_root = yaml_config['PATH']

        try:
            env.python = yaml_config['PYTHON']
        except KeyError:
            env.python = os.path.join(env.project_root, 'venv/bin/python')

        try:
            env.pip = yaml_config['PIP']
        except KeyError:
            env.pip = os.path.join(env.project_root, 'venv/bin/pip')

        self.config_server = yaml_config['WORK_SERVER']
        self.repository = yaml_config['REPOSITORY']
        self.path = yaml_config['PATH']
        self.name = yaml_config['SERVER']

    # Создание папки с виртуальным окружением
    def create_dir(self):
        run('mkdir -p {}'.format(self.path))

    def pip_install_requirements(self):
        self.pip('install -r requirements.txt')

    # Метод для изменения состояния какого-либо сервиса
    def control_service(self, action='restart', service=None):
        if service is None:
            service = self.config_server
        run('sudo service {server_name} {action}'.format(server_name=service,
                                                         action=action))
        puts('{service} has been {action}ed'.format(service=service, action=action))

    # Метода для выполнения какой-либо программы внутри корневого каталога с проектом
    def do(self, action):
        with cd(env.project_root):
            run(action)
        puts('{action} is completed'.format(action=action))

    # Методы для выполнения команды "от лица" pip из вируального окружения
    def pip(self, action):
        with cd(env.project_root):
            run('{pip} {action}'.format(pip=env.pip, action=action))

    # Метода для выполнения команды "от лица" python из вируального окружения
    def python(self, action):
        with cd(env.project_root):
            run('{python} {action}'.format(python=env.python, action=action))

    # Подготовка окружения на удаленном компьютере к работе
    def init(self):
        with cd(env.project_root):
            run('git init')
            # run('git remote set-url origin {repository}'.format(repository=REPOSITORY+'.git'))
            run('git remote add origin {repository}'.format(repository=self.repository))
            run('sudo apt-get -y install virtualenv')
            run('virtualenv venv')
        self.deploy()

    # Метод для изменения пути до репозитория
    def change_repository(self):
        with cd(env.project_root):
            run('git remote set-url origin {repository}'.format(repository=self.repository))

    # Метод для обновления проекта
    def deploy(self):
        with cd(env.project_root):  # Заходим в директорию с проектом на сервере
            run('git pull {branch} {fetch}'.format(branch='origin', fetch='master'))  # Пуляемся из репозитория

    # Метод для отката последнего изменения (по коммиту)
    def rollback(self):
        with cd(env.project_root):
            run('git reset --hard HEAD^')
            self.control_service(action='restart')

    def get_name(self):
        return self.name


