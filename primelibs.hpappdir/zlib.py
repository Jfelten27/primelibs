from utils import *
from palette import *

import base64

def compress(data):
  result = bytearray()
  bitOffset = 0

  def addBits(n, bits):
    nonlocal bitOffset
    nonlocal result
    for i in range(n):
      if bitOffset:
        result[-1] |= ((bits >> i) & 1) << bitOffset
      else:
        result.append((bits >> i) & 1)
      bitOffset = (bitOffset + 1) % 8

  def encode(codes, d):
    n, bits = codes[d]
    code = 0
    for i in range(n):
      code <<= 1
      code |= (bits >> i) & 1
    addBits(n, code)

  def construct(lengths):
    mb = max(lengths)
    count = counter(lengths)
    count[0] = 0
    offsets = [0] * (mb + 1)
    code = 0
    codes = {'max': mb, 'min': min(lengths, key=lambda x: (x - 1) % (mb + 1) + 1)}
    for i in range(mb):
      try:
        code += count[i]
      except:
        pass
      code <<= 1
      offsets[i + 1] = code
    for v, l in enumerate(lengths):
      if l:
        codes[v] = l, offsets[l]
        offsets[l] += 1
    return codes

  addBits(16, 0x0178)
  addBits(1, 1)
  addBits(2, 1)
  codes = construct((8,) * 144 + (9,) * 112 + (7,) * 24 + (8,) * 8)
  for d in data:
    encode(codes, d)
  encode(codes, 256)
  return result

def decompress(data, printResult=False, showProgress=False):
  codeLenOrder = (16, 17, 18, 0, 8, 7, 9, 6, 10, 5, 11, 4, 12, 3, 13, 2, 14, 1, 15)

  lengthLUT = (
      (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10),
      (1, 11), (1, 13), (1, 15), (1, 17),
      (2, 19), (2, 23), (2, 27), (2, 31),
      (3, 35), (3, 43), (3, 51), (3, 59),
      (4, 67), (4, 83), (4, 99), (4, 115),
      (5, 131), (5, 163), (5, 195), (5, 227),
      (0, 258),
  )

  distLUT = (
      (0, 1), (0, 2), (0, 3), (0, 4),
      (1, 5), (1, 7), (2, 9), (2, 13),
      (3, 17), (3, 25), (4, 33), (4, 49),
      (5, 65), (5, 97), (6, 129), (6, 193),
      (7, 257), (7, 385), (8, 513), (8, 769),
      (9, 1025), (9, 1537), (10, 2049), (10, 3073),
      (11, 4097), (11, 6145), (12, 8193), (12, 12289),
      (13, 16385), (13, 24577),
  )

  byteOffset = 0
  bitOffset = 0
  decodedData = bytearray()

  def getBits(n):
    nonlocal bitOffset
    nonlocal data
    bits = 0
    for i in range(n):
      byte = data[(bitOffset + i) // 8]
      bit = (byte >> ((bitOffset + i) % 8)) & 1
      bits |= bit << i
    bitOffset += n
    return bits

  def decode(codes):
    nonlocal bitOffset
    nonlocal data
    code = first = index = 0
    for l in range(1, codes['max'] + 1):
      code <<= 1
      byte = data[bitOffset // 8]
      bit = (byte >> (bitOffset % 8)) & 1
      code |= bit
      bitOffset += 1
      try:
        value = codes[(l, code)]
      except KeyError:
        pass
      else:
        return value
    raise ValueError

  def construct(lengths):
    mb = max(lengths)
    count = counter(lengths)
    count[0] = 0
    offsets = [0] * (mb + 1)
    code = 0
    codes = {'max': mb, 'min': min(lengths, key=lambda x: (x - 1) % (mb + 1) + 1)}
    for i in range(mb):
      try:
        code += count[i]
      except:
        pass
      code <<= 1
      offsets[i + 1] = code
    for v, l in enumerate(lengths):
      if l:
        codes[(l, offsets[l])] = v
        offsets[l] += 1
    return codes

  def getCodeLengths(lengths, nCode):
    symbols = construct(lengths)
    result = []
    prevLen = 0
    while len(result) < nCode:
      symbol = decode(symbols)
      if symbol < 16:
        result += [symbol]
        prevLen = symbol
      elif symbol == 16:
        result += [prevLen] * (3 + getBits(2))
      elif symbol == 17:
        result += [0] * (3 + getBits(3))
      elif symbol == 18:
        result += [0] * (11 + getBits(7))
    return result

  getBits(16)
  stop = 0
  while not stop:
    stop = getBits(1)
    blockType = getBits(2)
    if blockType == 0:
      blockLength = getBits(16)
      if blockLength > len(data):
        print(blockLength, data[:10])
        return b''
      for i in range(blockLength):
        decodedData += chr(getBits(8))
        print(decodedData[-1], end='')
      continue
    elif blockType == 1:
      litCodes = construct((8,) * 144 + (9,) * 112 + (7,) * 24 + (8,) * 8)
      distCodes = construct((5,) * 32)
    elif blockType == 2:
      nLitLenCodes = getBits(5) + 257
      nDistCodes = getBits(5) + 1
      nCodes = getBits(4) + 4

      lenLengths = [0] * 19
      for n, i in enumerate(codeLenOrder):
        if n == nCodes:
          break
        lenLengths[i] = getBits(3)
      lengths = getCodeLengths(lenLengths, nLitLenCodes + nDistCodes)
      litLengths = lengths[:nLitLenCodes]
      distLengths = lengths[nLitLenCodes:]
      litCodes = construct(litLengths)
      distCodes = construct(distLengths)

    while True:
      code = decode(litCodes)
      if code < 256:
        decodedData.append(code)
        if printResult:
          print(chr(code), end='')
      elif code == 256:
        break
      else:
        extLenBits, length = lengthLUT[code - 257]
        extLength = getBits(extLenBits)
        length += extLength

        extDistBits, dist = distLUT[decode(distCodes)]
        extDist = getBits(extDistBits)
        dist += extDist

        start = len(decodedData) - dist
        if length > dist:
          decodedData += decodedData[start:]
          for i in range(dist, length):
            decodedData.append(decodedData[start + i])
          if printResult:
            print(bytes(decodedData[-length:]).decode(), end='')
        else:
          if printResult:
            print(bytes(decodedData[start:start + length]).decode(), end='')
          decodedData += decodedData[start:start + length]
      if len(decodedData) % 1000 < 20:
        drawProgressBar(bitOffset / len(data) / 8, red)
  return decodedData