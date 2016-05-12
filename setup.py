from setuptools import setup

from crumby import __version__
from crumby import __doc__ as description

setup(name='crumby',
      version=__version__,
      author='bmweiner',
      author_email='bmweiner@users.noreply.github.com',
      url='https://github.com/bmweiner/crumby',
      description=description,
      license='MIT License',
      packages=['crumby', 'crumby.utils'],
      install_requires=['Flask', 'Flask-SQLAlchemy', 'geoip2'])
