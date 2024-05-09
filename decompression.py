import math
import struct
import sys

from compression import translating_to_binary_char
from encryption import decrypt_message_RSA


def decompression(decompression_file, private_key_file, destination_file):
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

    num_bytes = 2

    number_list = [int.from_bytes(encrypted_message[i:i + num_bytes], byteorder='big') for i in
                   range(0, len(encrypted_message), num_bytes)]
    try:
        decrypted_message = decrypt_message_RSA(number_list, private_key)

    except SyntaxError:
        print("Произошла ошибка синтаксиса при дешифровании.")
        sys.exit(1)

    x = char_list_len // 2
    N = math.ceil(math.log2(x))

    binary_representation = [translating_to_binary_char(i, N) for i in range(x)]
    dict_of_unique_words = dict(zip(binary_representation, decrypted_message))
    print(dict_of_unique_words)

    bin_array = [(byte >> i) & 1 for byte in packed_data for i in range(7, -1, -1)]
    ch_bin_array = ['1' if value == 1 else '0' for value in bin_array]

    if R != 0:
        ch_bin_array = ch_bin_array[:-R]

    decompressed_data = list()

    for i in range(0, len(ch_bin_array), N):
        decompressed_binary = ''.join(ch_bin_array[i:i + N])
        decompressed_data.append(dict_of_unique_words[decompressed_binary])

    with open(destination_file, 'w') as file:
        for each_value in decompressed_data:
            file.write(each_value)
