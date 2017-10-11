from setuptools import setup

setup(
    name="grafeo",
    packages=["grafeo"],
    version="0.0.2",
    description = 'grafeo: Cryptographically authenticated supply chain storage protocol',
    author = 'Lukas Koestlers',
    author_email = 'lkskstlr@gmail.com',
    license = 'MIT',
    url = 'https://github.com/lkskstlr/grafeo-utils',
    install_requires=[
          'pynacl',
          'requests',
          'zbarlight'
      ],
    keywords = [],
    classifiers = [],
)
