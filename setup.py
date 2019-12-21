import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
# README = open(os.path.join(here, 'README.txt')).read()
# CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid==1.10.4',
    'pyramid_tm==2.2.1',
    'pyramid_mako==1.1.0',
    'transaction==2.4.0',
    'SQLAlchemy==1.3.6',
    'zope.sqlalchemy==1.1',
    'deform==2.0.7',
    'colander==1.7.0',
    'waitress==1.4.0',
    'pytest==5.1.2',
    'requests==2.22.0',
    'python-json-logger==0.1.11'
]

setup(name='tea',
      version='0.0',
      description='tea',
      # long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='microservice',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = tea:main
      [console_scripts]
      initialize_auth_db = tea.scripts.initializedb:main
      """,
      )
