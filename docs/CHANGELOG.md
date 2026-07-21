# Changelog

## 📦 v1.3.0.20260721b0 — *kms-v1.3.0beta0/2026.07.21*

⚙ **Target Node Commit:** `a0871f01`
📝 **Release Type:** Pre-release - Minor Patch

### What's Changed

#### Repo Updates
- **New dev dependency:** GitPython (gitpython-developers/gitpython)
> [!note]
> This dependency makes the precommit process more robust.
- Precommit script updated via 820ca69
#### Module Updates 
- updated [\_\_init__.py](https://github.com/Boss-1s/key_multivalue_storage/blob/454634b0eea295ae78cb53d03cfb3174646e4b50/src/key_multivalue_storage/__init__.py) to include all `load.Load` methods and classes in the library tree
- Refactored all docstrings in load.py
- Added `help()` function in `load.Load`
- diff.py: third-party import should be after first-party import fixed
- test-meta.py: bumped to `t-meta-kms-v2026.7.1`
#### Dependency updates
* chore(deps): bump actions/setup-python from 6 to 7 by @dependabot[bot] in https://github.com/Boss-1s/key_multivalue_storage/pull/16
* chore(deps): bump reviewdog/action-actionlint from 1.72.0 to 1.72.1 by @dependabot[bot] in https://github.com/Boss-1s/key_multivalue_storage/pull/19

#### Notes
None.

#### Plans for next update
Looks like I'm going to be on a tight schedule here...

I'm going to be releasing one more beta on the 23rd, which should include docstring updates related to the storage module and delete module. After that, a little sparkle and cleanup is left before moving on to the release candidate stage, which is set to release as `v1.3.0.20260724rc0` on July 24th. As a reminder, the **final release is scheduled for _July 27th_, with a backup date of _July 30th_ in case things don't go as planned, giving me _three emergency days_.**

**Full Changelog**: https://github.com/Boss-1s/key_multivalue_storage/compare/v1.3.0.20260703a4...v1.3.0.20260721b0

---

## 📦 v1.3.0.20260703a4 — *kms-v1.3.0a4/2026.07.03*

⚙ **Target Node Commit:** `e658778d`
📝 **Release Type:** Pre-release - Minor Patch

### What's Changed
#### Repo Updates
##### Cherry-picked commits
0fff779, fa0924a, 546d497, 1c0d4d3, db4ac9c, 3be3602, 49645dc, 625cc38, 892c427, d9614ad, 4de3e08, cb36289, 0e1324f, df782e8, 67da837, d21b83d, 9eaabfb, 95af72e, 3456bf8, and possibly more....
_See more info about these commits and thier purpose at [`v1.2.4.20260703`](https://github.com/Boss-1s/key_multivalue_storage/releases/v1.2.4.20260703)_
##### Other Changes
- fixed: use same time format as main (df782e8)
- fixed: pass NIGHTLY env var (df782e8)

**All other repo related updates were released as part of [`v1.2.4.20260703`](https://github.com/Boss-1s/key_multivalue_storage/releases/v1.2.4.20260703).**
#### Module Updates 
- **New official dependencies:** `rich` (>=15.0.0) and `typing-extension` (~=4.15)
- **New dev dependency:** `precommit` (>=4.6.0)
- Small Pylint settings tweaks
- `release.py` now resides in `./test/automation`
- Partial implementation of Rich throughout the library; expect Rich to completely replace native `print()` and other `stdout`-related methods by `kms-semver1.4`
- Added `tmp/` to `.gitignore`
##### In __init__.py:
- Module docstring refactored
- `__all__`
- Commented out v1.x discontinuation for later
- Partially implemented help() function at the library scope
##### In storage.py (formerly key_multivalue_storage.py):
- Classes `Load`, `Edit`, `Delete` have been moved out into their respective modules (`load.Load`, `edit.Edit`, `delete.Delete`). They are still accessible through `Storage` in the context `Storage.<subclass>`; however, from v2.0 onward, they must be accessed through `<module>.<class>`. See docs for more info.
- `help()` implemented
##### Exceptions (utils/exceptions.py)
- New exception `NoInstantiationError(TypeError)`, used when attempting to instantiate an non-instantiable class (like `Storage.Load`)
- Docstring refactored
##### Metaclasses (utils/metadata.py)
- New metaclasses `_KmsMeta`, `_StorageMeta`, `_LoadMeta`, `_EditMeta`, `_DeleteMeta`
- Other than `_KmsMeta`, each metaclass contains semver, calver, last_update properties and a __repr__ method.
- `_StorageMeta` still contains the legacy VERSION, DATE_VERSION, and LAST_UPDATE to prevent breaking changes.
##### Warnings (utils/warnings.py)
- Docstring refactored
##### Tests (./test/)
- New test: `test-meta.py` -- Used to test repr implementation of classes via metaclass and the help() methods
- New folder: `test/automation` -- storing automation-related modules in there
- New automation: `release.py` -- moved from ./.github/workflows/src to ./test/automation
- Also completely refactored and cleaned up the whole release file (49645dc)
- New automation: `precommit.py` -- precommit job (changing last update dates for now...)
- To install this new precommit hook:
**Clone the repo:**
```sh
git clone -b beta https://github.com/Boss-1s/key_multivalue_storage kms
```
**`cd` into the created folder, create a .venv (if you haven't already) and install the hook:**
```sh
cd kms
uv sync
pre-commit install
```
_**See docs for more info.**_
- You can now run all tests from kms easily via one command whilst in development.
To run the tests:
**Clone the repo**:
```sh
git clone -b beta https://github.com/Boss-1s/key_multivalue_storage kms
```
`cd` into the created folder, then run the test command:
```sh
cd kms
python test/
```
_This may change in the near future, perhaps with a new test library in the first beta._
_**See docs for more info.**_
> [!WARNING]
> When tests are running on Windows, specifically the legacy `cmd.exe` shell, tests WILL fail due to a Unicode encoding error. See #14 for more details.
#### Dependency updates
* chore(deps): bump actions/checkout from 6 to 7 by @dependabot[bot] in https://github.com/Boss-1s/key_multivalue_storage/pull/10
* chore(deps): update typing-extensions requirement from ~=4.15 to ~=4.16 by @dependabot[bot] in https://github.com/Boss-1s/key_multivalue_storage/pull/13 and e658778

#### Plans for next update
Finally.

The final alpha release is here.

The plan right now is two betas and a release candidate, with the official release coming on July 27th. Expect the first beta sometime next week; it's most likely going to be a smaller release compared to the feature-and-fix-packed alphas we've had.
Side note: **Feature Freeze does not begin until kms-semver1.3.0rc0.**

**Full Changelog**: https://github.com/Boss-1s/key_multivalue_storage/compare/v1.3.0.20260610a3...v1.3.0.20260703a4

---

## 📦 v1.3.0.20260610a3 — *kms-v1.3.0-alpha3/2026.06.10*

⚙ **Target Node Commit:** `8b48b591`
📝 **Release Type:** Pre-release - Minor Patch

### What's Changed
#### Repo Updates
##### Cherry-picked commits
* A lot of commits from [`main`](https://github.com/Boss-1s/key_multivalue_storage/blob/main) were cherry-picked this time. Most of the commits were really related to fixing the release version commit bug (see [`v1.2.3.20260605.4`](https://github.com/Boss-1s/key_multivalue_storage/releases/tag/v1.2.3.20260605.4))
###### Commits cherry-picked _without_ conflict resolution 
33855ad, e4e8664, 12757f8, 2675284, a6a9ed3, bf6607a, b41c207, b871b5f, 4650290, eee9e56, 317da7d, 2630c0a, bb4f049, 26f4b71, e3de61a, 3ac9e17, 0f39c93, f375b1c, 78432d2, b58e724, d3ed467, 74d0422, 49808dc, d0ffda8, 29505b7, 2012ac1, dc57b97, a32ac32, 128e343, 9d26dfa, fed084c, fe75f15, 5a23676, cff3bad, 60d3048, aa1013f, b7098d8, 29029e5, e763214, 779e3c4, 4c9c4b0, b633311, e5b68bd, e458e95, 9415ca9, ed890a5, 7da66b1, 41444b8, 5faa9cc, 623ec76, 9286038, e988c85, fdef67b, a353b75, 84954ac, 9fdbab8, bd6b4cb, 99ec8ff, 23dd58c
###### Commits cherry-picked **with** conflict resolution
> This basically means that the cherry-picked commits have a small difference from the original commit.

34dd62c, 0abbb2a, 0ea7bac, d650ae6, e0d0145, 0c0f325, 40312c7, 799e1bc, b8bc5ff, 5d08a72, cace704, 19c9477, bd9a4c0, 2d969c2, 5b45ae6, 58fd625, 002c7c2, d1a1be5, bb799a4, 7aca59a, 40fe7a5, a7444cb, 249896d, 6125ed0, e62ea4a
##### Other Changes
> I put version numbers next to changes from upstream versions; however, this doesn't mean that `kms-semver1.3` is sourced from these changes.

* Added extension [`fanaticpythoner.better-todo-tree`](https://github.com/FanaticPythoner/better-todo-tree) in [`devcontainer.json`](.devcontainer/devcontainer.json)
* Refined bug report template ([`v1.2.3.20260605`](https://github.com/Boss-1s/key_multivalue_storage/releases/tag/v1.2.3.20260605))
* **Feature Request template!** ([`v1.2.3.20260605`](https://github.com/Boss-1s/key_multivalue_storage/releases/tag/v1.2.3.20260605))
* **Dependabot watches and updates dependencies on `beta` now, too**
* Dummy release to test release logic ([`v1.2.3.20260605`](https://github.com/Boss-1s/key_multivalue_storage/releases/tag/v1.2.3.20260605))
* **Nightly builds now release every push, no matter where the push occurs.**
* **_Release version change commit fixed! ([`v1.2.3.20260605.4`](https://github.com/Boss-1s/key_multivalue_storage/releases/tag/v1.2.3.20260605.4))_**
* `otest.json` AND `.github/.tmp` added to `.gitignore`
* README updates
* **Contribution Guideline updates** ([`v1.2.3.20260605`](https://github.com/Boss-1s/key_multivalue_storage/releases/tag/v1.2.3.20260605))
* [`uv.lock`](uv.lock)
* [`diff.py`](test/diff.py) update
#### Module Updates 
So many updates related to the package itself...let's get started!
##### [`__init__.py`](src/key_multivalue_storage/__init__.py)
* Triple-quote docstring (which tbh is not much of a docstring lol)
* Move `import warnings` to before module relative imports (see **[PEP 328](https://peps.python.org/pep-0328/)**
##### [`delete.py`](src/key_multivalue_storage/delete.py), [`edit.py`](src/key_multivalue_storage/edit.py), and [`load.py`](src/key_multivalue_storage/load.py)
* Created files to prepare for the next alpha release
##### [`utils/exceptions.py`](src/key_multivalue_storage/utils/exceptions.py)
* Created file
* **This module stores all custom Exceptions used by other modules.**
* Added new custom exception `KeyNotFoundError(KeyError)`
##### [`utils/metadata.py`](src/key_multivalue_storage/utils/metadata.py)
* Created file
* **This module stores the metaclasses for source modules.**
* Added new metaclass `_StorageMeta`
* _This module will receive more refactoring in the next alpha release._
##### [`utils/warnings.py`](src/key_multivalue_storage/utils/warnings.py)
* Created file
* **This module stores all custom warnings used by other modules.**
* Added new warning classes:
```py
DeleteWarning(UserWarning)
AdditionFailureWarning(RuntimeWarning)
SubtractionFailureWarning(RuntimeWarning)
CastWarning(SyntaxWarning)
```
* _This modules will receive more refactoring in the next alpha update._
##### [`key_multivalue_storage.py`](src/key_multivalue_storage/key_multivalue_storage.py)
- Moved metaclass(es) (`_StorageSettingsMeta` or `_StorageMeta`), warning(s) (`DeleteWarning`, `AdditionFailureWarning`, `SubtractionWarning`, `CastWarning`), and exception(s) (`KeyError`) into thier respective modules in `utils/`
- Lots of prettifying
- Comment fixes
- Fixed all linting ERRORS
- Pylint: 9.55 to 9.68 out of 10 (couldn't get 9.67 sadly lol)
- Removed __is_warning_category_ignored
- Implemented checking for warning category ignorance directly in the method `Storage.Delete.all()`
- Some docstring fixes...like two of them lol
- Fixed `warn` argument inconsistency in `Storage.Delete.all()`

Is it just me, or is everything revolved around bugs from the `Delete` class...
#### Dependency updates
* build(deps): bump astral-sh/setup-uv from 5 to 7 by @dependabot[bot] in https://github.com/Boss-1s/key_multivalue_storage/pull/8
* build(deps): bump oprypin/find-latest-tag from 1.1.2 to 1.1.3 by @dependabot[bot] in https://github.com/Boss-1s/key_multivalue_storage/pull/7

#### Notes
This was supposed to be release _v1.3.0.**20260608**a3_, however I found out (a bit too late) that the release built on `main` for some reason, so I'm rereleasing it with the **CORRECT** branch on target...

#### Plans for next update
It's been two weeks since the last alpha, but this one is finally here. So much effort to fix something upstream just so I could finally release this...
I believe that after this, we will see one more big alpha release. That release will mainly contain the separation of the `Load`, `Edit`, and `Delete` classes from `Storage`, along with separate metadata for each of these classes. After that comes the beta releases, which will have small fixes, tweaks, native Pylint support, and definitely NO breaking changes. Hopefully, we'll only need one release candidate before the actual `kms-semver1.3.0` update.

That's it, folks!

**Full Changelog**: [`v1.3.0.20260524a2` vs `v1.3.0.20260610a3`](https://github.com/Boss-1s/key_multivalue_storage/compare/v1.3.0.20260524a2...v1.3.0.20260610a3)

**YANKED**: `v1.3.0.20260608a3`

---

## 📦 v1.3.0.20260524a2 — *kms-v1.3.0a2/2026.05.24*

⚙ **Target Node Commit:** `f5cb3356`
📝 **Release Type:** Stable Promotion

### What's Changed
#### Repo Updates
* feat: use github-actions bot for signatures
#### Module Updates 
* None this time :)
#### Dependency updates
* None this time ;)

#### Plans for next update
The next alpha with major changes will be released in a week, with the last major alpha in two or three weeks. The next big change will be separating the classes into different modules. I will try my best to keep breaking changes to a minimum, but no promises can be made lol. Other things that need to be done is fixing type hint warnings and conflicts, and obviously, fixing the docstrings, which is the main point of the update, after all.

**Full Changelog**: https://github.com/Boss-1s/key_multivalue_storage/compare/v1.3.0.20260524a1...v1.3.0.20260524a2

---

## 📦 v1.3.0.20260524a1 — *kms-v1.3.0-alpha1/2026.05.24*

⚙ **Target Node Commit:** `51583499`
📝 **Release Type:** Pre-release - Minor Patch

### What's Changed
#### Repo Updates
* **Main reason for this release is hoping that the auto version commit gets fixed**
* feat: auto-version commit (f040b8a, 5158349)
* feat: uv for testing (58fd625)
#### Module Updates 
* None this time :)
#### Dependency updates
* None this time ;)

#### Notes
If this doesn't work you'll most likely see another alpha release today...

#### Plans for next update
The next alpha with major changes will be released in a week, with the last major alpha in two or three weeks. The next big change will be separating the classes into different modules. I will try my best to keep breaking changes to a minimum, but no promises can be made lol. Other things that need to be done is fixing type hint warnings and conflicts, and obviously, fixing the docstrings, which is the main point of the update, after all.

**Full Changelog**: https://github.com/Boss-1s/key_multivalue_storage/compare/v1.3.0.20260523a0...v1.3.0.20260524a1

---

## 📦 v1.3.0.20260523a0 — *kms-v1.3.0-alpha0/2026.05.23*

⚙ **Target Node Commit:** `002c7c21`
📝 **Release Type:** Pre-release - Minor Update

omg its finally here!!! :>

### What's Changed
#### Repo Updates
* **See [v1.2.3.20260523](https://github.com/Boss-1s/key_multivalue_storage/releases/tag/v1.2.3.20260523) for some updates, as that update's contents were merged into this one's.**
* Added badge links in Readme
* Fixed false info in Readme and wiki
* Fixed minor grammar and spelling errors in documentation (wiki, readme, security guide)
* [Bug Report template](https://github.com/Boss-1s/key_multivalue_storage/blob/main/.github/ISSUE_TEMPLATE/bug_report.yml)
* [CODEOWNERS](https://github.com/Boss-1s/key_multivalue_storage/blob/beta/docs/CODEOWNERS)
* [Release template](https://github.com/Boss-1s/key_multivalue_storage/blob/beta/docs/release-template.md)
* Nightlys for both `main` and `beta` branches!
* Griffe and Pylint are both optional dependencies in v1.3
* New test file: [`diff.py`](diff.py) - shows all breaking changes
#### Module Updates 
##### In key_multivalue_storage:
* **Breaking changes between kms-semver1.3.0 and kms-semver1.20260506.2 include the following:**
* _The `key` value of a `Storage` instance is now set to type `Any`. However, it is still recommended that the value be a string to avoid string-casting errors._
* _The `top_level_key` parameter of [`Storage.Delete.by_propkey`](https://github.com/Boss-1s/key_multivalue_storage/blob/beta/src/key_multivalue_storage/key_multivalue_storage.py#L694) is now called `top_lv_key`_
* [_Renamed all metadata_](https://github.com/Boss-1s/key_multivalue_storage/wiki/Roadmap#breaking-changes-in-kms-semver13)
* **Raised PyLint score from 0.00 to 9.95!**
* Removed \_\_all__ (only rely on \_\_all__ in \_\_init__.py from now on)
* Removed all trailing whitespace
* Ensured all lines were under 100 chars
* Removed all unnecessary indentation
* Changed all indentation to be spaces instead of tabs (pylint was giving nightmares about that)
* Added TODO comments
* Completely commented out unfinished logger
* Fixed like 30% of docstrings
* Prettified like 70% of the module
* Other stuff that I could not find lol
##### In \_\_init.py__:
* Added `PendingDeprecationWarning` about module name deprecation
* Added `PendingDeprecationWarning` about `kms-semver1.x` deprecation
#### Dependency updates
* None this time

#### Plans for next update
Damn, did this take long. I got it finished in the end, didn't I?

Looks like the next alpha will be released in a week, with the last alpha in two or three weeks. The next big change will be separating the classes into different modules. I will try my best to keep breaking changes to a minimum, but no promises can be made lol. Other things that need to be done is fixing type hinting warnings and conflictions, and obviously, fixing the docstrings, which is the main point of the update, after all.

**Note that kms-semver1.3 will now be officially designated as built from [`v1.2.3.20260523.1`](https://github.com/Boss-1s/key_multivalue_storage/releases/tag/v1.2.3.20260523.1).**

**Full Changelog**: [`v1.2.2.20260517.3` vs `v1.3.0.20260522a0`](https://github.com/Boss-1s/key_multivalue_storage/compare/v1.2.2.20260517.3...v1.3.0.20260522a0)

---

## 📦 v1.2.4.20260702 — *kms-v1.2.4/2026.07.03*

⚙ **Target Node Commit:** `5710f8a7`
📝 **Release Type:** Minor Patch

### What's Changed
#### Repo Updates
* **Release workflow is now stable, [thanks to this update!](https://github.com/Boss-1s/key_multivalue_storage/releases/tag/v1.2.4.20260610b0)**
* Changed automated release update commit message and description
* Some `release.py` and `release.yml` refactoring
* Better nightly versioning for both `main` and `beta`
* More transitions to `uv`
* feat: use `dependency-groups` instead of `optional-dependencies` (708d560@beta, ab42dcc@main)
* feat: pin python version (e20a0d6)
* **Documentation website!!!** (https://boss-1s.github.io/key_multivalue_storage)
* All issue templates have `needs triage` as one of the default tags now
#### Module Updates 
* **Pylint Implementation!!~~**
* Removed ALL trailing whitespace
* fix: import `types.TracebackType` (2b3479f)
* **New official dependency**: `typing-extensions` at `~=4.16`
* `typing-extenstions.deprecated` was used over `warnings.deprecated` to keep CPython >=3.12 instead of just chopping off older version just because of an `@deprecated` flag
* Removed random empty `warnings.warn()`
#### Dependency updates
* chore(deps): bump actions/checkout from 6 to 7 by @dependabot[bot] in https://github.com/Boss-1s/key_multivalue_storage/pull/11
* chore(deps): update typing-extensions requirement from ~=4.15 to ~=4.16 by @dependabot[bot] in https://github.com/Boss-1s/key_multivalue_storage/pull/12

#### Plans for next update
Our next few 1.2.4.x updates should see more updates to the [documentation website](https://boss-1s.github.io/key_multivalue_storage), and changes that will pave the way to `1.3.0` **This patch version (`1.2.4`) may be the last one before the release of `kms-semver1.3.0`.**

**Full Changelog**: https://github.com/Boss-1s/key_multivalue_storage/compare/v1.2.3.20260605.4...v1.2.4.20260702

---

## 📦 v1.2.4.20260610b0 — *kms-v1.2.4-beta0/2026.06.10*

⚙ **Target Node Commit:** `de48c51d`
📝 **Release Type:** Pre-release - Major Patch

Testing release logic....

**Full Changelog**: https://github.com/Boss-1s/key_multivalue_storage/compare/v1.2.3.20260605.4...v1.2.4.20260610b0

---

## 📦 v1.2.3.20260605.4 — *kms-v1.2.3/2026.06.05d*

⚙ **Target Node Commit:** `b875965f`
📝 **Release Type:** Stable Promotion

### What's Changed
#### Repo Updates
* Everything from [`v1.2.3.20260605.1`](https://github.com/Boss-1s/key_multivalue_storage/releases/tag/v1.2.3.20260605.1) to here is fixing that damned thing of a commit push...and with this release it's finally fixed. Whew!
* Updated README to have a link to roadmap
#### Module Updates 
* Prettified up to line 343 in `key_multivalue_storage.py`
#### Dependency updates
* None this time ;)

Huge credits to Google's AI Mode for explaining SSH to me so that I could get this done lol 🎉🎉

#### Plans for next update
Our next few 1.2.3.x updates should see more Repo updates, specifically working on the wiki page and other documentation. I am also hoping for some prettifying in the module itself on kms-semver1.2, whilst working on kms-semver1.3.

**Full Changelog**: https://github.com/Boss-1s/key_multivalue_storage/compare/v1.2.3.20260605.1...v1.2.3.20260605.4

Yanked: [`v1.2.3.20260605.2`](https://github.com/Boss-1s/key_multivalue_storage/releases/tag/v1.2.3.20260605.2), [`v1.2.3.20260605.3`](https://github.com/Boss-1s/key_multivalue_storage/releases/tag/v1.2.3.20260605.3)

---

## 📦 v1.2.3.20260605.4b3 — *kms-v1.2.3b3/2026.06.05d*

⚙ **Target Node Commit:** `b7ad7dbc`
📝 **Release Type:** Stable Promotion

so many betas....im praying this'll work.....please....

**Full Changelog**: https://github.com/Boss-1s/key_multivalue_storage/compare/v1.2.3.20260605.4b2...v1.2.3.20260605.4b3

---

## 📦 v1.2.3.20260605.4b2 — *kms-v1.2.3b2/2026.06.05d*

⚙ **Target Node Commit:** `fae9ca15`
📝 **Release Type:** Stable Promotion

Hopefully this works...

**Full Changelog**: https://github.com/Boss-1s/key_multivalue_storage/compare/v1.2.3.20260605.4b1...v1.2.3.20260605.4b2

---

## 📦 v1.2.3.20260605.4b1 — *kms-v1.2.3b1/2026.06.05d*

⚙ **Target Node Commit:** `fae9ca15`
📝 **Release Type:** Stable Promotion

**Full Changelog**: https://github.com/Boss-1s/key_multivalue_storage/compare/v1.2.3.20260605.4b0...v1.2.3.20260605.4b1

---

## 📦 v1.2.3.20260605.4b0 — *kms-v1.2.3b0/2026.06.05d*

⚙ **Target Node Commit:** `a0549a98`
📝 **Release Type:** Pre-release - Minor Patch

**Full Changelog**: https://github.com/Boss-1s/key_multivalue_storage/compare/v1.2.3.20260605.3...v1.2.3.20260605.4b0

---

## 📦 v1.2.3.20260605.3 — *[YANKED] kms-v1.2.3/2026.06.05c*

⚙ **Target Node Commit:** `27cebddb`
📝 **Release Type:** Minor Patch

### What's Changed
#### Repo Updates
* fatal: test mode set to 'true' in real release file :[
#### Module Updates
None this time :}
#### Dependency updates
None this time :]

#### Plans for next update
Our next few 1.2.3.x updates should see more Repo updates, specifically working on the wiki page and other documentation. I am also hoping for some prettifying in the module itself on kms-semver1.2, whilst working on kms-semver1.3.
If release fails again i swear....

**Full Changelog**: https://github.com/Boss-1s/key_multivalue_storage/compare/v1.2.3.20260605.2...v1.2.3.20260605.3

---

## 📦 v1.2.3.20260605.2 — *[YANKED] kms-v1.2.3/2026.06.05b*

⚙ **Target Node Commit:** `de7e3bb3`
📝 **Release Type:** Minor Patch

### What's Changed
#### Repo Updates
* fatal typo: `target_commitish` spelled with two 't's
#### Module Updates
* None this time
#### Dependency updates
* None this time

#### Plans for next update
Our next few 1.2.3.x updates should see more Repo updates, specifically working on the wiki page and other documentation. I am also hoping for some prettifying in the module itself on kms-semver1.2, whilst working on kms-semver1.3.
If release fails again i swear....

**Full Changelog**: https://github.com/Boss-1s/key_multivalue_storage/compare/v1.2.3.20260605.1...v1.2.3.20260605.2

---

## 📦 v1.2.3.20260605.1 — *kms-v1.2.3/2026.06.05a*

⚙ **Target Node Commit:** `77609c6c`
📝 **Release Type:** Minor Patch

### What's Changed
#### Repo Updates
##### Cherry-picked from `beta` branch
* docs/CODEOWNERS
* docs/release-template.md
---
* Small update to Contributing Guidelines (02f6b15)
* Readded release environment to deploy to
* Hopefully fixed the whole "commit version change after release" thing....I will crash out if that doesn't work.
#### Module Updates 
* None this time :)
#### Dependency Updates
* chore(deps): bump webfactory/ssh-agent from 0.9.0 to 0.10.0 by @dependabot[bot] in https://github.com/Boss-1s/key_multivalue_storage/pull/9

#### Notes
Apparently I never uncommented the step for releasing to PyPI so here I am...with a bunch of other fixes. Hopefully, after this is fixed, i won't have to touch the release workflow again until I decide about a possible `CHANGELOG.md`...

#### Plans for next update
Our next few 1.2.3.x updates should see more Repo updates, specifically working on the wiki page and other documentation. I am also hoping for some prettifying in the module itself on kms-semver1.2, whilst working on kms-semver1.3.
If the release fails again i swear....

**Full Changelog**: [`v1.2.3.20260605` vs `v1.2.3.20260605.1`](https://github.com/Boss-1s/key_multivalue_storage/compare/v1.2.3.20260605...v1.2.3.20260605.1)

---

## 📦 v1.2.3.20260605 — *kms-v1.2.3/2026.06.05*

⚙ **Target Node Commit:** `791c8605`
📝 **Release Type:** Minor Patch

### What's Changed
#### Repo Updates
* The `test.yml` workflow will now deploy to its respective head branch's test environment when Dependabot makes a PR
* Hopefully SSH signing is fixed meaning I can commit the version change
* Dummy Release to test if releasing works
* Nightly now releases every push
* **New Contribution Rules!**
* **Bug Report and Feature Request Templates**
#### Module Updates
##### In `key_multivalue_storage.py`:
* Added `DeprecationWarning` to the argument `top_level_key` in `Storage.Delete.by_propkey()`
* Added `DeprecationWarning`s to all metadata variables
* Replaced all tab characters with spaces
* Logging section removed completely
#### Dependency updates
* Bump [astral-sh/setup-uv](https://github.com/astral-sh/setup-uv) from 5 to 7 by @dependabot[bot] in https://github.com/Boss-1s/key_multivalue_storage/pull/5
* Bump [oprypin/find-latest-tag](https://github.com/oprypin/find-latest-tag) from 1.1.2 to 1.1.3 by @dependabot[bot] in https://github.com/Boss-1s/key_multivalue_storage/pull/6

#### Plans for next update
Our next few 1.2.3.x updates should see more Repo updates, specifically working on the wiki page and other documentation. I am also hoping for some prettifying in the module itself on kms-semver1.2, whilst working on kms-semver1.3.
If release fails again i swear....

**Full Changelog**: [`v1.2.3.20260523.1` vs `v1.2.3.20260605`](https://github.com/Boss-1s/key_multivalue_storage/compare/v1.2.3.20260523.1...v1.2.3.20260605)

(Yanked: [`v1.2.3.20260604`](https://github.com/Boss-1s/key_multivalue_storage/releases/tag/v1.2.3.20260604))

---

## 📦 v1.2.3.20260523.1 — *kms-v1.2.3/2026.05.23a*

⚙ **Target Node Commit:** `190cb35e`
📝 **Release Type:** Minor Patch

### What's Changed
#### Repo Updates
* Fixes to `push.sh`
* Main reason for this push is `release.yml` fix
#### Module Updates 
* None this time :)
#### Dependency updates
* None this time :)

#### Plans for next update
Our next few 1.2.3.x updates should see more Repo updates, specifically working on the wiki page and other documentation. I am also hoping for some prettifying in the module itself on kms-semver1.2, whilst working on kms-semver1.3.

**Full Changelog**: https://github.com/Boss-1s/key_multivalue_storage/compare/v1.2.3.20260523...v1.2.3.20260523.1

---

## 📦 v1.2.3.20260523 — *kms-v1.2.3/2026.05.23*

⚙ **Target Node Commit:** `9e3ab939`
📝 **Release Type:** Major Patch

### What's Changed
#### Repo Updates
* Added badge links in Readme
* Fixed false info in Readme and wiki
* Fixed minor grammar and spelling errors in documentation (wiki, readme, security guide)
* [Bug Report template](https://github.com/Boss-1s/key_multivalue_storage/blob/main/.github/ISSUE_TEMPLATE/bug_report.yml)
* Nightlys for both `main` and `beta` branches!
* Code of Conduct
* Contribution Guidelines
* [Wiki](https://github.com/Boss-1s/key_multivalue_storage/wiki) Updates
* Added Linting for TOML, YAML, Bash (`*.toml`, `*.yaml`/`*.yml`, `*.sh`)
#### Module Updates 
##### In \_\_init__.py:
* Added `PendingDeprecationWarning` about module name deprecation
#### Dependency updates
* None this time ;)

#### Plans for next update
Our next few 1.2.3.x updates should see more Repo updates, specifically working on the wiki page and other documentation. I am also hoping for some prettifying in the module itself on kms-semver1.2, whilst working on kms-semver1.3.

**Full Changelog**: [`v1.2.2.20260517.3` vs `v1.2.3.20260522`](https://github.com/Boss-1s/key_multivalue_storage/compare/v1.2.2.20260517.3...v1.2.3.20260522)

---

## 📦 v1.2.2.20260517.3 — *kms-v1.2.2/2026.05.17c*

⚙ **Target Node Commit:** `b313bc41`
📝 **Release Type:** Stable Promotion

### What's Changed
#### Repo Updates
* Added an auto-version script
* Added a step in build job to auto-version based on release details before publication
* Minor updates to Contributing Guidelines
* Removed unneeded files... 😅
#### Module Updates 
* None this time :)
#### Dependency updates
* None this time :)

#### Plans for next update
Our next few 1.2.2.x update should see more Repo updates as I slowly get situated in PyPi and here, specifically working on the wiki page and other documentation. I am also hoping for some prettifying in the module itself on kms-semver1.2, while preparing for kms-semver1.3 alpha release 1.

**Full Changelog**: https://github.com/Boss-1s/key_multivalue_storage/compare/v1.2.2.20260517.2...v1.2.2.20260517.3

---

## 📦 v1.2.2.20260517.3-b — *kms-v1.2.2/2026.05.17c-beta*

⚙ **Target Node Commit:** `bb7d6746`
📝 **Release Type:** Pre-release - Minor Patch

### What's Changed
#### Repo Updates
* Added an auto-version script
* Added a step in build job to auto-version based on release details before publication
#### Module Updates 
* None this time :)
#### Dependency updates
* None this time :)

#### Notes
This is marked as a beta release because I have no idea if the current code works. If you see another beta, then, well, we all know what that means...

#### Plans for next update
Our next few 1.2.2.x update should see more Repo updates as I slowly get situated in PyPi and here, specifically working on the wiki page and other documentation.

The 1.3 beta will come out soon!

---

## 📦 v1.2.2.20260517.2 — *kms-v1.2.2/2026.05.17b*

⚙ **Target Node Commit:** `6cc925b0`
📝 **Release Type:** Minor Patch

### What's Changed
#### Repo Updates
* fixed a fatal error in which versions were incorrect, preventing release of previous version
#### Module Updates 
* None this time ;)
#### Dependency updates
* None this time ;)

#### Plans for next update
Our next few 1.2.2.x update should see more Repo updates as I slowly get situated in PyPi and here, specifically working on the [wiki page](https://github.com/Boss-1s/key_multivalue_storage/wiki) and other documentation.

The 1.3 beta will come out soon!

**Full Changelog**: [`kms-calver2026.05.17` vs `kms-calver2026.05.17b`](https://github.com/Boss-1s/key_multivalue_storage/compare/v1.2.2.20260517...v1.2.2.20260517.2)

---

## 📦 v1.2.2.20260517.1 — *kms-v1.2.2/2026.05.17a*

⚙ **Target Node Commit:** `2308c0c7`
📝 **Release Type:** Minor Patch

### What's Changed
#### Repo Updates
* fixed a fatal error in which classifiers were incorrect, preventing release of previous version
#### Module Updates 
* None this time ;)
#### Dependency updates
* None this time ;)

#### Plans for next update
Our next few 1.2.2.x update should see more Repo updates as I slowly get situated in PyPi and here, specifically working on the [wiki page](https://github.com/Boss-1s/key_multivalue_storage/wiki) and other documentation.

The 1.3 beta will come out soon!

**Full Changelog**: [`kms-calver2026.05.17` vs `kms-calver2026.05.17a`](https://github.com/Boss-1s/key_multivalue_storage/compare/v1.2.2.20260517...v1.2.2.20260517.1)

---

## 📦 v1.2.2.20260517 — *kms-v1.2.2/2026.05.17*

⚙ **Target Node Commit:** `b6170c53`
📝 **Release Type:** Minor Patch

### What's Changed
#### Repo Updates
* Changed some classifiers in [`pyproject.toml`](https://github.com/Boss-1s/key_multivalue_storage/blob/main/pyproject.toml)
* Completed [Security Policy](https://github.com/Boss-1s/key_multivalue_storage/blob/main/docs/SECURITY.md)
* Created [Contributing Guidelines](https://github.com/Boss-1s/key_multivalue_storage/blob/main/docs/CONTRIBUTING.md)
* Created blank [`requirements.txt`](https://github.com/Boss-1s/key_multivalue_storage/blob/main/requirements.txt)
* Other fixes
#### Module Updates 
* None this time ;)
#### Dependency updates
* Bump `setuptools` from `61.0` to `77.0.3` (7b64369)

#### Plans for next update
Our next few 1.2.2.x update should see more Repo updates as I slowly get situated in PyPi and here, specifically working on the [wiki page](https://github.com/Boss-1s/key_multivalue_storage/wiki) and other documentation.

The 1.3 beta will come out soon!

**Full Changelog**: [`kms-calver2026.05.15a` vs `kms-calver2026.05.17`](https://github.com/Boss-1s/key_multivalue_storage/compare/v1.2.2.20260515.1...v1.2.2.20260517)

---

## 📦 v1.2.2.20260515.1 — *kms-v1.2.2/2026.05.15a*

⚙ **Target Node Commit:** `cc051257`
📝 **Release Type:** Minor Patch

### What's Changed
#### Repo Updates
* Fixed a fatal bug where release would not deploy properly due to insufficient permissions 
#### Module Updates 
* None this time ;)
#### Dependency updates
* None this time ;)

#### Plans for next update
Our next few 1.2.2.x update should see more Repo updates as I slowly get situated in PyPi and here, specifically working on the [wiki page](https://github.com/Boss-1s/key_multivalue_storage/wiki) (which is currently empty).
The 1.3 beta may also come out around that time. 

---

## 📦 v1.2.2.20260515 — *kms-v1.2.2/2026.05.15*

⚙ **Target Node Commit:** `1968a9b4`
📝 **Release Type:** Minor Patch

### What's Changed
#### Repo Updates
* Readme is practically finished!
* Added Security Advisory, which contains an explanation of the versioning systems and supported versions.
* Added Dependabot
* Added CodeQL for code scanning
* Release assets should now be automatically uploaded to this release page right here
* Fixed multiple test deployment issue
#### Module Updates 
None this time ;)
#### Dependency updates
* Bump actions/checkout from 4 to 6
* Bump softprops/action-gh-release from 2 to 3

**Full Changelog**: [`v1.2.2.20260506.2 vs. v1.2.2.20260515`](https://github.com/Boss-1s/key_multivalue_storage/compare/v1.2.2.20260506.2...v1.2.2.20260515)

#### Plans for next update
Our next 1.2.2.x update should see more Repo updates as I slowly get situated in PyPi and here, specifically working on the [wiki page](https://github.com/Boss-1s/key_multivalue_storage/wiki) (which is currently empty).
The 1.3 beta may also come out around that time. 

---

## 📦 v1.2.2.20260506.2 — *kms-v1.2.2/2026.05.06b*

⚙ **Target Node Commit:** `44758a3c`
📝 **Release Type:** Major Patch

### First Package Release! (hopefully)
This module was originally a single file that I made just for fun, now i've decided to make it into a package!
README will be finished in v1.3, alongside the 'Great Docstring Update' ;)

**Full Changelog**: https://github.com/Boss-1s/key_multivalue_storage/commits/v1.2.2.20260506.2

---

## 📦 v1.2.1.20260417.2 — *kms-v1.2.1/2026.04.17b*

⚙ **Target Node Commit:** `70424d7e`
📝 **Release Type:** Major Patch

> [!CAUTION]
> This is an older release of this library brought back to life through archives in [this commit history](https://github.com/Boss-1s/scratchattach/commits/c2ac6affabf7c36eb64e6a5fafc8005d1e81c3ad/key_multivalue_storage.py). Things may be broken and not work.

> [!note]
> This release involves three seperate releases: the main release, `v1.2.1.20260417`, and the two patches after that, `v1.2.1.20260417a` and `v1.2.1.20260417b` **(This release)**.

#### What's Changed
##### `kms-v1.2.1/2026.04.17`
- Fixed License Statement Format
- Changed Versioning format (now `sematic/date` vs. old one `date` and `sematic` separate)
- Created metaclass `_StorageSettingsMeta`
- Seven new global variables: `VERSION`, `DATE_VERSION`, `LAST_UPDATE`, `indent`, `encode`, `skip_delete_warn`, `auto_delete_self`
- Instance ID now prioritizes `uuid.uuid7()`, and falls back to `uuid.uuid4()` if CPython version is < 3.14
- Small changes to functions `store` and `Delete.all` to support globals
##### `kms-v1.2.1/2026.04.17a`
- Changes involving the global variable `skip_delete_warn` have been reverted and the variable deleted
##### `kms-v1.2.1/2026.04.17b` (This release)
- Fix tests failing due to an attempt to grab the indent in the `__store` functions, which is an `@staticmethod`
- Changed it so all functions in Edit that use `__store` provide the indent default (`Storage.indent`) beforehand
- Prettified `_encode` and `_decode`

Changelog:
`kms-v1.2.1/2026.04.17`: https://github.com/Boss-1s/scratchattach/commit/515e0c715c723aa4821b90f9753d062cd7bc7675
`kms-v1.2.1/2026.04.17a`: https://github.com/Boss-1s/scratchattach/commit/db471126f57ee6b0fe371631b04d6bfcc7e00b78
`kms-v1.2.1/2026.04.17b` **(This release)**: https://github.com/Boss-1s/scratchattach/commit/208a0874e3ebeaf124fb926bff271fffb2452b39

---

## 📦 v1.2.0.20260128.1 — *kms-v1.2/2026.01.28a*

⚙ **Target Node Commit:** `f0c2322b`
📝 **Release Type:** Minor Patch

> [!CAUTION]
> This is an older release of this library brought back to life through archives in [this commit history](https://github.com/Boss-1s/scratchattach/commits/c2ac6affabf7c36eb64e6a5fafc8005d1e81c3ad/key_multivalue_storage.py). Things may be broken and not work.

#### What's Changed
- Removed unused `datetime`

Changelog: https://github.com/Boss-1s/scratchattach/commit/b64dd8bd9891e664d84980521e21877f11799a29

---

## 📦 v1.2.0.20260104 — *kms-v1.2/2026.01.04*

⚙ **Target Node Commit:** `5aced039`
📝 **Release Type:** Initial Release

> [!CAUTION]
> This is an older release of this library brought back to life through archives in [this commit history](url). Things may be broken and not work.

#### What's Changed
- Partially added `logging.Logger` support
- `Storage._KeyNotFoundError` now inherits from `KeyError` instead of the generic `Exception`
- **Complete type-hint refactor**
- **Remove `Storage._dprint`** (`_dprint` was a legacy private function that implemented an extremely redundant `stdout` printing though printing with both `print()` and `os.system("echo...")`)
- Refactored debug messages to include the method in which the print statement is nested in
- **_Finished all dunder methods_** (added `__getitem__`, `__setitem__`, `__delitem__`, `__len__`, `__contains__`, `__iter__`, `__getattr__`, `__setattr__`, `__call__`, `__enter__`, `__exit__`, `__format__`)

Changelog: https://github.com/Boss-1s/scratchattach/commit/84a75fc3847bcc2de0e7f45b3b41230ef659fec3

---

