# -*- coding: utf-8 -*-
import yaml
import os
from fabric.api import run, env, cd, puts


class ServerSSH(object):
    # В конструктор класса передается объект класса Settings,
    # который содержит в себе все необходимые настройки
    def __init__(self, yaml_file, host):

        with open(yaml_file) as f:
            yaml_config = yaml.load(f.read())

        env['host_string'] = host

        # Инициализация окружения
        env.key_filename = yaml_config['path_key']
        env.user = host.split('@')[0]
        env.project_root = yaml_config['path']

        try:
            env.python = yaml_config['python']
        except KeyError:
            env.python = os.path.join(env.project_root, 'venv/bin/python')

        try:
            env.pip = yaml_config['pip']
        except KeyError:
            env.pip = os.path.join(env.project_root, 'venv/bin/pip')

        try:
            self.branch = yaml_config['branch']
        except KeyError:
            self.branch = 'master'

        try:
            self.requirements = yaml_config['venv_requirements']
        except:
            self.requirements = 'requirements.txt'

        self.config_server = yaml_config['work_service']
        self.repository = yaml_config['repository']
        self.path = yaml_config['path']
        self.migrate_command = yaml_config['migrate_command']


    # Создание папки с виртуальным окружением
    def create_dir(self):
        run('mkdir -p {}'.format(self.path))

    def delete_dir(self):
        run('rm -rf {}'.format(self.path))

    # Установка требуемых для нормальной работы плагинов
    def pip_install_requirements(self, requirements=None):
        req_command = 'install -r {requirements}'
        if not requirements:
            self.pip(req_command.format(requirements=self.requirements))
        else:
            self.pip(req_command.format(requirements=requirements))

    # Метод для изменения состояния какого-либо сервиса
    def control_service(self, action='restart', service=None):
        if service is None:
            service = self.config_server
            if service == 'None':
                return
        run('sudo service {server_name} {action}'.format(server_name=service,
                                                         action=action))
        puts('{service} has been {action}ed'.format(service=service,
                                                    action=action))

    # Метода для выполнения какой-либо программы внутри корневого каталога с проектом
    def run(self, action):
        with cd(env.project_root):
            run(action)

    # Запуск стронней функции
    def do(self, f):
        with cd(env.project_root):
            f()

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
        with cd(env.project_root):
            run('git pull origin {branch}'.format(branch=self.branch))

    # Метод для отката с определенному коммиту
    def rollback(self, hash=None):
        if not hash:
            self.rollback_on_commit()
        else:
            with cd(env.project_root):
                run('git reset --hard {hash}'.format(hash=hash))

    # Метод для отката последнего изменения (по коммиту)
    def rollback_on_commit(self):
        with cd(env.project_root):
            run('git reset --hard HEAD^')

    # Метод для полного обновления вируального окружения
    # Подразумевается, что в проекте присутствует файл requirements.txt
    # Имя файла можно поменять в объекте с настройками
    def venv_update(self):
        with cd(env.project_root):
            run('rm -rf venv')
            run('virtualenv venv')
            # self.pip_install_requirements()

    def run_migrate_command(self):
        self.run(self.migrate_command)