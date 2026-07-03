"""
Run all kms tests.

### Usage
In your terminal, run:
```sh
git clone https://github.com/boss-1s/key_multivalue_storage kms
cd kms
python test/
```
"""
#pylint: disable=exec-used,consider-using-with

exec(open("test/test-general.py").read())
print("-"*30)
exec(open("test/test-meta.py").read())
