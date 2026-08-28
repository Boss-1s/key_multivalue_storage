# Development

**Before contributing to this library, it is crucial that you read the [contribution guidelines](https://boss-1s.github.io/key_multivalue_storage/contribution-guidelines), to ensure max preparation before contributing anything.**

## Keywords

There are several important vocabulary words you might want to tuck in your back pocket when contributing to kms.

- **kms** - Abbreviation of this library, `key_multivalue_storage`. Also the recommended import alias.
- **py** - Refers to Python.
- **CI/CD** - **Continuous Integration and Continuous Deployment**. This is a development strategy where one automates the software development lifecycle, moving code from development to production securely and efficiently.
- **`gh`** - Refers to Github.
- **`semver`** - Short for 'Semantic Versioning'. [See more about `semver` here.](https://semver.org/)
- **`calver`** - Short for 'Calendar Versioning'. [See more about `calver` here.](https://calver.org/)
- **feat** - Short for 'feature'.
- **CPython** - Regular, trusty ol' Python. This is the Python language we are all familiar with.
- **`top_lv_key`** - Top level key. In kms, the top level key is the key in which all data is nested under (the '*Key*' in '*Key* to Multivalue Storage').
- **`val`** - Value. In kms, this usually refers to the '*Multivalue*' in 'Key to *Multivalue* Storage'.
- **`subkey`** or **`propkey`** - Subkey/Property Key. In kms, this is the key part of the key-value pair nested under a top level key (The key-value pair is the '*Multivalue*' in '*Key* to Multivalue Storage'.)
- **`subval`** or **`propval`** - Sub-value/Property Value. In kms, this is the **value** part of the key-value pair nested under a top level key (The key-value pair is the '*Multivalue*' in '*Key* to Multivalue Storage'.)

```jsonc
{
    "my_data": { // "my_data" is the top level key.
        "foo": 10, // "foo" is the subkey here.
        "bar": -10 // -10 is the sub-value here.
    }
}
```

*All of this is stored within the Storage object collectively:*

```py
from key_multivalue_storage import Storage

Storage("my_data",
        foo=10,
        bar=-10,
)
```

## Project Branches & Release Logic
This repo has a couple branches. Each branch focuses on a specific minor version of kms. You can tell which minor version it focuses on by looking at the branch name. For example, the branch 'semver1.2.x' focuses on updates to `kms-semver1.2.x...`. Versions that have reached EOL will be named as `eol/semver...`. Legacy versions like `kms-v1.2/2026.01.04` will be named as `releases/v[PyPi Version]`. Otherwise, each branch will receive updates as usual. **The default branch will be either a) the stable branch, if development for the next major/minor version has not yet started, or b) the *unstable* development branch, if the (new) branch has been created and development has started.**

Nightly builds will **ALWAYS** be available for each branch.

### Release Cycles

*Related: [Releases](https://boss-1s.github.io/key_multivalue_storage/security#releases)*

#### Minor Patches
Minor patches are never scheduled. They are only released when a fatal bug is in need of attention and cannot wait until the next major patch.

#### Major Patches

Starting from `kms-semver1.3.0`, **major patches will occur every 5~6 _weeks_.** This, of course, is subject to change, and may be temporarily altered to sync up with other real-life schedules, as in the case of `kms-semver1.3.1` being released **two weeks after `kms-semver1.3.0`** but `kms-semver1.3.2` being released ***eight weeks* after `kms-semver1.3.1`**. I will usually try to match up major patches with the development branch's pre-releases.

#### Minor Updates

Starting from `kms-semver1.3.1`, **minor updates will occur every 5~6 _months_.** Like major patches, this is subject to, what is usually, a temporary change. Each minor update has its own branch, starting from the `kms-semver1.2.x` series (which starts at update `kms-semver1.2.2/2026.05.06b`), which is housed on the branch `semver1.2.x`. **The default branch will be the current stable series's branch until the development branch has reached its first alpha.**

Also, regarding update lifecycles, here is a table showing the usual lifecycle of an update. `kms-semver1.3.x` is used as an example.

| Release | Stage | Allowed | Start Date | Concurrency |
| :---: | :---: | :---: | :---: | :---: |
| v1.3.0a0 | Alpha (Feature) | Everything | 2026/05/23 | v1.2.3 |
| v1.3.0a4 | Alpha (Feature) | Everything | 2026/07/03 | v1.2.4 (2026.07.02) |
| v1.3.0b0 | Beta (Bugfix) | refactors, bugfixes and security updates | 2026/07/21 | --- |
| v1.3.0rc0 | Release Candidate (Stable) | Security updates only | 2026/07/24 | v1.2.5 (Maintenance) |
| v1.3.0 | Stable (Bugfix) | refactors, bugfixes, security updates | 2026/07/30 | --- |
| v1.3.3 | Stable (Bugfix/Security) | bugfixes and security updates ONLY | 2026/10/12 | v1.4.0a0 |
| v1.3.6 | Maintenance (Security) | crtical security updates ONLY | 2027/01/03 | v1.4.0 (stable) |
| v1.3.7 | EOS (End of Support) | nothing, support has ended | 2027/03/31 | v1.5.0a0 |
| v1.3.7 | EOL (End of Life) | nothing, version is no longer available and branch will be locked | 2027/06/30 | v1.5.0 (stable) |

TL;DR **an update is usually supported for about 9-10 months before EOS (starting from pre-release), then removed about 13 months after its first pre-release (or 11 months after its first stable release).**

### PR Rules

When creating a pull request against a head branch in kms, there are a few rules that must be followed, or the PR may be rejected.

- **All AI usage must be disclosed.** This is also stated clearly in the Contribution Guidelines - if your code smells of AI, and there is no disclosure about it, your PR will be *manually rejected and **closed**.*
- **Always link to an issue.** It is important to always link your PRs to an issue. If you attempt to create a PR without linking to an issue, it will be automatically rejected and closed. *To ensure it stays open, create an issue first, then link your PR back to the newly created issue with development keywords.*
- **Follow branch naming conventions.** To ensure formality in this repo's environment, I kindly ask that branches be named by the following convention: `[Conventional Commit Category]/[Head Branch]/[Issue Number]`. For example, `fix/semver1.3.x/80`. This way, anyone can know the type of PR, the HEAD, and the issue it links to - just by reading the branch name.

> [!caution]
> If a PR is not assigned a priority or does not have a `Needs Triage` tag, **that PR has not been reviewed and/or was forced reopened.** Do *not* trust, download, install, or test these PRs; let the maintainers handle them.

[**Learn more about the versioning system**](security#official-versioning)

[**Learn about supported versions**](security#supported-versions)

## Installing the development pre-commit hook (kms-semver>=1.3.0a4)

**Clone the repo:**
```sh
git clone -b v1.3.0.20260724rc0 https://github.com/Boss-1s/key_multivalue_storage kms
```

**Or, if you wish, you can fork this repo and create a codespace.**

`cd` into the created folder, create a .venv (if you haven't already) and install the hook:
```sh
cd kms
uv sync --dev
pre-commit install
```

## Running all tests at once (kms-semver>=1.3.0a4)

**Clone the repo**:
```sh
git clone -b v1.3.0.20260724rc0 https://github.com/Boss-1s/key_multivalue_storage kms
```

**Or, if you wish, you can fork this repo and create a codespace.**

`cd` into the created folder, sync your venv, then run the test command:
```sh
cd kms
uv sync --dev
python test/
```
_This may change in the near future, perhaps with a new test library in the first beta._

> [!note]
> If you forked the repo and opened a codespace instead of cloning, don't run the `cd` commands.

### `python test/ <arg>` (kms-semver>=1.3.0b0)

Aside from running all tests, you can also pass arguments to run a specific test. **This will be actively developed to be easier to use.**

#### Available Arguments

> [!note]
> All of the arguments listed below are case-insensitive.

- [`a`/`all`](#aall)
- [`general`](#general)
- [`meta`](#meta)
- [`exceptions`/`warnings`](#exceptionswarnings)
- [`diff`/`diff2`](#diff)
- [`help_shortcut`](#help_shortcut)
- [`reset_env`](#reset_env)


#### `a`/`all`

**Syntax: `python test/ a` or `python test/ all**

Passing the argument `a` or `all` runs all main tests. It produces the exact same result as passing no arguments at all.

#### `general`

**Syntax: `python test/ general`**

Passing the argument `general` will **execute the test `test/test-general.py`**. No other tests will be run. This test is a general test that ensures that class `Storage` and its methods and other classes (`Load`, `Edit`, `Delete`) and their methods work properly. **It does not check smoothness, speed, or Pythonicity; it only ensures everything works.**

#### `meta`

> [!important]
> This test is still being developed and finished. It is not robust yet, please try not to rely on it. 

**Syntax: `python test/ meta`**

Passing the argument `meta` will **execute the test `test/test-meta.py`. No other tests will be run. This test is a targeted test designed to ensure the new `help()` functions work and that the new metaclasses are in order and working.

#### `exceptions`/`warnings`

**Syntax: `python test/ exceptions`**

* Alternate Syntax: `python test/ warnings`*

Passing the argument `exceptions` or `warnings` will **execute the test `test/test-exceptions.py`. No other tests will be run. This test is a targeted test designed to ensure all exceptions and warnings exist, are working properly, and are exposed to the top level of the library.

#### `diff`

> [!important]
> This test requires a second argument.

**Syntax: `python test/ diff <OLDTAG>`**

*Alternate Syntax: `python test/ diff2 <OLDTAG> <NEWTAG>`*

**Example Usage: `python test/ diff my_version_tag` | `python test/diff2 "v1.0" "v2.0"`**

Passing the argument `diff` will run the program `test/diff.py`. No other tests will be run. This program helps find breaking changes in your current working directory by comparing it against a Git tag, commit SHA, or branch, using Griffe. This Git tag/commit/branch must be passed as a second argument. (See example usage above)

Passing `diff2` runs the same thing, except it does not compare against your working directory and you will have to provide a Git tag/commit/branch as the third argument.

#### `help_shortcut`

> [!warning]
> This test may be removed or renamed in the near future.

**Syntax: `python test/ help_shortcut`**

Passing the argument `help_shortcut` will run the following code snippet:
```py
import key_multivalue_storage as kms
kms.help()
```
No other tests will run. This test is a targeted test to ensure that the library's main `help()` method is visually correct by human determination.

#### `reset_env`

**Syntax: `python test/ reset_env <SSH_USER> <SSH_EMAIL> <SSH_PRIVATE_KEY> [reconfig_ssh_key_clearall=false]`**

**Example Usage: `python test/ reset_env foo example@example.com "$SSH_PRIVATE_KEY" true`**

Passing the argument `reset_env` will run all automations within the directory `test/automation/.vscode_rebuild/`. As of `kms-semver1.3.0rc1`, this directory contains the following automations:

- **reconfigure_ssh_key.sh**
- **reinstall_extensions.py**

This is especially useful when developing `kms` in VSCode, and you want the full and complete experience.

> [!warning]
> Surround your SSH key in double quotes to prevent parsing errors.

> [!important]
> Because `kms` requires signed commits, you must pass your SSH credentials to `reset_env`; otherwise, it will not run.

> [!tip]
> Using GPG? GPG key signing has not exactly been implemented into the development workspace yet. However, when it does, all you have to do is run `reset_env` and pass your GPG key credentials in place of the SSH key credentials.
