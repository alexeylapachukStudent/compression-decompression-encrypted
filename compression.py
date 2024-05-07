import math
import struct
import sys
from collections import Counter


def translating_to_binary_char(symbol, length):
    bin_symbol = bin(symbol)[2::]
    extended_symbol = bin_symbol.rjust(length, "0")
    return extended_symbol


def compression(generated_file, compressed_file):
    with open(generated_file, 'r') as generated_file_opened:
        text_to_encrypt = generated_file_opened.read()

    k = len(text_to_encrypt)
    x = len(set(text_to_encrypt))
    N = math.ceil(math.log2(x))
    R = (8 - (k * N) % 8) % 8

    count_char = Counter(text_to_encrypt)

    binary_representation = [translating_to_binary_char(i, N) for i in range(x)]
    binary_list = [(ch, binary_representation[i]) for i, (ch, freq) in enumerate(count_char.most_common())]
    sorted_char_list = [ch for ch, _ in binary_list]
    print(len(sorted_char_list))
    binary_dict = dict(binary_list)

    with open(compressed_file, 'wb') as destination:
        destination.write(chr(R).encode())
        destination.write(struct.pack('I', len(sorted_char_list)))

        bin_array = list()

        try:
            for char in text_to_encrypt:
                if char in binary_dict:
                    binary_value = binary_dict[char]
                    for binary_value_to_save in binary_value:
                        bin_array.append(True if binary_value_to_save == '1' else False)
                else:
                    print("Error with dictionary values!")
                    sys.exit(1)
            if R != 0:
                for i in range(R):
                    bin_array.append(False)
        except TypeError:
            print("File is empty!")

        try:
            chunks = [bin_array[i:i + 8] for i in range(0, len(bin_array), 8)]
            for chunk in chunks:
                packed_bytes = 0
                for i, bit in enumerate(chunk):
                    packed_bytes |= bit << (7 - i)
                destination.write(struct.pack('B', packed_bytes))

        except TypeError:
            print("File is empty!")
