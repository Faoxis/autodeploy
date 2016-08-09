# -*- coding: utf-8 -*-

import os


class Settings(object):
    USER = "JustAnUser"
    PASSWORD = "YouWillNeverGuess"
    HOST = "192.168.56.101"
    PATH = "/home/sebuntu-1/work/fabtest/"
    REPOSITORY = "https://github.com/faoxis/gittest.git"

    SERVER = "production"
    PORT = 22
    BRANCH = "dev"
    PATH_KEY = [os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')]  # Локальный путь до файла с ключами
    PYTHON = os.path.join(PATH, 'venv/bin/python')
    PIP = os.path.join(PATH, 'venv/bin/pip')
    WORK_SERVER = 'rabbitmq-server'
    VENV_REQUIREMENTS = 'requirements.txt'

    # # На случай, если понадобиться задать расположение python по абсолютному пути
    # def set_user_by_name(self):
    #     self.PYTHON = os.path.join(self.PATH, '/home/{user}venv/bin/python'.format(user=self.USER))
