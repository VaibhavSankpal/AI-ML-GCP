from setuptools import setup, find_packages

REQUIRED_PACKAGES = ['pandas',
                     'scikit-learn',
                     'sklearn',
                     'numpy',
                     'lime',
                     'google-cloud-storage']

setup(name='<TEMPLATE-NAME>',
      version='1.0',
      packages=find_packages(),
      include_package_data=True,
      description='<JOB-DESCRIPTION>',
      install_requires=[REQUIRED_PACKAGES],
      zip_safe=False)