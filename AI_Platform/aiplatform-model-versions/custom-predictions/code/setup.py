from setuptools import setup
from setuptools import find_packages

setup(
    name='my_custom_code',
    version='0.1',
    author = 'Vaibhav Sankpal',
    author_email = 'vaibhav.sankpal@accenture.com',
    packages=find_packages(),
    scripts=['predictor.py', 'preprocess.py'])