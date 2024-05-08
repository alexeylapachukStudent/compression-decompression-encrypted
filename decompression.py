import math
import struct
from compression import translating_to_binary_char
from encryption import decrypt_message_RSA


def decompression(decompression_file, private_key_file):
    with open(private_key_file, 'r') as f:
        private_key = tuple()
        first_value = int(f.readline().strip())

        private_key += (first_value,)

        second_value = int(f.readline().strip())
        private_key += (second_value,)

    with open(decompression_file, "rb") as destination:
        R = ord(destination.read(1))
        char_list_len = struct.unpack('I', destination.read(4))[0]
        encrypted_message = destination.read(char_list_len)
        packed_data = destination.read()

    x = char_list_len
    N = math.ceil(math.log2(x))

    binary_representation = [translating_to_binary_char(i, N) for i in range(x)]
    bin_array = [(byte >> i) & 1 for byte in packed_data for i in range(7, -1, -1)]
    ch_bin_array = ['1' if value == 1 else '0' for value in bin_array]

    if R != 0:
        ch_bin_array = ch_bin_array[:-R]
