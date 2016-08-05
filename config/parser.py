import json
import yaml

class JsonParser(object):
    config = None

    def __init__(self, path):
        with open(path) as f:
            self.config = json.loads(f.read())

    def getConfig(self):
        if self.config == None:
            raise UserWarning('There was no current information about test server')
        else:
            return self.config

    def getValue(self, value):
        return self.config[0][value]

class YamlParser(object):
    config = None

    def __init__(self):
        pass

    def __init__(self, path):
        with open(path) as f:
            self.config = yaml.load(f.read())

        print self.config['title']


if __name__ == '__main__':
    test = YamlParser('production.yaml')