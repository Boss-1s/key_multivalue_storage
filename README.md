# Key to Multivalue Storage - kms
kms - a _tiny side project_ tuned into a **library**.

<img width="100" alt="kms logo" src="https://github.com/user-attachments/assets/0b569791-672b-4954-a377-fd1cbe4543ae" />

**JSON storage wrapper and editor.** Created with love by Boss_1s.

Once upon a time, this was just a small project to solve a problem: the over-steep learning curve for [scratchattach](https://github.com/TimMcCool/scratchattach)'s database functionality. Now, I have decided to make it a library, something with humble beginnings with big hopes in its future.



This is, after all, the greatest piece of a CPython progam I have made. ;)

---------

## 🚀 What's New in `kms-semver1.4.0a1`

> [!important]
> `kms-semver1.4.x` is ***officially*** built off of `kms-v1.3.1/2026.08.12`, and *partially* off of `kms-v1.3.2/2026.09.30`.

### 💡 Features & Automation

* **More Encoding Options!**
    * Instead of being forced to use a very childish, insecure character mapping encoding system, you can now choose from a variety of different encodings, including popular ones like Base64 or binary.
    * Different character sets aside from the default UTF-8 are also added, allowing for a wider range of support.
    * Plus, you can now also encode subkeys, top level keys, both in the JSON file AND the object!
    ```py
    from key_multivalue_storage import Storage, Encoding, CharSet # New enums containing all allowed encodings and charsets

    db = Storage("top_level_key", foo="bar", baz="bax")
    db.encoding = Encoding.Base64
    db.encode_object(top_lv_key=True,
                     subkeys=False,
                     subvals=True) # Object's values will now be encoded
    print(repr(db)) # Storage(top_lv_key=dG9wX2xldmVsX2tleQ==, key_value_pairs={'foo':'YmFy','baz:'YmF4'})

    print(db.charset) # CharSet.UTF8

    db.store(
        'my_database_storage.json',
        encoding=Encoding.Base2, # binary
        charset=CharSet.ASCII # American Standard Code for Information Interchange
    ) # Stores the original Storage object (before encoding into Base64) as Binary after conversion to ASCII

    # The Storage object does NOT get mutated by `.store`, as it should.
    ```
* New functions `kms.storage.create_storage()` and `kms.storage.create_storage_from_dict()`

    > Note that these functions are **module level functions.** They are not methods residing in `Storage`.
    
    * `kms.storage.create_storage()` does the exact same as instantiating with `Storage(key, kwargs)`; it is used internally to avoid circular imports.
      ```py
      def create_storage(key: Any, **kwargs: Any) -> Storage: ...
      ```
    * `kms.storage.create_storage_from_dict()` takes a dictionary in the format `dict[Any, dict[Any, Any]]` (monokey-multivalue structure) and converts it into a `Storage` object. This function is especially useful if unpacking is not your favorite thing. This function is also used internally solely to avoid circular imports.
      ```py
      def create_storage_from_dict(data_dict: dict[Any, dict[Any, Any]]) -> Storage: ...
      ```
* 
    

### 🪲 Bug Fixes

*

### ⏰ Infrastructure & CI

*

### 📢 Upcoming Roadmap
* **v1.4.0a1:** Expected October 24th, 2026.
* **v1.4.0 Major:** Alpha scheduled for October 12, 2026, with a stable target of early January 2027.

> [!important]
> Forward-ports from `semver1.3.x` are not included here. Check the `semver1.3.x` branch's README for specific changes there.

