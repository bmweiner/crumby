from setuptools import setup

__version__ = '0.7.1'
__description__ = 'A Flask based web analytics app'

setup(name='crumby',
      version=__version__,
      author='bmweiner',
      author_email='bmweiner@users.noreply.github.com',
      url='https://github.com/bmweiner/crumby',
      description=__description__,
      license='MIT License',
      packages=['crumby', 'crumby.extensions', 'crumby.views'],
      include_package_data=True,
      scripts =['scripts/crumby'],
      install_requires=['Flask',
                        'Flask-Bcrypt',
                        'Flask-Login',
                        'Flask-SQLAlchemy',
                        'Jinja2',
                        'SQLAlchemy',
                        'geoip2'])
