# -*- coding: utf-8 -*-
import os
from settings.secret_settings import *

SERVER = "production"
PORT = 22
BRANCH = "dev"
PATH_KEY = [os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')]  # Локальный путь до файла с ключами
PYTHON = os.path.join(PATH, 'venv/bin/python')
PIP = os.path.join(PATH, 'venv/bin/pip')
WORK_SERVER = 'rabbitmq-server'
VENV_REQUIREMENTS = 'requirements.txt'

# class Settings(object):
#     SERVER = "production"
#     PORT = 22
#     BRANCH = "dev"
#     PATH_KEY = [os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')]  # Локальный путь до файла с ключами
#     PYTHON = os.path.join(PATH, 'venv/bin/python')
#     PIP = os.path.join(PATH, 'venv/bin/pip')
#     WORK_SERVER = 'rabbitmq-server'
#     VENV_REQUIREMENTS = 'requirements.txt'

