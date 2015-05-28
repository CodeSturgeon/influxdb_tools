import argparse
from urllib import urlencode
from urllib2 import urlopen
from ConfigParser import SafeConfigParser


DUMPER_DESC = 'Dump InfluxDB series to json files'
LOADER_DESC = 'Load InfluxDB series from json files'
INFLUXDB_URL_TEMPLATE = ''.join([
        'http://{host}:{port}',
        '/db/{dbname}/series?u={user}&p=pass',
    ])


def dumper():
    args = parse_args(DUMPER_DESC)
    cfg = load_cfg(args.config_file).defaults()
    cfg.update(args.__dict__)
    print cfg


def parse_args(desc):
    parser = argparse.ArgumentParser(description=desc)
    #parser.add_argument('dbname', help='Name of database to work with')
    parser.add_argument('-d', '--data-dir', default='.',
            help='JSON files location')
    parser.add_argument('-c', '--config-file', default='./influxdb_tools.ini',
            help='Config file to use')

    return parser.parse_args()


def load_cfg(cfg_path):
    cfg = SafeConfigParser(defaults={
            'user': 'root',
            'pass': 'root',
            'addr': 'localhost',
            'port': '8086',
        })
    cfg.read(cfg_path)
    return cfg
