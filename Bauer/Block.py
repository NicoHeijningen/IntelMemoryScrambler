import random

class BitString(object):
	def __init__(self, strm = None):
		if isinstance(strm, str):
			self._strm = [ int(i) for i in strm ]
		elif strm is not None:
			self._strm = list(strm)
		else:
			self._strm = list()
		assert(all(x in [ 0, 1 ] for x in self._strm))

	def append(self, value):
		assert(value in [ 0, 1 ])
		self._strm.append(value)
		return self
	
	def prepend(self, value):
		assert(value in [ 0, 1 ])
		self._strm.insert(0, value)
		return self

	def setrandomly(self, length):
		self._strm = [ random.randint(0, 1) for i in range(length) ]
		return self

	def setfromstr(self, string):
		self._strm = [ int(i) for i in string ]
		return self

	def clone(self):
		clone = BitString(list())
		clone._strm = list(self._strm)
		return clone

	@staticmethod
	def _bito(x, bitcount):
		"""Switches bitorder of the given number (i.e. most significant bit
		becomes least significant bit and vice versa)."""
		y = 0
		for i in range(bitcount):
				if (x & (1 << i)) != 0:
						y |= (1 << (bitcount - 1 - i))
		return y

	def getxorval(self, other, msbfirst = True):
		assert(len(self) == len(other))
		if msbfirst:
			return sum((a ^ b) << bit for (bit, (a, b)) in enumerate(zip(self._strm, other._strm)))
		else:
			return sum((a ^ b) << (len(self._strm) - 1 - bit) for (bit, (a, b)) in enumerate(zip(self._strm, other._strm)))

	def xor(self, blocksize, value, msbfirst = True):
		if not msbfirst:
			value = self._bito(value, blocksize)
		clone = self.clone()
		for i in range(len(self._strm)):
			clone._strm[i] ^= ((value >> (i % blocksize)) & 1)
		return clone

	def toint(self, msbfirst = False):
		if msbfirst:
			return sum((value << (len(self._strm) - 1 - bit)) for (bit, value) in enumerate(self._strm))
		else:
			return sum((value << bit) for (bit, value) in enumerate(self._strm))

	def isuniform(self):
		return len(set(self._strm)) == 1

	def wordswap(self, wordsize):
		assert((len(self._strm) % wordsize) == 0)
		clone = self.clone()
		clone._strm = [ ]
		for i in range(0, len(self._strm), wordsize):
			clone._strm += self._strm[i : i + wordsize][::-1]
		return clone
	
	def byteorderswap(self, wordsize, bytelen = 8):
		assert((len(self._strm) % wordsize) == 0)
		assert((wordsize % bytelen) == 0)
		clone = self.clone()
		clone._strm = [ ]
		for i in range(0, len(self._strm), wordsize):
			word = self._strm[i : i + wordsize]
			for j in reversed(range(0, len(word), bytelen)):				
				clone._strm += word[j : j + bytelen]
		return clone

	def export(self, wordlen = 32):
		wordcnt = (len(self) + wordlen - 1) // wordlen
		words = [ ]
		for i in range(wordcnt):
			chunk = self[i * wordlen : (i + 1) * wordlen]
			words.append("0x%x" % (chunk.toint()))
		exportstr = "{ %d, { %s } }" % (len(self), ",".join(words))
		return exportstr

	def fullexport(self, wordlen = 32):
		return "struct bitSequence sequence = %s;" % (self.export(wordlen))

	@property
	def streamdata(self):
		return self._strm

	def prefixequal(self, other):
		minlen = min(len(self), len(other))
		return self[:minlen] == other[:minlen]

	def __xor__(self, other):
		assert(len(self) == len(other))
		return BitString([ x ^ y for (x, y) in zip(self._strm, other._strm) ])

	def __eq__(self, other):
		return self._strm == other._strm

	def __len__(self):
		return len(self._strm)

	def __getitem__(self, index):
		if isinstance(index, int):
			return self._strm[index]
		else:
			clone = BitString(list())
			clone._strm = self._strm[index]
			return clone
	
	@property
	def binstr(self):
		return "".join(str(x) for x in self._strm)

	def __str__(self):
		if len(self) <= 150:
			return "BitString<%s:%s>" % (len(self), self.binstr)
		else:
			return "BitString<%s:%s...>" % (len(self), self.binstr[:150])


