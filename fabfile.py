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


# Создание объекта с настройками для продакшена
prouction_settings = Settings()
prouction_settings.USER = prod_yaml['USER']
prouction_settings.PASSWORD = prod_yaml['PASSWORD']

# Создание еще одного объекта с настройками для тестового сервера
test_settings = Settings()

# Изменение настроек по умолчанию. Можно вынести в отдельный файл.
# Для этого можно в отдельном файле создать класс, который будет наследоваться от класса Settings.
test_settings.SERVER = 'test'
test_settings.USER = test_yaml['USER']
test_settings.PASSWORD = test_yaml['PASSWORD']

# Создание объекта - удаленного сервера
production_server = ServerSSH(prouction_settings)

# Инициализация production-сервера
@roles(prouction_settings.SERVER)
def init_production():
    production_server.init()

# Обновление production-сервера
@roles(prouction_settings.SERVER)
def deploy_production():
    production_server.deploy()
