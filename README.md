# PrimeLibs
## Introduction
A collection of Python libraries to provide a useful framework for creating powerful HP Prime applications with ease

## Getting Started

To include PrimeLibs in one of your python projects, use the following lines at the start of your main.py file:

```python3
import sys
sys.path.append('.')
sys.path.append('../primelibs.hpappdir')
```

## Documentation

### base64.py

This library provides a set of function for working with Base64-encoded strings.

#### b64encode

##### Syntax:
```python3
b64encode(data: bytes) -> str
```

##### Parameters:
- `data: bytes` -- input data to be converted to Base64 format

##### Returns:
the input byte sequence encoded in Base64

##### Example:
```python3
base64.b64encode(b'Hello, world!')
```
Output: `'SGVsbG8sIHdvcmxkIQ=='`

#### b64decode

##### Syntax:
```python3
b64encode(data: str) -> bytearray
```

##### Parameters:
- `data: str` -- Base64 data to be converted to bytes format

##### Returns:
the input Base64 string decoded into a byte array

##### Example:
```python3
base64.b64decode('SGVsbG8sIHdvcmxkIQ==')
```
Output: `bytearray(b'Hello, world!')`






### filebroswer.py

This is a set of classes derived fromm the `gui.py` framework which provide file I/O pop-up window functionality

#### FileBrowser(gui.Frame)

##### Syntax:
```python3
FileBrowser(ext='') -> FileBrowser
```

##### Properties:


##### 
