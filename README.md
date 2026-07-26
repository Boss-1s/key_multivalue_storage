# Key to Multivalue Storage - kms
kms - a _tiny side project_ tuned into a **library**.

**JSON storage wrapper and editor.** Created with love by Boss_1s.

Once upon a time, this was just a small project to solve a problem: the over-steep learning curve for [scratchattach](https://github.com/TimMcCool/scratchattach)'s database functionality. Now, I have decided to make it a library, something with humble beginnings with big hopes in its future.



This is, after all, the greatest piece of a CPython progam I have made. ;)

__________

## Badges
### Download

[![CPython](https://img.shields.io/badge/CPython-3.12%20%7C%203.13%20%7C%203.14-blue?style=for-the-badge)](https://www.python.org/downloads/release/python-3122/)
[![Package](https://img.shields.io/badge/Stable%20Package-PyPi-violet?style=for-the-badge)](https://pypi.org/project/key-multivalue-storage/)
[![Beta Nightly](https://img.shields.io/badge/Nightly%20Package-kms--semver1%2E3%2Ex%20Nightly-purple?style=for-the-badge)](https://nightly.link/boss-1s/key_multivalue_storage/workflows/test.yml/semver1.3.x/full-kms-nightly.zip)

### Status

[![Release](https://img.shields.io/github/actions/workflow/status/Boss-1s/key_multivalue_storage/.github%2Fworkflows%2Frelease.yml?style=for-the-badge&label=Release&labelColor=maroon)](https://github.com/Boss-1s/key_multivalue_storage/deployments/release)
[![Tests](https://img.shields.io/github/actions/workflow/status/Boss-1s/key_multivalue_storage/.github%2Fworkflows%2Ftest.yml?style=for-the-badge&label=Tests&labelColor=blue)](https://github.com/Boss-1s/key_multivalue_storage/deployments/test)

### Info & Docs

[![Changelog](https://img.shields.io/badge/Changelog-Click%20Here-gray?style=for-the-badge&labelColor=blue)](https://boss-1s.github.io/key_multivalue_storage/CHANGELOG)
[![PyPI - Version](https://img.shields.io/pypi/v/key-multivalue-storage?style=for-the-badge&label=Latest&color=gray&labelColor=purple)](https://github.com/Boss-1s/key_multivalue_storage/releases)
[![Documentation](https://img.shields.io/badge/Documentation-Click-gray?style=for-the-badge&labelColor=blue)](https://boss-1s.github.io/key_multivalue_storage)
[![License](https://img.shields.io/pypi/l/key-multivalue-storage?style=for-the-badge&color=gray&labelColor=%230a6149)](https://github.com/Boss-1s/key_multivalue_storage/blob/main/LICENSE)
[![Contributing](https://img.shields.io/badge/Contribution%20Guidelines-Click-gray?style=for-the-badge&labelColor=orange)](https://github.com/Boss-1s/key_multivalue_storage/blob/main/docs/CONTRIBUTING.md)
[![Security](https://img.shields.io/badge/Versioning%20%26%20Security-Click-gray?style=for-the-badge&labelColor=red)](https://github.com/Boss-1s/key_multivalue_storage/blob/main/docs/CONTRIBUTING.md)

_____________

## Installation
Install with `pip`:
```bash
pip install -U key-multivalue-storage
```

Or, download the latest version of the `.whl` file [in the releases page](https://github.com/Boss-1s/key_multivalue_storage/releases)

You can also choose to download the development environment alongside the package:
```sh
pip install -U key-multivalue-storage[dev]
```
The development package includes Pylint and Griffe for testing and finding breaking changes. You can see the tests in the [test folder](https://github.com/Boss-1s/key_multivalue_storage/blob/semver1.3.x/test/). 

[*See more about tests here.*](https://boss-1s.github.io/key_multivalue_storage/Development)

## Usage
- Create a Storage object to wrap the data to be stored:
```py
from key_multivalue_storage import Storage
my-db = Storage("my_top_level_key", mysubkey="myvalue", myothersk="anotherval")
```
- To store the object, use `Storage.store()`.
```py
my-db.store("database.json")
```
- You can change certain global variables for each `Storage` instance.
```py
Storage.indent = 4 # indent size of JSON files
Storage.encode = True # Whether to encode stored values
Storage.auto_delete_self = True
# Whether to automatically release the object
# from memory after certain operations i.e.
# Storage.store()
```

### See the full documentation [here](https://boss-1s.github.io/key_multivalue_storage)!

## [Contribute](https://github.com/Boss-1s/key_multivalue_storage/fork)
## [Roadmap](https://github.com/Boss-1s/key_multivalue_storage/wiki/Roadmap#possible-future-features)
## [Report a Bug](https://github.com/Boss-1s/key_multivalue_storage/issues)
## [Scratchattach](https://github.com/TimMcCool/scratchattach/)
