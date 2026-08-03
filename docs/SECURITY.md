# Versioning, Release, and Security

## Versioning
I use two versioning systems, my offical versioning and the PyPI versioning.
### Official Versioning 
Official versioning all starts with 'kms-'. 
Depending on the type of official versioning, you may see the following:
- `kms-v`(SemVer)`/`(CalVer)(patch letter)
- `kms-semver`(SemVer)
- `kms-calver`(CalVer)

You will most likely see `kms-semver` a lot more than the other two.

### PyPI Versioning 
To conform with [PEP 440](https://peps.python.org/pep-0440/), I use a secondary versioning system. This one has no prefixes and follows all PEP 440 guidelines.

Basically, this:

> `kms-v1.2/2026.01.04`

becomes this as a tag:

> `v1.2.0.20260104`

which is automatically converted by `setuptools` and becomes this in PyPI:

> `1.2.0.20260104`

**Letter suffixes** become _numbers_ according to its _position in the alphabet_ (i.e. a is 1, b is 2)

## Releases
When a release is published, a build of the library will be created and published to PyPI with the **PyPI Versioning**. The official name of the release as seen from Github will be the **Official Version string**.

The version string would look like either one of the following:

> `kms-v(major).(minor).(patch)/(year YYYY).(month MM).(day DD)(letter suffix)`
>
> i.e. `kms-v1.2/2026.01.04`

or

> `(major).(minor).(patch).(year YYYY)(month MM)(day DD).(number suffix)`
>
> i.e. `1.2.2.20260515.1`

- An update is a **minor patch** when only the ***date*** changes in the version string, or a ***suffix*** is added to the string. This is usually used to denote small, unoticiable changes to the module or minor changes to the repository like updating the README.
- An update is a **major patch** when the ***patch number*** changes in the version string, along with the **date**. This is usually used to denote bug fixes, minor feature additions, dependancy updates, or major updates to repository resources like documentation.
- An update is a **minor update** when the ***minor version number*** changes in the version string, resetting the **patch number** to zero, and changes the **date**. This is usually used to denote major additions, minor breaking changes in *some* features, etc. It is possible for a minor update to skip increments in the patch number.
- An update is a **major update** when the ***major version number***  changes in the version string, resetting both the **minor version number** and **patch number** to zero, and changes the **date**. This type of update denotes **widespread breaking changes** within the library. **All versions with different major version numbers will *NEVER* be backwards compatible**.

[**See more about sematic versioning (SemVer) here**](https://semver.org/)

[**See more about calendar versioning (CalVer) here**](https://calver.org/)

## Supported Versions

Currently, the only **released** package versions _(not necessarially supported)_ are `kms-v1.2/2026.01.04` and later. However, I may port all `kms-semver1.x.x` to PyPI if I have the time.

[See more about the upcoming kms-semver2.0 update.](Roadmap#kms-semver200)

| Version | Production Stage | Current Status | Expected EOL |
| :------: | :-------: | ------------------ | :-: |
| 1.0.x | Inactive(7) | Unsupported | Already reached EOL |
| 1.1.x | Inactive(7) | Unsupported | Already reached EOL |
| 1.2.x | Production/Stable (5)| LTS | 1.5 |
| 1.3.x | Production/Stable (5) | Stable - **Latest** | 1.6 |
| 1.4.x | Planning(1) | Unreleased | 2.0 |
| 1.5.x | Planning(1) | Unreleased | 2.1 |
| 1.6.x | None(0) | Unreleased | 2.2 |
| 2.0.x | Planning(1) | Unreleased | 2.3 |

## Reporting a Vulnerability

[**Click here to draft a security vulnerability.**](https://github.com/Boss-1s/key_multivalue_storage/security/advisories/new) It is also recommended that an issue linking to that security advisory is created one the security advisory is published and becomes public. For anyone out there who has a fix, just **fork the repo**, **make the edit**, and **create a PR linking back to the issue.**
