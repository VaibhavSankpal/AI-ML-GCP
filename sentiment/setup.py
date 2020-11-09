from setuptools import setup, find_packages

REQUIRED_PACKAGES = ['pattern==2.6',
                     'keras==2.0.2',
                     'google-cloud-bigquery==1.20.0', 'pyarrow']

setup(name='sentiment_batch_job',
      version='1.0',
      author='Jigar Chhadwa',
      author_email='jigar.chhadwa@accenture.com',
      url='https://www.accenture.com',
      packages=find_packages(),
      include_package_data=True,
      description='Sentiment model on AI Platform Jobs',
      install_requires=[REQUIRED_PACKAGES],
      zip_safe=False)