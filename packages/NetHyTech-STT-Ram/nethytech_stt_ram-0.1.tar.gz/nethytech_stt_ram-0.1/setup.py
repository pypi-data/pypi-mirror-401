from setuptools import setup, find_packages

setup(
    name='NetHyTech_STT-Ram',
    version='0.1',
    author='Ramsharma',
    author_email='rambhakthanuman823975@gmail.com',
    description='this is speech to text package created by a Ramsharma',)
packages=find_packages(),
install_requirements=[
   'selenium',
   'webdriver_manager'
    ]

