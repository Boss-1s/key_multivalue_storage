> [!note]
> Note that each main class and module **has a help() method**, accessible via `<class/module>.help()`. These `help()` methods are simply docstring printers and hinters, so they will not be touched on in this documentation.

# `load.py`

This module houses the `Load` class, a helper class that loads JSON objects stored with `Storage.store()` back into `Storage` objects.

## Structure of the Module

> [!tip]
> Click on a class or method below to go straight to its documentation!

- `load.py` — loading helpers (Load class)
  - [`Load`](#storage-load)
	  - [`by_key`](#storage-load-by-key)
	  - [`by_index`](#storage-load-by-index)
	  - [`keys`](#storage-load-keys)
	  - [`values`](#storage-load-values)

## `Storage.Load`

### Methods

#### `Storage.Load.by_key()`

```py
@classmethod
def by_key(cls,
           file_path: str,
           key: Any,
           raw: bool=False
          ) -> Storage | None:
```

Load a json file and find the key to extract
a single key-multivalue pair and its values.

##### Arguments

| Symbol | Type Hint | Default | Description |
|----|----|----|----|
|`file_path`|`str`|Required|Path to JSON file.|
|`key`|`Any`|Required|Top-level key to search for (strings recommended).|
|`raw`|`bool`|`False`|If `False` attempt to decode encoded values; if `True` return raw stored values.|

##### Output

- `Storage`: Returns a Storage object containing the loaded data if found.
- `None`: Returns None if the key was not found or if there was an error.

##### Example

```py
s = Storage.Load.by_key("db.json", "users")
print(repr(s))
```

---

#### `Storage.Load.by_index()`

```py
@classmethod
def by_index(cls,
             file_path: str,
             index: int,
             raw: bool=False
            ) -> Storage | None:
```

Load a json file and find the index at which to
extract a single key-multivalue pair and its values.

Do note that this method bases the start index at 0.

##### Arguments

| Symbol | Type Hint | Default | Description |
|----|----|----|----|
|`file_path`|`str`|Required|Path to JSON file.|
|`index`|`int`|Required|0-based index of top-level key to return.|
|`raw`|`bool`|`False`|If `False` attempt to decode encoded values; if `True` return raw stored values.|

##### Returns

- `Storage`: If sucessful, a Storage object will be returned with the loaded data.
- `None`: Only returned on failure to load the file or if the index is out of bounds.

##### Example

```py
```

---

#### `Storage.Load.keys()`

```py
@classmethod
def keys(cls,
         file_path: str
        ) -> list[str] | None:
```

Load a json file and returns the keys of that file.

##### Arguments

| Symbol | Type Hint | Default | Description |
|----|----|----|----|
|`file_path`|`str`|Required|Path to JSON file.|

##### Returns
- `list[str]`: A list containing strings of the top level keys in the loaded JSON file.
- `None`: May return None on error or if no keys were found.

##### Example

```py
```

---

#### `Storage.Load.values()`

```py
@classmethod
def values(cls,
           file_path: str,
           key: Any,
           keys: bool=False,
           raw: bool=True
          ) -> list[str] | None:
```

Loads a json file and returns the values under the inputed key.

Unlike other loading methods, this one returns the raw values by default.

Keys can also be returned as a key-value pair if keys=True.

##### Arguments

| Symbol | Type Hint | Default | Description |
|----|----|----|----|
|`file_path`|`str`|Required|Path to JSON file.|
|`key`|`Any`|Required|Top-level key to fetch values for.|
|`keys`|`bool`|`False`|If `True`, returns `["prop: value", ...]` strings; otherwise returns list of values.|
|`raw`|`bool`|`True`|If `True`, return raw stored values (no decode). If `False`, attempt to decode encoded ints.|

##### Returns
- `list[str]`: A list containing the values under the specified key in the loaded data. If `keys=True`, then the list will contain key-value pairs in the format "key: value".
- `None`: Returns None if the key was not found or if there was an error.

##### Example

```py
```

### Other Info

- This class cannot be instantiated. Attempting to do so will raise [`kms.NoInstantiationError`](#kmsnoinstantiationerror).
- Aside from `Storage`, this is the only class with [a] method(s) that return(s) a `Storage` object.
<!--stackedit_data:
eyJwcm9wZXJ0aWVzIjoiZXh0ZW5zaW9uczpcbiAgcHJlc2V0Oi
BnZm1cbiIsImhpc3RvcnkiOlsxODc4MjE5NDY0XX0=
-->