<!--🔗 **[Full Changelog](https://github.com/Boss-1s/key_multivalue_storage/compare/v1.3.1.20260812...v1.3.2.20260930)**-->
🔗 **[Working Changelog](https://github.com/Boss-1s/key_multivalue_storage/compare/v1.3.1.20260812...semver1.4.x)**

__________

## Badges
### Download

[![CPython](https://img.shields.io/badge/CPython-3.12%20%7C%203.13%20%7C%203.14%20%7C%203.15-blue?style=for-the-badge)](https://www.python.org/downloads/release/python-3122/)
[![Package](https://img.shields.io/badge/Stable%20Package-PyPi-violet?style=for-the-badge)](https://pypi.org/project/key-multivalue-storage/)
[![Beta Nightly](https://img.shields.io/badge/Nightly%20Package-kms--semver1%2E4%2Ex%20Nightly-purple?style=for-the-badge)](https://nightly.link/boss-1s/key_multivalue_storage/workflows/test.yml/semver1.4.x/full-kms-semver-1-3-nightly.zip)

### Status

[![Release](https://img.shields.io/github/actions/workflow/status/Boss-1s/key_multivalue_storage/.github%2Fworkflows%2Frelease.yml?style=for-the-badge&label=Release&labelColor=maroon)](https://github.com/Boss-1s/key_multivalue_storage/deployments/release)
[![Tests](https://img.shields.io/github/actions/workflow/status/Boss-1s/key_multivalue_storage/.github%2Fworkflows%2Ftest.yml?branch=semver1.4.x&style=for-the-badge&label=Tests&labelColor=blue)](https://github.com/Boss-1s/key_multivalue_storage/deployments/test)

[![Quality gate](https://sonarcloud.io/api/project_badges/quality_gate?project=Boss-1s_key_multivalue_storage)](https://sonarcloud.io/summary/new_code?id=Boss-1s_key_multivalue_storage)

### Info & Docs

[![Changelog](https://img.shields.io/badge/Changelog-Click-gray?style=for-the-badge&labelColor=blue)](https://boss-1s.github.io/key_multivalue_storage/CHANGELOG)
[![Latest Version](https://img.shields.io/github/v/release/Boss-1s/key_multivalue_storage?include_prereleases&sort=semver&filter=v1.4.*&style=for-the-badge&label=Latest&labelColor=purple&color=gray
)](https://github.com/Boss-1s/key_multivalue_storage/releases)
[![Documentation](https://img.shields.io/badge/Documentation-Click-gray?style=for-the-badge&labelColor=blue)](https://boss-1s.github.io/key_multivalue_storage)
[![License](https://img.shields.io/pypi/l/key-multivalue-storage?style=for-the-badge&color=gray&labelColor=%230a6149)](https://github.com/Boss-1s/key_multivalue_storage/blob/main/LICENSE)
[![Contributing](https://img.shields.io/badge/Contribution%20Guidelines-Click-gray?style=for-the-badge&labelColor=orange)](https://boss-1s.github.io/key_multivalue_storage/contribution-guidelines)
[![Security](https://img.shields.io/badge/Versioning%20%26%20Security-Click-gray?style=for-the-badge&labelColor=red)](https://boss-1s.github.io/key_multivalue_storage/security)

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
The development package includes Pylint for testing and Griffe for finding breaking changes. You can see every test script in the repo's [test folder](https://github.com/Boss-1s/key_multivalue_storage/blob/semver1.4.x/test/). 

[*See more about tests here.*](https://boss-1s.github.io/key_multivalue_storage/Development)

## Usage
- Create a Storage object to wrap the data to be stored:
```py
>>> from key_multivalue_storage import Storage
>>> my_db = Storage("my_top_level_key", mysubkey="myvalue", myothersk="anotherval")
```
- To store the object, use `Storage.store()`.
```py
>>> my_db.store("database.json")
Data stored successfully in 'database.json'.
```
- You can change certain global variables for each `Storage` instance.
```py
>>> Storage.indent = 4 # indent size of JSON files
>>> Storage.encode = True # Whether to encode stored values
```
- Load the data back into a Storage object:
```py
>>> import key_multivalue_storage as kms
>>> loaded_db = kms.Load.by_key("database.json", "my_top_level_key") # You can also use Storage.Load.by_key()
>>> loaded_db = my_db
True
```
- You can also cast a Storage object into a dictionary!
```py
>>> dict_db = dict(my_db)
>>> dict_db
{"my_top_level_key":{"mysubkey":"myvalue","myothersk":"anotherval"}}
```

There's a _lot_ more to this library that what _meets the eye_.

### See the full documentation [here](https://boss-1s.github.io/key_multivalue_storage)!

## [Contribute](https://github.com/Boss-1s/key_multivalue_storage/fork)
## [Roadmap](https://github.com/Boss-1s/key_multivalue_storage/wiki/Roadmap#possible-future-features)
## [Report a Bug](https://github.com/Boss-1s/key_multivalue_storage/issues)


Have a GREAT day/night! :)