class Block(object):
	def __init__(self, source = None):
		if source is None:
			self._data = bytearray()
		else:
			self._data = bytearray(source)

	def bytedecimate(self, offset, threshold, period):
		return Block(value for (index, value) in enumerate(self._data) if ((index + offset) % period) < threshold)

	@property
	def bytesdata(self):
		return bytes(self._data)

	def clone(self):
		clone = Block()
		clone._data = bytearray(self._data)
		return clone

	def setfromhex(self, string):
		string = string.replace(" ", "")
		assert((len(string) % 2) == 0)
		self._data = bytearray(int(string[i : i + 2], 16) for i in range(0, len(string), 2))
		return self

	@staticmethod
	def _bitstobyte(bits, msbfirst):
		if msbfirst:
			return sum([ (value << bit) for (bit, value) in enumerate(reversed(bits)) ])
		else:
			return sum([ (value << bit) for (bit, value) in enumerate(bits) ])

	def setfrombits(self, bitstr, msbfirst = True):
		if isinstance(bitstr, str):
			bitstr = [ int(c) for c in bitstr ]
		assert((len(bitstr) % 8) == 0)
		self._data = bytearray(len(bitstr) // 8)
		for i in range(0, len(bitstr), 8):
			self._data[i // 8] = self._bitstobyte(bitstr[i : i + 8], msbfirst)
		return self
	
	@staticmethod
	def _bytetobits(byte, msbfirst):
		if msbfirst:
			rng = reversed(range(8))
		else:
			rng = range(8)
		bits = ((byte >> i) & 1 for i in rng)
		return bits
		
	def tobits(self, msbfirst = True):
		bitstring = [ ]
		for byte in self._data:
			bitstring += self._bytetobits(byte, msbfirst)
		return BitString(bitstring)

	def todecimatedbits(self, offset, period, msbfirst = True):
		bits = self.tobits(msbfirst = msbfirst)
		bits = [ bit for (index, bit) in enumerate(bits) if ((index % period) == offset) ]
		return BitString(bits)

	def decimate(self, period, offset = 0, msbfirst = True):
		bits = self.todecimatedbits(offset, period)
		bitcnt = (len(bits) // 8) * 8
		bits = bits[:bitcnt]
		clone = self.clone()
		clone.setfrombits(bits)
		return clone

	def setfromint(self, value, length = None, endian = "LE"):
		assert(endian in [ "LE", "BE" ])
		assert(value >= 0)
		if (length is not None):
			assert(length >= 0)
			assert(value < (256 ** length))
	
		self._data = bytearray()
		while (value > 0) or ((length is not None) and (length > 0)):
			self._data.append(value & 0xff)
			value >>= 8
			if length is not None:
				length -= 1
		if endian == "BE":
			self._data = bytearray(reversed(self._data))
		return self

	def toint(self, endian = "LE"):
		assert(endian in [ "LE", "BE" ])
		if endian == "LE":
			return sum(value << (8 * index) for (index, value) in enumerate(self._data))
		else:
			return sum(value << (8 * index) for (index, value) in enumerate(reversed(self._data)))

	def __eq__(self, other):
		if isinstance(other, Block):
			return self._data == other._data
		elif isinstance(other, bytes):
			return self._data == other
		else:
			raise Exception("Uncomparable")

	def __xor__(self, other):
		if len(self) != len(other):
			raise Exception("Can only XOR blocks of equal size")
		result = Block()
		result._data = bytearray(x ^ y for (x, y) in zip(self, other))
		return result

	def xorpattern(self, other):
		for i in range(len(self)):
			self._data[i] ^= other[i % len(other)]
		return self
	
	def andpattern(self, other):
		for i in range(len(self)):
			self._data[i] &= other[i % len(other)]
		return self
	
	def __invert__(self):
		return Block((~value) & 0xff for value in self)
	
	def __xor__(self, other):
		return Block(v1 ^ v2 for (v1, v2) in zip(self, other))
	
	def __or__(self, other):
		return Block(v1 | v2 for (v1, v2) in zip(self, other))

	@staticmethod
	def _hammingweight(byte):
		weight = 0
		while byte > 0:
			if (byte & 1) == 1:
				weight += 1
			byte >>= 1
		return weight

	def avghammingweight(self):
		return sum(self._hammingweight(x) for x in self._data) / len(self)

	def diffchars(self):
		return len(set(self._data))

	def deinterlace(self, bitcnt):
		return [ self.todecimatedbits(i, bitcnt) for i in range(bitcnt) ]
	
	def partition(self, partlength):
		if len(self) % partlength != 0:
			raise Exception("Block length (%d) not evenly divisible by parition length (%d)." % (len(self), partlength))
		parts = [ ]
		for i in range(len(self) // partlength):
			parts.append(self[partlength * i : partlength * (i + 1) ])
		return parts

	def invert(self):
		for (index, char) in enumerate(self._data):
			self._data[index] = (char ^ 0xff)
		return self

	def join(self, blocks):
		result = Block()
		for (index, block) in enumerate(blocks):
			if index > 0:
				result += self
			result += block
		return result

	@staticmethod
	def fromfile(filename):
		return Block(open(filename, "rb").read())

	def __add__(self, other):
		clone = self.clone()
		clone._data += other._data
		return clone

	def __getitem__(self, index):
		if isinstance(index, int):
			return self._data[index]
		else:
			clone = Block()
			clone._data = self._data[index]
			return clone

	def __iter__(self):
		return iter(self._data)

	def _gethexstr(self):
		if len(self) <= 80:
			return "".join("%02x" % (x) for x in self._data)
		else:
			return "".join("%02x" % (x) for x in self._data[:80]) + "..."

	def __len__(self):
		return len(self._data)

	def __str__(self):
		return "%3d={%s}" % (len(self), self._gethexstr())

if __name__ == "__main__":
	assert(Block().setfromhex("ff7f") == b"\xff\x7f")
	assert(Block(b"foobar") == b"foobar")

	b = Block().setfromhex("0102030405")
	b.xorpattern(Block().setfromhex("a050"))
	assert(b == b"\xa1\x52\xa3\x54\xa5")

	b = Block().setfromhex("01020304")
	assert(b.toint(endian = "BE") == 0x01020304)
	assert(b.toint(endian = "LE") == 0x04030201)

	assert(Block().setfromint(0x123456789abcdef, endian = "LE") == b"\xef\xcd\xab\x89\x67\x45\x23\x01")
	assert(Block().setfromint(0x123456789abcdef, endian = "BE") == b"\x01\x23\x45\x67\x89\xab\xcd\xef")

	assert(Block().setfromint(0x1234, length = 3, endian = "LE") == b"\x34\x12\x00")
	assert(Block().setfromint(0x1234, length = 3, endian = "BE") == b"\x00\x12\x34")
	assert(Block().setfromint(0x1234, length = 5, endian = "LE") == b"\x34\x12\x00\x00\x00")
	assert(Block().setfromint(0x1234, length = 5, endian = "BE") == b"\x00\x00\x00\x12\x34")

	assert(Block().setfromhex("0102").tobits(msbfirst = True) == BitString([ 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0 ]))
	assert(Block().setfromhex("0102").tobits(msbfirst = False) == BitString([ 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0 ]))
	assert(Block().setfromhex("ab").tobits(msbfirst = True) == BitString([ 1, 0, 1, 0, 1, 0, 1, 1 ]))
	assert(Block().setfromhex("ab").tobits(msbfirst = False) == BitString([ 1, 1, 0, 1, 0, 1, 0, 1 ]))

	assert(Block().setfrombits([ 0, 0, 0, 0, 1, 0, 1, 0 ]) == b"\x0a")
	assert(Block().setfrombits([ 0, 0, 0, 0, 1, 0, 1, 0 ], msbfirst = False) == b"\x50")
	assert(Block().setfrombits([ 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0 ]) == b"\x0a\xf0")
	assert(Block().setfrombits([ 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0 ], msbfirst = False) == b"\x50\x0f")

	for hexstr in [ "ff001234567899", "a55a9904", "abcd", "123456" ]:
		orig = Block().setfromhex(hexstr)
		b = orig.clone()
		assert(orig == b)
		assert(orig is not b)

		for endian in [ "LE", "BE" ]:
			i = b.toint(endian = endian)
			b = Block().setfromint(i, endian = endian)
			assert(b == orig)
		
		for msbfirst in [ True, False ]:
			bits = b.tobits(msbfirst = msbfirst)
			b = Block().setfrombits(bits, msbfirst = msbfirst)
			assert(b == orig)

		b.xorpattern(Block().setfromhex("a55a"))
		assert(b != orig)
		
		b.xorpattern(Block().setfromhex("5aa5"))
		assert(b != orig)
		
		b.xorpattern(Block().setfromhex("ff"))
		assert(b == orig)

	assert(Block(b"foobar")[:3] == Block(b"foo"))

	oneblock = Block(b"\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01")
	deinterlaced = oneblock.deinterlace(8)
	assert(len(deinterlaced) == 8)
	for bitstrm in deinterlaced:
		assert(bitstrm.isuniform())

	bitstrm = BitString([0] * (8 * 16))
	for i in range(256):
		xorstrm = bitstrm.xor(8, i)
		bytestrm = Block().setfrombits(xorstrm, msbfirst = False)
		assert(bytestrm.diffchars() == 1)
		assert(bytestrm[0] == i)
		assert(len(bytestrm) == 16)


	strm1 = BitString([0, 1, 0, 1, 0, 0, 0, 0, 0, 1 ])
	strm2 = BitString([1, 0, 1, 0, 0, 0, 0, 0, 1 ])
	assert(strm1[1:] == strm2)

	strm = Block(b"\x01\x02\x04").tobits(msbfirst = True)
	assert(strm == BitString([0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0 ]))
	strm = strm.wordswap(8)	
	assert(Block().setfrombits(strm, msbfirst = True) == Block(b"\x80\x40\x20"))
	assert(Block().setfrombits(strm, msbfirst = False) == Block(b"\x01\x02\x04"))

	strm = Block(b"\x01\x02\x04\x08").tobits(msbfirst = True)
	assert(strm == BitString([0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0 ]))
	strm = strm.wordswap(16)
	assert(strm == BitString([0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0 ]))
	assert(Block().setfrombits(strm, msbfirst = True) == Block(b"\x40\x80\x10\x20"))
	assert(Block().setfrombits(strm, msbfirst = False) == Block(b"\x02\x01\x08\x04"))
	
	strm = Block(b"\x00\x00\x00\x01").tobits(msbfirst = True)
	assert(Block().setfrombits(strm.byteorderswap(32)) == Block(b"\x01\x00\x00\x00"))
	assert(Block().setfrombits(strm.byteorderswap(16)) == Block(b"\x00\x00\x01\x00"))


	strm1 = BitString("110011010010000000101100000111000000000101110011101111010000111000111011001111000001001100110010011001010101110011100110101")
	strm2 = BitString("001100011000000001101100011010001100101110100011011110010011111111100010101010001101110111010100110110101001110100100110010")
	for msbfirst in [ False, True ]:
		xorvalue = strm1.getxorval(strm2, msbfirst = msbfirst)
		assert(strm1.xor(len(strm1), xorvalue, msbfirst = msbfirst) == strm2)
		assert(strm2.xor(len(strm1), xorvalue, msbfirst = msbfirst) == strm1)
