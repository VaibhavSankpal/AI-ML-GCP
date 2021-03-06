from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = ['lime','google-cloud-bigquery==1.20.0', 'pyarrow']

setup(
  name='census-deploy-package',
  version='0.1',
  author = 'Vaibhav Sankpal',
  author_email = 'vaibhav.sankpal@accenture.com',
  install_requires=REQUIRED_PACKAGES,
  packages=find_packages(),
  description='A Census deployment package for training on Cloud AI Platform.')