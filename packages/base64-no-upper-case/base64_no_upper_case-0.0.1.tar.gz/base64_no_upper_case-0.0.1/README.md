Base64, but no UPPER CASE.

It is useful in case-insensitive scenarios, such as Scratch.

```
!#$%&()*,-.:;<>?@[]^_`{|}~abcdefghijklmnopqrstuvwxyz0123456789+/
```

For Scratch:  
<https://scratch.mit.edu/projects/1263900629/>  

For JavaScript:  
<https://www.npmjs.com/package/base64-no-upper-case>  

## Setup

```
pip3 install base64-no-upper-case
```

```py
import base64NoUpperCase

# Encode str
enc = base64NoUpperCase.encode("Hello world!")
print(enc)

# Decode to str
dec = base64NoUpperCase.decodeToStr("])`sb)8gd29yb)@h")
print(dec)

# Encode bytearray
enc = base64NoUpperCase.encode(bytearray(16))
print(enc)

# Encode bytes
enc = base64NoUpperCase.encode(bytes(16))
print(enc)

# Decode to bytearray
dec = base64NoUpperCase.decode("^2rn8;ffl7<z*}{.|m@|{w==")
print(dec)
```
