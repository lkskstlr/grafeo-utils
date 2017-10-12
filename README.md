# Grafeo Utils

[![build-status-image]][travis]
[![pypi-version]][pypi]
[![coverage-status]][coveralls]

_At the moment he code coverage banner is often wrong. Just click it to go to [coveralls.io](https://coveralls.io/github/lkskstlr/grafeo-utils?branch=maste) and see the real coverage._ 


**This is work in progress and right now not even in alpha. The implementation is most likely not cryptographically sound. Do not use this within any production system. Any help is appreciated, just reach out via github issues :)**


**Cryptographically authenticated supply chain storage protocol.**

Full documentation for the project is available [here](https://lkskstlr.github.io/grafeo-utils/).

---

# Overview
Grafeo is a cryptographic protocol to insure supply chain information authenticity. It works for distributed and centralized databases and does not require trust in any central organization.

This repository contains python utils to interface said protocol without hustle.

# Requirements

* Python (3.6)
* [nacl](https://github.com/pyca/pynacl) 
* [requests](https://github.com/requests/requests)

# Installation
Install using `pip`
```bash
pip install grafeo
```

[build-status-image]: https://travis-ci.org/lkskstlr/grafeo-utils.svg?branch=master
[travis]: https://travis-ci.org/lkskstlr/grafeo-utils?branch=master

[pypi-version]: https://img.shields.io/pypi/v/grafeo.svg
[pypi]: https://pypi.python.org/pypi/grafeo

[coverage-status]: https://coveralls.io/repos/github/lkskstlr/grafeo-utils/badge.svg?branch=master
[coveralls]: https://coveralls.io/github/lkskstlr/grafeo-utils?branch=maste
