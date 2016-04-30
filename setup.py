from setuptools import setup, find_packages

requires = [
    'argparse'
]

setup(name='pythonwhois',
      version='2.4.3',
      description='Module for retrieving and parsing the WHOIS data for a domain. Supports most domains. No dependencies.',
      author='Sven Slootweg',
      author_email='pythonwhois@cryto.net',
      url='http://cryto.net/pythonwhois',
      packages=find_packages(exclude=['doc', 'test']),
      install_requires=requires,
      scripts=["pwhois"],
      license="WTFPL"
      )
