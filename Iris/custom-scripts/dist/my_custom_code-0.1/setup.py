from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = ['scikit-learn==0.20.2']

setup(
    name='my_custom_code',
    version='0.1',
    author = 'Vaibhav Sankpal',
    author_email = 'vaibhav.sankpal@accenture.com',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    scripts=['predictor.py', 'preprocess.py'])

