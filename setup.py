#!/usr/bin/env python
from distutils.core import setup

setup(name='pheweb_colocalization',
      version='0.0.1',
      description='pheweb colocalization',
      author='major seitan',
      packages=['pheweb_colocalization'],
      license='MIT',
      url='https://github.com/FINNGEN/finngen-common-data-model',
      package_dir={ 'pheweb_colocalization': 'pheweb_colocalization' },
      tests_require=['pytest', 'tox', 'pytest-cov', ],
      install_requires=[
          'finngen_common_data_model@git+https://github.com/FINNGEN/finngen-common-data-model.git@79b91972e85cd6cf6e2afd63dab1860eb7385009#egg=finngen_common_data_model',
          'attrs>=19.3.0',
          'SQLAlchemy>=1.3.18',
          'pytest>=5.4.3' ],
      dependency_links=['https://github.com/FINNGEN/finngen-common-data-model.git@79b91972e85cd6cf6e2afd63dab1860eb7385009#egg=finngen_common_data_model'])
