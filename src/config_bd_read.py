import configparser
import os
from config import ROOT_DIR

file_path = os.path.join(ROOT_DIR, 'data', 'database.ini')

def connect():
    config_BD = {}
    config = configparser.ConfigParser()
    config.read(file_path)


    host = config['postgresql']['host']
    port = config['postgresql']['port']
    user = config['postgresql']['user']
    password = config['postgresql']['password']

    config_BD['host'] = host
    config_BD['port'] = port
    config_BD['user'] = user
    config_BD['password'] = password

    return config_BD

