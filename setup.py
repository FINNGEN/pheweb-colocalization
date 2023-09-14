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
          'Flask~=2.0.3',
          'finngen_common_data_model@git+https://github.com/FINNGEN/finngen-common-data-model.git@1696ee5e38d93ba77327a45ab4bc83b88d13d52e#egg=finngen_common_data_model',
          'attrs>=19.3.0',
          'SQLAlchemy~=1.3.19',
          'PyMySQL>=0.10.1',
          'pytest>=5.4.3',
          'mysqlclient~=2.0.1',
      ],
      dependency_links=[
          'https://github.com/FINNGEN/finngen-common-data-model.git@1696ee5e38d93ba77327a45ab4bc83b88d13d52e#egg=finngen_common_data_model'],
      extras_require={
          'dev': ['pytest>=6.1.2', 'pytest-cov>=2.10.1', ],
      }
)
