#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()

def read_license():
    with open('LICENSE') as f:
        return f.read()

app_version = "2.3.0"
app_name = "phantasy_apps"
app_description = 'Physics high-level applications and toolkits for accelerator system -- applications'
app_long_description = readme() + '\n\n'
app_platform = ["Linux"]
app_author = "Tong Zhang"
app_author_email = "zhangt@frib.msu.edu"
app_license = read_license()
# app_url = "https://controls.frib.msu.edu/phantasy/"
app_keywords = "phantasy high-level python"
installrequires = [
    'numpy',
#    'scipy',
    'matplotlib',
#    'xlrd',
]
extrasrequire = {
    "LMS": [
        'tornado',
        'humanize',
        'motor==0.4',
        'jinja2',
        'jsonschema',
    ]
}

def set_entry_points():
    r = {}
    r['console_scripts'] = [
        'pm_dat2json=phantasy_apps.wire_scanner.converter:main',
        'as_out2json=phantasy_apps.allison_scanner.out2json:main',
    ]

    r['gui_scripts'] = [
        'unicorn_app=phantasy_apps.unicorn:run',
        'lattice_viewer=phantasy_apps.lattice_viewer:run',
        'trajectory_viewer=phantasy_apps.trajectory_viewer:run',
        'correlation_visualizer=phantasy_apps.correlation_visualizer:run',
        'quad_scan=phantasy_apps.quad_scan:run',
        'va_launcher=phantasy_apps.va:run',
        'orm=phantasy_apps.orm:run',
        'wire_scanner=phantasy_apps.wire_scanner:run',
        'settings_manager=phantasy_apps.settings_manager:run',
        'allison_scanner=phantasy_apps.allison_scanner:run',
        'app_launcher=phantasy_apps.app_launcher:run',
        'device_viewer=phantasy_apps.diag_viewer:run',
        'image_viewer=phantasy_apps.imageviewer:run',
        'pm_viewer=phantasy_apps.pm_viewer:run',
        'phy_model=phantasy_apps.online_model:run',
    ]
    return r

setup(
    name=app_name,
    version=app_version,
    description=app_description,
    long_description=app_long_description,
    author=app_author,
    author_email=app_author_email,
    # url = app_url,
    platforms=app_platform,
    license=app_license,
    keywords=app_keywords,
    packages=find_packages(exclude=['utest', 'demo', 'example']),
    include_package_data=True,
    entry_points=set_entry_points(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Physics'],
    tests_require=['nose'],
    test_suite='nose.collector',
    install_requires=installrequires,
    extras_require=extrasrequire,
)
