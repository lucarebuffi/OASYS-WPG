#! /usr/bin/env python3

import os

from setuptools import find_packages, setup

NAME = 'OASYS-WPG'
VERSION = '0.0.1'
ISRELEASED = True

DESCRIPTION = 'WPG on OASYS'
README_FILE = os.path.join(os.path.dirname(__file__), 'README.txt')
LONG_DESCRIPTION = open(README_FILE).read()
AUTHOR = 'Alexey Buzmakov, Luca Rebuffi'
AUTHOR_EMAIL = 'luca.rebuffi@elettra.eu'
URL = 'https://github.com/lucarebuffi/OASYS-WPG'
DOWNLOAD_URL = 'https://github.com/lucarebuffi/OASYS-WPG'
LICENSE = 'GPLv3'

KEYWORDS = (
    'waveoptics',
    'simulator',
    'oasys1',
)

CLASSIFIERS = (
    'Development Status :: 4 - Beta',
    'Environment :: X11 Applications :: Qt',
    'Environment :: Console',
    'Environment :: Plugins',
    'Programming Language :: Python :: 3',
    'Intended Audience :: Science/Research',
)

SETUP_REQUIRES = (
    'setuptools',
)

INSTALL_REQUIRES = (
    'oasys>=1.0.0',
)

PACKAGES = find_packages(exclude=('*.tests', '*.tests.*', 'tests.*', 'tests'))

PACKAGE_DATA = {
    "orangecontrib.wpg.widgets.sources":["icons/*.png", "icons/*.jpg"],
    "orangecontrib.wpg.widgets.optical_elements":["icons/*.png", "icons/*.jpg"],
}

NAMESPACE_PACAKGES = ["orangecontrib", "orangecontrib.wpg", "orangecontrib.wpg.widgets"]

ENTRY_POINTS = {
    'oasys.addons' : ("wpg = orangecontrib.wpg", ),
    'oasys.widgets' : (
        "WPG Sources = orangecontrib.wpg.widgets.sources",
        "WPG Optical Elements = orangecontrib.wpg.widgets.optical_elements",
    ),
}

if __name__ == '__main__':
    setup(
          name = NAME,
          version = VERSION,
          description = DESCRIPTION,
          long_description = LONG_DESCRIPTION,
          author = AUTHOR,
          author_email = AUTHOR_EMAIL,
          url = URL,
          download_url = DOWNLOAD_URL,
          license = LICENSE,
          keywords = KEYWORDS,
          classifiers = CLASSIFIERS,
          packages = PACKAGES,
          package_data = PACKAGE_DATA,
          #          py_modules = PY_MODULES,
          setup_requires = SETUP_REQUIRES,
          install_requires = INSTALL_REQUIRES,
          #extras_require = EXTRAS_REQUIRE,
          #dependency_links = DEPENDENCY_LINKS,
          entry_points = ENTRY_POINTS,
          namespace_packages=NAMESPACE_PACAKGES,
          include_package_data = True,
          zip_safe = False,
          )