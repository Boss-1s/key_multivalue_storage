# Security Policy

## Things to note
I use two versioning systems, my offical versioning and the PyPi versioning.
### Official Versioning 
Official versioning all starts with 'kms-'. 
Depending on the type of official versioning, you may see the following:
- kms-v(semver)/(calver)(patch letter)
- kms-semver(semver)
- kms-calver(calver)
### PyPi Versioning 
To conform with [PEP 440](https://peps.python.org/pep-0440/), I use a secondary versioning system. This one has no prefixes and follows all PEP 440 guidelines. Basically, this:
> kms-v1.2/2026.01.04

becomes this:
> v1.2.0.20260104

Letter prefixes become numbers according to its position in the alphabet (i.e. a is 1, b is 2)

## Supported Versions

Currently, the only (and latest) released package version is kms-v1.2.2/2026.05.06b. However, I may port all kms-semver1.x.x to pypi.

[See more about the upcoming kms-semver2.0 update.]

| Version | Current Status | Expected EOL |
| ------- | ------------------ | - |
| 1.0.x | Unsupported | Already reached EOL |
| 1.1.x | Unsupported | Already reached EOL |
| 1.2.x | Supported | 2.1 |
| 1.3.x | Unreleased | 2.1 |
| 1.4.x | Unreleased | 2.2 |
| 1.5.x | Unreleased | 2.2 |
| 1.6.x | Unreleased | 2.3 |
| 2.0 | Unreleased | Undetermined|

## Reporting a Vulnerability

Please report vulnerabilities as a GitHub issue. I will get back to you ASAP.
