# Roadmap
> [!Tip]
> **This is the roadmap for kms.** As time goes on, more and more items and information will be added to this roadmap.

[**Learn more about the versioning system**](https://github.com/Boss-1s/key_multivalue_storage/blob/main/SECURITY.md#official-versioning)

[**Learn about supported versions**](https://github.com/Boss-1s/key_multivalue_storage/blob/main/SECURITY.md#supported-versions)

## The "No" List
kms will **NEVER** have the following features:
* The ability to interact with the following file extensions: `*.txt`, `*.rtf`, `*.dbf`, `*.html`, `*.mdb`, `*.accdb`
* The reliance on other libraries that function similar to kms

## Accepted Issues

[See bugs here.](https://github.com/Boss-1s/key_multivalue_storage/issues?q=is%3Aissue%20state%3Aopen%20label%3Abug)

[See refactorization requests here.](https://github.com/Boss-1s/key_multivalue_storage/issues?q=is%3Aissue%20state%3Aopen%20label%3Arefactor)

[See feature requests here.](https://github.com/Boss-1s/key_multivalue_storage/issues?q=is%3Aissue%20state%3Aopen%20label%3Aenhancement)

## Full Roadmap

> [!warning]
> This roadmap has been completely rewritten to follow a five-to-six-month minor release cycle.

<!--
Roadmap format:

#### kms-semver<semver>
- **Projected Release Date: YYYY/MM/DD**
- **Projected Alpha 0 Release Date: YYYY/MM/DD** (only for minor and major updates)

*Stable Release tag: `<PyPi Version>`

##### Features
- List features here.

##### Bug Fixes
- List bug fixes here

##### Graceful Deprecation cycle <semver>
- List 'partial' breaking changes and deprecations here.
-->

### kms-semver1.3.2
- **Projected Release Date: 2026/9/30**

*Stable Release tag: `v1.3.2.20260930`*

#### Features

- [**#52**](https://github.com/Boss-1s/key_multivalue_storage/issues/52) - *`logging.Logger`*
- [**#75**](https://github.com/Boss-1s/key_multivalue_storage/issues/75) - *`__iadd__` for `Storage`*

#### Bug Fixes

None for now...

#### Graceful Deprecation cycle 1.3.2

- None for now...

---

### kms-semver1.4.0
- **Projected Stable Release Date: 2027/01/03**
- **Projected Alpha 0 Release Date: 2026/10/12**

*Stable Release tag: `v1.4.0.20260103`*

#### Features
* Make certain functions accept a `Storage` object so that arithmetic/bitwise operators can be avoided
* Make certain functions return `Storage` objects instead of `None`
* New methods allowing for easy modification of `Storage` objects in `Edit` class instead of using operators
* Native scratchattach support

#### Bug Fixes
* None for now...

#### Graceful Deprecation cycle 1.4.0
* None for now...

---

### kms-semver1.5.0
- **Projected Stable Release Date: 2027/06/30**
- **Projected Alpha 0 Release Date: 2027/03/31**

*Stable Release tag: `v1.5.0.20270630`*

#### Features
* Multiple file format support (`.json`, `.yaml`, `.yml`)
* YAML parsing and editing
* Find custom UUIDv7 library so that no fallback to UUIDv4 is necessary
* Allow choosing type of UUID as the instance ID
* Begin shift to 2.0

#### Bug Fixes
* None for now...

#### Graceful Deprecation cycle 1.5.0
* None for now...

---

### kms-semver1.6.0
- **Projected Stable Release Date: 2028/01/08**
- **Projected Alpha 0 Release Date: 2027/10/05**

*Stable Release tag: `v1.6.0.20280108`*

> [!caution]
> This will be the last update in the `kms-semver1.x` series. If you are still using this series of updates by then, you should switch over to `kms-semver2.x` instead.

#### Features
* Begin deprecation and LTS/EOS of kms-semver1.x series

#### Bug Fixes
* None for now...

This update will not have a deprecation cycle.

---

### `kms-semver2.0.0`
- **Projected Stable Release Date: 2027/08/17**
- **Projected Alpha 0 Release Date: 2027/06/14**

*Stable Release tag: `v2.0.0.20270817`*

**kms-semver2.0.0 is an upcoming, backwards-incompatible update planned for release on August 17th, 2027, exactly two years after the release of kms-v1.0.0/2026.08.17.**
This update will bring many changes and features, including the ability to store and read JSON data with SQL querying, store data in YAML files, `MultiStorage` which makes nesting `Storage` in `Storage` easier and more Pythonic, and more. All of these features will be built up slowly in the kms-semver1.x releases leading up to this version.

> [!Note]
> These lists is incomplete. As time passes and the release gets closer, more things will be added in the lists below.

> [!important]
> `kms-semver2.0.0` will be built off of a version of `kms-semver1.5.0`, though this may not matter because the library will have a complete rewrite.

> [!warning]
> These are all planned features and projected (breaking) changes; they are not guaranteed to make it into the final release.

#### Breaking Changes

- **Module name changes**: Import `kms` to use the library, and `kms.storage` for `Storage`.

```py
# before v2.0.0
import key_multivalue_storage as kms
from key_multivalue_storage import Storage
# after v2.0.0
import kms
from kms.storage import Storage
```

- **Explicit submodule import style**: When importing classes, the format `from kms.<module> import <class>` will be used.

- **Implementation of `__slots__`**: By implementing `__slots__`, `kms` can be more lightweight and reduce memory footprints in especially MASSIVE `Storage` instances.

#### New Features

##### `MultiStorage`
`MultiStorage` will be a new class that takes the original `Storage` object a step further, **allowing for *key-multivalue pairs INSIDE a key-multivalue pair*!**

The original Storage object only supported this:
```json
{
    "key1": {
        "subkey1": "val1",
        "subkey2": "val2"
    }
}
```
To store another key-multivalue pair, you would've needed a `Storage` object passed in another's `**kwargs` argument to allow that, which would have been very messy.

`MultiStorage` makes that easier by taking in an arbitrary number of Storage arguments and combining them behind-the-scenes to allow key-multivalue pairs in a key-multivalue pair.

```py
from kms.storage import MultiStorage
# Currently, MultiStorage's usage is planned to look like this
MultiStorage(top_lv_key, *storages, **kwargs)
# When typing in this...
MultiStorage("key1", Storage("subkey", subsubkey="val1", subsubkey2="val2"), subkey2="val3")
```
It would return a `MultiStorage` instance. You can then cast it to a `dict`, which would make it look like this:
```json
{
   "key1": {
        "subkey": {
            "subsubkey": "val1",
            "subsubkey2": "val2"
        },
        "subkey2": "val3"
    }
}
```

#### Important Changes

##### Method Refactorization

**Lots of methods will be getting complete refactors.** What I mean is that for some methods, their arguments will no longer be positional-based, **meaning you must type out the whole argument name and equals to set it.** One planned method that will have this change is `Delete.all()`.

```py
class Delete(metaclass=meta._DeleteMeta):
    ...
    # Old method signature
    def all(file_path: str, warn: bool=True) -> None: ...

# This meant you could call the arguments by position as well.
Delete.all("my_file.json", False)
```

```py
class Delete(metaclass=meta._DeleteMeta):
    ...
    # New method signature
    def all(file_path: str, *, warn: bool=True) -> None: ...

# In kms-semver2.0, you **have** to type `warn=` for this to work.
Delete.all("my_file.json", warn=False)
```

Another, proposed by [**#74**](https://github.com/Boss-1s/key_multivalue_storage/issues/74), has nothing to do with arguments, but with the underlying logic of the method itself. Instead of returning `self.values` when using the `with` keyword, we would instead return the whole `Storage` object - effectively replacing the deprecated `auto_delete_self` attribute and `Storage.store(instant_delete: bool)` argument.

These types of refactorizations - whether it's argument positioning, logic, or just a tweak of a variable name - will prove how each change makes kms more and more **memory-efficient** and **lightweight**.

See all other new features in the [release notes](/Boss-1s/key_multivalue_storage/releases).
