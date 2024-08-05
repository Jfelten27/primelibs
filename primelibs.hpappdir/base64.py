from math import *

_b64chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

def b64decode(data):
  result = bytearray()
  for i in range(0, len(data), 4):
    values = bytes([_b64chars.index(d) for d in data[i:i + 4] if d != '='])
    chunk = sum([v << (6 * (3 - i)) for i, v in enumerate(values)])
    decodedchunk = [(chunk >> i) & 0xff for i in range(16, -8, -8)]
    result += bytearray(decodedchunk[:len(values) - 1])
  return result

def b64encode(data):
  result = ''
  for i in range(0, ceil(len(data) / 3) * 3, 3):
    chunk = sum([d << (16 - 8 * i) for i, d in enumerate(data[i:i + 3])])
    values = ''.join([_b64chars[(chunk >> i) & 0x3f] for i in range(18, -6, -6)][:len(data[i:i + 3]) + 1]) + '=' * (3 - len(data[i:i + 3]))
    result += values
  return result