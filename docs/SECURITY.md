# Versioning, Release, and Security

## Versioning
I use two versioning systems, my offical versioning and the PyPi versioning.
### Official Versioning 
Official versioning all starts with 'kms-'. 
Depending on the type of official versioning, you may see the following:
- kms-v(SemVer)/(CalVer)(patch letter)
- kms-semver(SemVer)
- kms-calver(CalVer)

### PyPi Versioning 
To conform with [PEP 440](https://peps.python.org/pep-0440/), I use a secondary versioning system. This one has no prefixes and follows all PEP 440 guidelines. Basically, this:
> kms-v1.2/2026.01.04

becomes this as a tag:
> v1.2.0.20260104

which automatically becomes this in PyPi:
> 1.2.0.20260104

Letter suffixes become numbers according to its position in the alphabet (i.e. a is 1, b is 2)

## Releases
When a release is published, a build of the library will be created and published to PyPi with the **PyPi Versioning**. The official name of the release as seen from Github will be the **Official Version string**.

The version string would look like either one of the following:

> kms-v(major).(minor).(patch)/(year YYYY).(month MM).(day DD)(letter suffix)
>
> i.e. kms-v1.2/2026.01.04

> (major).(minor).(patch).(year YYYY)(month MM)(day DD).(number suffix)
>
> i.e. 1.2.2.20260515.1

- An update is a **minor patch** when only the ***date*** changes in the version string, or a ***suffix*** is added to the string. This is usually used to denote small, unoticiable changes to the module or minor changes to the repository like updating the README.
- An update is a **major patch** when the ***patch number*** changes in the version string, along with the **date**. This is usually used to denote bug fixes, minor feature additions, dependancy updates, or major updates to repository resources like documentation.
- An update is a **minor update** when the ***minor version number*** changes in the version string, resetting the **patch number** to zero, and changes the **date**. This is usually used to denote major additions, minor breaking changes in *some* features, etc. It is possible for a minor update to skip increments in the patch number.
- An update is a **major update** when the ***major version number***  changes in the version string, resetting both the **minor version number** and **patch number** to zero, and changes the **date**. This type of update denotes **widespread breaking changes** within the library. **All versions with different major version numbers will *NEVER* be backwards compatible**.

You may see a discrepancy between the version string within the [main module file](https://github.com/Boss-1s/key_multivalue_storage/blob/main/src/key_multivalue_storage/key_multivalue_storage.py) and the released version string. This is because updates may not have involved the module. Always trust the higher version number.

[**See more about sematic versioning (SemVer) here**](https://semver.org/)

[**See more about calendar versioning (CalVer) here**](https://calver.org/)

## Supported Versions

Currently, the only released package versions are kms-v1.2.2/2026.05.06b and later. However, I may port all kms-semver1.x.x to pypi.

[See more about the upcoming kms-semver2.0 update.](https://github.com/Boss-1s/key_multivalue_storage/wiki/Roadmap#kms-semver20-20270817)

| Version | Production Stage | Current Status | Expected EOL |
| ------|-------| ------------------ | - |
| 1.0.x | Inactive(7) | Unsupported | Already reached EOL |
| 1.1.x | Inactive(7) | Unsupported | Already reached EOL |
| 1.2.x | Production/Stable (5)| LTS | 1.5 |
| 1.3.x | Production/Stable (5) | Pre-Release | 1.6 |
| 1.4.x | Planning(1) | Unreleased | 2.0 |
| 1.5.x | None(0) | Unreleased | 2.1 |
| 1.6.x | None(0) | Unreleased | 2.2 |
| 2.0.x | Planning(1) | Unreleased | 2.3 |

## Reporting a Vulnerability

Please report vulnerabilities as a GitHub issue. I will get back to you ASAP.
