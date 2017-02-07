from setuptools import setup

__version__ = '0.5'
__description__ = 'A Flask based web analytics app'

setup(name='crumby',
      version=__version__,
      author='bmweiner',
      author_email='bmweiner@users.noreply.github.com',
      url='https://github.com/bmweiner/crumby',
      description=__description__,
      license='MIT License',
      packages=['crumby', 'crumby.utils', 'crumby.views'],
      install_requires=['Flask', 'Flask-SQLAlchemy', 'geoip2'])
