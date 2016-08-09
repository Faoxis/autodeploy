# coding: utf-8
import os

import yaml
from fabric.decorators import roles
from fab.main import ServerSSH
from settings.settings_class import Settings

# Yaml-файл содержит необходимые настройки, в том числе пароли.
# Нужен тут только для того, чтобы не хранить эту информацию в коммите
with open('settings/productionserver.yaml') as f:
    prod_yaml = yaml.load(f.read())

# Аналогично
with open('settings/testserver.yaml') as f:
    test_yaml = yaml.load(f.read())

# ----------------------------- Настройка продакшена --------------------------#
# Создание объекта с настройками для продакшена
prod_settings = Settings()
prod_settings.USER = prod_yaml['USER']
prod_settings.PASSWORD = prod_yaml['PASSWORD']

# Создание объекта - удаленного сервера
production_server = ServerSSH(prod_settings)


# Инициализация production-сервера
@roles(prod_settings.SERVER)
def init_production():
    # Метод create_dir нужен для создания рабочего каталога на сервере
    production_server.create_dir()
    # Метод init базового класса ServerSSH инициализирует git, устанавливает виртуальное окружение
    # и скачивает последнюю версию проекта
    production_server.init()
    # Метод pip позволяет выполнять команды от имени pip вируального окружения сервера
    production_server.pip('install -r requirements.txt')
    # Метод python позволяет выполнять команды "от лица" python виртуального окружения сервера
    production_server.python('hello.py')  # В данном примере запускает скрипт hello.py,
    # но вместо него можно было запустить и скрипт с миграцией базы данных

    # Метод control_service позволяет совершать операции restart | stop | start с каким - либо сервисом на сервере
    # production_server.control_service('restart', 'rabbitmq-server' ) # Сервис можно указать явно
    production_server.control_service('restart')  # Или просто указать дейтвие,
    # которое будете применено к серверу по умолчанию


# Обновление production-сервера
@roles(prod_settings.SERVER)
def deploy_production():
    production_server.deploy()


# Обновление виртуального окружения
@roles(prod_settings.SERVER)
def venv_update_production():
    production_server.venv_update()


# --------------------------------------------------------------------------------#


# ----------------------------- Настройка тестового сервера ----------------------#

# Изменение настроек по умолчанию. Можно вынести в отдельный файл.
# Для этого можно в отдельном файле создать класс, который будет наследоваться от класса Settings.
# Тут создается класс только для примера.
class TestServerSettings(Settings):
    SERVER = 'test'
    USER = test_yaml['USER']
    PASSWORD = test_yaml['PASSWORD']
    REPOSITORY = test_yaml['REPOSITORY']
    HOST = test_yaml['HOST']
    PATH = test_yaml['PATH']


# Создание еще одного объекта с настройками для тестового сервера
test_settings = TestServerSettings()

# Создание тестового сервера
test_server = ServerSSH(test_settings)


@roles(test_settings.SERVER)
def init_test_server():
    test_server.init()


@roles(test_settings.SERVER)
def deploy_test_server():
    test_server.deploy()
    # --------------------------------------------------------------------------------#



