from setuptools import setup

# Put here required packages
packages = ['Django<=1.5',]

dependency_links = ['https://www.djangoproject.com/download/1.5.1/tarball/#egg=Django-1.5.1',],

setup(
    name='flockapi',
    version='0.1',
    description='OpenShift App',
    author='Tara Neier',
    author_email='tara@neier.me',
    url='http://www.python.org/sigs/distutils-sig/',
    install_requires=[
        'Django>=1.5',
        'Django<1.7',
        'django-rest-swagger',
        'djangorestframework',
        'pytz'
    ],
)
