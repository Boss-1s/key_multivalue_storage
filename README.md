# Key to Multivalue Storage - kms
kms - a tiny side project tuned into a library.


![CPython](https://img.shields.io/badge/CPython-3.12%20%7C%203.13%20%7C%203.14-purple?style=for-the-badge)
[![Package](https://img.shields.io/badge/Package-PyPi-violet?style=for-the-badge)](https://pypi.org/project/key-multivalue-storage/)
[![Nightly](https://img.shields.io/badge/Package-Nightly-violet?style=for-the-badge)](https://nightly.link/boss-1s/key_multivalue_storage/workflows/release-nightly/main/full-kms-nightly.zip)

---

[![Release](https://img.shields.io/github/actions/workflow/status/Boss-1s/key_multivalue_storage/.github%2Fworkflows%2Frelease.yml?style=for-the-badge&label=Release%20Env&labelColor=maroon)](https://github.com/Boss-1s/key_multivalue_storage/deployments/release)
[![Tests](https://img.shields.io/github/actions/workflow/status/Boss-1s/key_multivalue_storage/.github%2Fworkflows%2Ftest.yml?style=for-the-badge&label=Tests&labelColor=blue)](https://github.com/Boss-1s/key_multivalue_storage/deployments/test)
[![License](https://img.shields.io/pypi/l/key-multivalue-storage?style=for-the-badge&color=cyan&labelColor=%230a6149)](https://github.com/Boss-1s/key_multivalue_storage/blob/main/LICENSE)

---

[![PyPI - Version](https://img.shields.io/pypi/v/key-multivalue-storage?style=for-the-badge&label=Latest&color=teal)](https://github.com/Boss-1s/key_multivalue_storage/releases)

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

## Usage
- Create a Storage object to prepare the data to be stored:
```py
from key-multivalue-storage import Storage
my-db = Storage("my_top_level_key", mysubkey="myvalue", myothersk="anotherval")
```
- To store the object, use `Storage.store()`.
```py
my-db.store("database.json")
```
- You can change certain global settings for each `Storage` instance.
```py
Storage.indent = 4 #indent size of JSON files
Storage.encode = True # Whether to encode stored values
Storage.auto_delete_self = True
# Whether to automatically release the object
# from memory after certain operations i.e.
# Storage.store()
```

### See the full documentation [here](https://github.com/Boss-1s/key_multivalue_storage/wiki)!
