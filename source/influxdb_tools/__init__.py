import argparse
from urllib import urlencode
from urllib2 import urlopen
from ConfigParser import SafeConfigParser
import json
import os


DUMPER_DESC = 'Dump InfluxDB series to json files'
LOADER_DESC = 'Load InfluxDB series from json files'
INFLUXDB_URL_TEMPLATE = (
        'http://{host}:{port}'
        '/db/{dbname}/series?u={user}&p={pass}'
    )


def dumper():
    # Setup cfg
    args = parse_args(DUMPER_DESC)
    cfg = load_cfg(args.config_file).defaults()
    cfg.update(args.__dict__)
    base_url = INFLUXDB_URL_TEMPLATE.format(**cfg)
    # Get series list
    series_url = base_url + '&' +  urlencode({'q': 'list series'})
    resp = urlopen(series_url)
    series_data = json.loads(resp.read())
    series = [p[1] for p in series_data[0]['points']]
    for s in series:
        print s
        s_url = base_url + '&' +  urlencode({'q': 'select * from "%s"'%s})
        resp = urlopen(s_url)
        s_path = os.path.join(cfg['data_dir'], s.replace('/', '_')+'.json')
        open(s_path, 'w').write(resp.read())


def parse_args(desc):
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('dbname', help='Name of database to work with')
    parser.add_argument('-d', '--data-dir', default='.',
            help='JSON files location')
    parser.add_argument('-c', '--config-file', default='./influxdb_tools.ini',
            help='Config file to use')

    return parser.parse_args()


def load_cfg(cfg_path):
    cfg = SafeConfigParser(defaults={
            'user': 'root',
            'pass': 'root',
            'host': 'localhost',
            'port': '8086',
        })
    cfg.read(cfg_path)
    return cfg
