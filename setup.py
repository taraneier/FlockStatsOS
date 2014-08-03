from setuptools import setup

setup(
    name='flockapi',
    version='0.1',
    description='OpenShift App',
    author='Tara Neier',
    author_email='tara@neier.me',
    url='http://www.python.org/sigs/distutils-sig/',
    install_requires=['Django>=1.6', 'Django<1.7','djangorestframework','django-rest-swagger','pytz'],
)
