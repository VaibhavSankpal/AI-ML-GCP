from setuptools import find_packages
from setuptools import setup

# REQUIRED_PACKAGES = ['google-cloud-bigquery==1.20.0', 'pyarrow']

setup(
  name='census-train-package',
  version='0.1',
  # install_requires=REQUIRED_PACKAGES,
  packages=find_packages(),
  description='An Census deployment package for training on Cloud ML Engine.')