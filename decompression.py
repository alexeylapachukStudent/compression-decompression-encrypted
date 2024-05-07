import math
import struct


def decompression(decompression_file):
    with open(decompression_file, "rb") as destination:
        R = ord(destination.read(1))
        char_list_len = struct.unpack('I', destination.read(4))[0]
        packed_data = destination.read()

    bin_array = [(byte >> i) & 1 for byte in packed_data for i in range(7, -1, -1)]
    ch_bin_array = ['1' if value == 1 else '0' for value in bin_array]

    N = math.ceil(math.log2(char_list_len))

    if R != 0:
        ch_bin_array = ch_bin_array[:-R]
        
