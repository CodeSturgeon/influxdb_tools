from setuptools import setup

setup(
    name="influxdb_tools",
    version="0.0.1",
    package_dir={'': 'source'},
    scripts=[
        'scripts/influxdb_dumper',
        'scripts/influxdb_loader',
    ]
)
