# -*- coding: utf-8 -*-

from fabric.api import run, env, cd, puts


class ServerSSH(object):
    settings = None

    # В конструктор класса передается объект класса Settings,
    # который содержит в себе все необходимые настройки
    def __init__(self, settings):
        self.settings = settings
        # Сразу же необходимо "сказать" библиотеке fabric о создании новой роли
        env.roledefs[self.settings.SERVER] = [self.settings.USER + '@' +
                                              self.settings.HOST + ':' +
                                              str(self.settings.PORT)]

        # Инициализация окружения
        env.key_filename = self.settings.PATH_KEY
        env.user = self.settings.USER
        env.password = self.settings.PASSWORD
        env.project_root = self.settings.PATH
        env.python = self.settings.PYTHON
        env.pip = self.settings.PIP

    def create_dir(self):
        run('mkdir -p {}'.format(self.settings.PATH))

    # Метод для изменения состояния какого-либо сервиса
    def control_service(self, action='restart', service=None):
        if service is None:
            if self.settings.WORK_SERVER is None:
                return
            service = self.settings.WORK_SERVER
        run('echo {password} | sudo -S service {server_name} {action}'.format(server_name=service,
                                                                              password=self.settings.PASSWORD,
                                                                              action=action))
        puts('{service} has been {action}ed'.format(service=service, action=action))

    # Метода для выполнения какой-либо программы внутри корневого каталога с проектом
    def do(self, action):
        with cd(env.project_root):
            run(action)
        puts('{action} is completed'.format(action=action))

    # Метода для выполнения команды "от лица" pip из вируального окружения
    def pip(self, action):
        with cd(env.project_root):
            run('{pip} {action}'.format(pip=env.pip, action=action))

    # Метода для выполнения команды "от лица" python из вируального окружения
    def python(self, action):
        with cd(env.project_root):
            run('{python} {action}'.format(python=env.python, action=action))

    # Метод для полного обновления вируального окружения
    # Подразумевается, что в проекте присутствует файл requirements.txt
    # Имя файла можно поменять в объекте с настройками
    def venv_update(self):
        with cd(env.project_root):
            run('rm -rf venv')
            run('virtualenv venv')
            # run('{pip} install -r {requirements}'.format(pip=env.pip, requirements=self.settings.VENV_REQUIREMENTS))

    # Подготовка окружения на удаленном компьютере к работе
    def init(self):
        with cd(env.project_root):
            run('git init')
            # run('git remote set-url origin {repository}'.format(repository=REPOSITORY+'.git'))
            run('git remote add origin {repository}'.format(repository=self.settings.REPOSITORY))
            run('echo {password} | sudo -S apt-get -y install virtualenv'.format(password=self.settings.PASSWORD))
            run('virtualenv venv')
        self.deploy()

    # Метод для изменения пути до репозитория
    def change_repository(self):
        with cd(env.project_root):
            run('git remote set-url origin {repository}'.format(repository=self.settings.REPOSITORY))

    # Метод для обновления проекта
    def deploy(self):
        with cd(env.project_root):  # Заходим в директорию с проектом на сервере
            run('git pull {branch} {fetch}'.format(branch='origin', fetch='master'))  # Пуляемся из репозитория

    # Метод для отката последнего изменения (по коммиту)
    def rollback(self):
        with cd(env.project_root):
            run('git reset --hard HEAD^')
            self.control_service(action='restart')
