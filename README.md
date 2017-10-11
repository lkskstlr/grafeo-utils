# Grafeo Utils

**Cryptographically authenticated supply chain storage protocol.**

Full documentation for the project is available [here](https://lkskstlr.github.io/grafeo-utils/).

---

# Overview

This is work in progress and right now not even in alpha. The implementation is most likely not cryptographically sound. Do not use this within any production system. Any help is appreciated, just reach out via github issues :)

Grafeo is a cryptographic protocol to insure supply chain information authenticity. It works for distributed and centralized databases and does not require trust in any central organization.

This repository contains python utils to interface said protocol without hustle.

# Requirements

* Python (3.6)
* [nacl](https://github.com/pyca/pynacl) 
* [requests](https://github.com/requests/requests)
* [zbarlight](https://github.com/Polyconseil/zbarlight)

# Installation

Install using `pip`...
```bash
pip install grafeo
```
