# Welcome to the key_multivalue_storage wiki!

**JSON storage wrapper and editor.** Created with love by Boss_1s.

Once upon a time, this was just a small project to solve a problem: the over-steep learning curve for [scratchattach](https://github.com/TimMcCool/scratchattach)'s database functionality. Now, I have decided to make it a library, something with humble beginnings with big hopes in its future.

![CPython](https://img.shields.io/badge/CPython-3.12%20%7C%203.13%20%7C%203.14-purple?style=for-the-badge)
[![Release](https://img.shields.io/github/actions/workflow/status/Boss-1s/key_multivalue_storage/.github%2Fworkflows%2Frelease.yml?style=for-the-badge&label=Release%20Env&labelColor=maroon)](https://github.com/Boss-1s/key_multivalue_storage/deployments/release)
[![Tests](https://img.shields.io/github/actions/workflow/status/Boss-1s/key_multivalue_storage/.github%2Fworkflows%2Ftest.yml?style=for-the-badge&label=Tests&labelColor=blue)](https://github.com/Boss-1s/key_multivalue_storage/deployments/test)
[![License](https://img.shields.io/pypi/l/key-multivalue-storage?style=for-the-badge&color=cyan&labelColor=%230a6149)](https://github.com/Boss-1s/key_multivalue_storage/blob/main/LICENSE)
[![PyPI - Version](https://img.shields.io/pypi/v/key-multivalue-storage?style=for-the-badge&label=Latest&color=teal)](https://github.com/Boss-1s/key_multivalue_storage/releases)
[![](https://img.shields.io/github/v/release/boss-1s/key_multivalue_storage?include_prereleases&style=for-the-badge&label=Latest%20Unstable&color=%231b6e6e)](https://github.com/Boss-1s/key_multivalue_storage/releases)

### It is __strongly__ recommended to learn Python before using kms. The best environment to learn in is CPython 3.12 for this library.

> Please do note that throughout this repository, the library `key-multivalue-storage` may also be referred to as its repo/package name (`key_multivalue_storage`) or its abbreviation (`kms`).

## Documentation
- [**Documentation**](Documentation)
- [`Storage`](Documentation#storage)
- [Loading](Documentation#storageload)
- [Editing](Documentation#storageedit)
- [Deleting](Documentation#storagedelete)

## Resources
- [Versioning, Release, and Security](security)
- [Info on kms-semver2.0](Roadmap#kms-semver20-20270817)
- [PyPi Package Page](https://pypi.org/project/key-multivalue-storage/)

## Contributor Resources
- [**Structure of the library**](https://boss-1s.github.io/key_multivalue_storage/Documentation#structure-of-the-library)
- [Contributor Guidelines](contribution-guidelines)
- [Changelog](CHANGELOG)
- [Development Help](Development)
- [Roadmap](Roadmap)
- [Issues](https://github.com/Boss-1s/key_multivalue_storage/issues)
- [Pull Requests](https://github.com/Boss-1s/key_multivalue_storage/pulls)

You can contribute to this open-source project by [forking this repo](https://github.com/Boss-1s/key_multivalue_storage/fork), making changes, then opening a [pull request](https://github.com/Boss-1s/key_multivalue_storage/compare). Be sure to read through the [guidelines](CONTRIBUTING)!

## Installation
Install with `pip`:
```bash
pip install -U key-multivalue-storage
```

Or, download the latest version of the `.whl` file [here](https://pypi.org/project/key-multivalue-storage/#files)

You can also choose to download the development environment alongside the package:
```sh
pip install -U key-multivalue-storage[dev]
```
The development package contains both Pylint and Griffe.

## Basic Usage
- **Create a Storage object to prepare the data to be stored:**
```py
from key_multivalue_storage import Storage # note the module name!
my_db = Storage("my_top_level_key", mysubkey="myvalue", myothersk="anotherval")
```
- To store the object, use `Storage.store()`.
```py
my_db.store("database.json")
```
- You can change certain global settings for each `Storage` instance.
```py
Storage.indent = 4 #indent size of JSON files
Storage.encode = True #Whether to encode stored values
Storage.auto_delete_self = True
# Whether to automatically release the object
# from memory after certain operations i.e.
# Storage.store()
```
- **Loading a stored object by a top level key and loading all the top level keys of a JSON file:**
```py
>>> Storage.Load.by_key("database.json", "my_top_level_key")
Storage(top_lv_key="my_top_level_key", key_value_pairs=["mysubkey"="myvalue", "myothersk"="anotherval"])
>>> Storage.Load.keys("database.json")
["my_top_level_key"]
```
> [!TIP]
> [*See more about loading here.*](Documentation#storageload)

- **Editing a subkey's name and value within the JSON file:**
```py
>>> Storage.Edit.propkey("database.json", # file_path
                         "my_top_level_key", # top_lv_key
                         "mysubkey", # oldpropkey
                         "newkey" # newpropkey
                         noexist_ok = True # Creates a new subkey with the new subkey name if the old subkey name did not exist
                        )
>>> Storage.Load.values("database.json", "my_top_level_key", keys=True, raw=False)
["newkey: myvalue", "myothersk: anotherval"]
>>> Storage.Edit.propval("database.json", # file_path
                         "my_top_level_key", # top_lv_key
                         "myothersk", # propkey
                         "wow!" # newval
                        )
>>> Storage.Load.values("database.json", "my_top_level_key", keys=True, raw=False)
["newkey: myvalue", "myothersk: wow!"]
```
> [!TIP]
> [*See more about editing here.*](Documentation#storageedit)

- **Deleting a subkey-value pair within the JSON file:**
```py
>>> Storage.Delete.by_propkey("database.json", # file_path
                              "my_top_level_key", # top_level_key
                              "myothersk" # property_key
                             )
>>> Storage.Load.values("database.json", "my_top_level_key", keys=True, raw=False)
["newkey: myvalue"]
```
> [!TIP]
> [*See more about deleting here.*](Documentation#storagedelete)

- **Adding and subtracting two `Storage` instances:**
```py
>>> # Adding instances combines the two instances, as long as the top level key is the same.
>>> addStorage = Storage("combine", sk1="val1") + Storage("combine", sk2="val2")
>>> print(addStorage)
Storage(top_lv_key="combine", key_value_pairs=["sk1"="val1", "sk2"="val2"])
>>> # Subtracting instances remove any exact same key-value pairs from the two instances, as long as the top level key is the same.
>>> subStorage = Storage("combine", sk1="val1", sk2="val2") - Storage("combine", sk2="val2")
>>> print(addStorage)
Storage(top_lv_key="combine", key_value_pairs=["sk1"="val1"])
```
> [!TIP]
> [*See more about special functions here.*](Documentation#special-methods)

***

> [!TIP]
>**All kms features are documented in the [documentation](Documentation).**


---

## Thanks for using kms! ❤

<br><br><br><br><br><br>
<!--stackedit_data:
eyJoaXN0b3J5IjpbNzg4Njg3Mzk2LC04MDYwMjAwOTRdfQ==
-->