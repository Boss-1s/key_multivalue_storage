import key_multivalue_storage as kms

assert kms.Encoding
assert kms.Encoding.UTF8 == "utf-8"
assert kms.Encoding.UTF16 == "utf-16"
assert kms.Encoding.UTF32 == "utf-32"
assert kms.Encoding.ASCII == "ascii"
assert kms.Encoding.BASE64 == "base64"
assert kms.Encoding.KMS == "kms_default"
assert kms.Encoding.SHA256 == "sha256"
assert kms.Encoding.SHA512 == "sha512"
assert kms.Encoding.SHA1 == "sha1"
assert kms.Encoding.RSA == "rsa"
assert kms.Encoding.AES == "aes"
assert kms.Encoding.HMAC == "hmac"
assert kms.Encoding.PIGPEN == "pigpen"
assert kms.Encoding.MORSE == "morse_code"
assert kms.Encoding.NONE == ""
assert kms.Encoding("NONEXISTENT") == kms.Encoding.KMS
