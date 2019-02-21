try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='namara',
    packages=['namara'],
    version='0.2.0',
    description='The official Python client for the Namara data collaboration platform',
    author='ThinkData Works',
    author_email='info@namara.io',
    license='Apache-2.0',
    url='https://github.com/namara-io/namara-python',
    keywords=['namara','open data','api','canada','us','government','independent'],
    install_requires=['requests-futures==0.9.9'],
    classifiers=[]
)
