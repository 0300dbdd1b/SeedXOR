
from ctypes import BigEndianStructure
import sys
from secrets import randbits
from binascii import a2b_hex
from hashlib import sha256

DEFAULT_DICT_PATH = './BIP39_Wordlists/BIP39_EN'

def check_entropy(entropy):
	ln = len(entropy)
	if ln <= 128:
		return(resize_bin(entropy,128))
	elif ln > 128 & ln <= 160:
		return(resize_bin(entropy, 160))
	elif ln > 160 & ln <= 192:
		return(resize_bin(entropy, 192))
	elif ln > 192 & ln <= 224:
		return(resize_bin(entropy, 224))
	elif ln > 224 & ln <= 256:
		return(resize_bin(entropy, 256))
	else:
		return ("Too Big Entropy")

def get_dic(dict_path=DEFAULT_DICT_PATH):
	wordlist = {}
	with open(dict_path) as dict:
		key = 0
		for line in dict:
			(key, val) = key , line
			wordlist[int(key)] = val
			key += 1
		return (wordlist)

	
def dict_to_str(dict):
	output = ""
	for index in dict:
		output += (dict[index] + " ")
	output = output[:-1]
	return (output)

def resize_bin(bin, nbits):
	if nbits - len(bin) > 0:
		for i in range(0, nbits - len(bin)):
			bin = "0" + bin
	return (bin)


def get_wordnumber(word, dict_path=DEFAULT_DICT_PATH):
	index = 0
	with open(dict_path) as dict:
		for line in dict:
			if word == line or word == line[:-1]:
				dict.close()
				return resize_bin(bin(index)[2:], 11)
			index += 1
	dict.close()
	return ("Error")



def mnemonic_to_entropy(phrase, dict_path=DEFAULT_DICT_PATH):
	mnemonic = ""
	phrase = phrase.split(" ")
	for words in phrase:
		mnemonic += get_wordnumber(words, dict_path)
	return(mnemonic[:-int(len(mnemonic)/32)])

def entropy_to_mnemonic(entropy, dict_path):
	entropy = check_entropy(bin(entropy)[2:])
	entropy = hex(int(entropy,2))[2:]
	entropy = entropy if len(entropy)%2 == 0 else "0" + entropy
	dict = get_dic(dict_path)
	fingerprint = sha256(a2b_hex(entropy)).hexdigest()[:int(len(entropy)/32)]
	checksum = resize_bin(bin(int(entropy, 16))[2:], int(len(entropy) * 4)) + resize_bin(bin(int(fingerprint, 16))[2:], int(len(entropy)/8))
	mnemonic = {}
	index = 1
	i = 0
	while i < len(checksum):
		word = int(checksum[i:i+11], 2)
		word = dict.get(word)
		(index, word) = index , word[:-1]
		mnemonic[int(index)] = word
		index += 1
		i += 11
	return (dict_to_str(mnemonic))



def seed_xor(seed, seed_nbits, n, deterministic, outputs):
	if deterministic == False:
		new_entropy = randbits(seed_nbits)
	if deterministic == True:
		print(sha256(a2b_hex(hex(seed)[2:])).hexdigest())
		new_entropy = int(sha256(a2b_hex(hex(seed)[2:])).hexdigest()[2:int(seed_nbits/4) + 2], 16)
		print(new_entropy)
	outputs.append(new_entropy)
	seed =  seed ^ new_entropy

	if n <= 2:
		outputs.append(seed)
		return(outputs)
	else:
		return(seed_xor(seed, seed_nbits, n-1, deterministic, outputs))

def seed_combining(seeds):
	seeds[0] = seeds[0] ^ seeds[1]
	seeds.pop(1)
	if len(seeds) > 1:
		return(seed_combining(seeds))
	else:
		return(seeds[0])

def xor_printer(outputs, dict_path=DEFAULT_DICT_PATH):
	print("XOR Splitted Mnemonics :")
	i = 1
	for output in outputs:
		print(i, ": ", entropy_to_mnemonic(int(bin(output),2), dict_path),"\n")
		i+=1

def main():
	if (sys.argv[1] == '--split' and sys.argv[2] == '--deterministic' and len(sys.argv) >= 4):
		outputs = []
		dict_path = DEFAULT_DICT_PATH
		entropy = mnemonic_to_entropy(sys.argv[3], dict_path)
		seed_xor(int(entropy,2), len(entropy), int(sys.argv[4]),True, outputs)
		xor_printer(outputs, dict_path)
	elif (sys.argv[1] == '--split' and len(sys.argv) >= 3):
		outputs = []
		dict_path = DEFAULT_DICT_PATH
		entropy = mnemonic_to_entropy(sys.argv[2], dict_path)
		seed_xor(int(entropy,2), len(entropy), int(sys.argv[3]),False, outputs)
		xor_printer(outputs, dict_path)
	elif (sys.argv[1] == '--combine' and len(sys.argv) >= 3):
		i = 2
		outputs = []
		dict_path = DEFAULT_DICT_PATH
		while i < len(sys.argv):
			outputs.append(int(mnemonic_to_entropy(sys.argv[i]),2))
			i+=1
		print(entropy_to_mnemonic(seed_combining(outputs), dict_path))
	

	else:
		return ("error")


	return

main()