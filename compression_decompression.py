import math
import struct
from collections import Counter

# Pliki używane do kompresji i dekompresji 

generated_file = "generated.txt"
destination_file = "compressed.txt"
decompression_file = "decompressed.txt"


# Funckja, która tłumuczy zapis dziesiętny na zapis binarny
def translating_to_binary_char(symbol, length):
    bin_symbol = bin(symbol)[2::]
    extended_symbol = bin_symbol.rjust(length, "0")
    return extended_symbol


# Pobieranie zawartości pliku
with open(generated_file, 'r') as file:
    text_to_encrypt = file.read()


# Funkcja, zawierająca wszystkie dane użytkownika
def data():
    k = len(text_to_encrypt)  # Ilość występujących symboli w tekście
    x = len(set(text_to_encrypt))  # Ilość unkilanych symboli w tekście
    N = math.ceil(math.log2(x))  # Dlugość bitów dla zapisania jednej wartości
    R = (8 - (k * N) % 8) % 8  # Bity uzupełniające

    return k, x, N, R


# Funkcja sortownia ilości elementów zgdodnie z zapisem binaranym

def sort_binary_frequency_of_symbols():
    # Obliczenie ilości unilanych elementów
    unique_words_dict = Counter(text_to_encrypt)

    # Sprawdzenia czy słownik nie jest pusty

    if len(unique_words_dict):

        # Pobieranie danych

        k, x, N, R = data()

        binary_representation = list()

        # Tworzenie liczb binarnych dla każdego elemnetu

        for i in range(x):
            binary_representation.append(translating_to_binary_char(i, N))

        binary_list = []

        # Przejście po unikalnym wartościom: symbol oraz binarne reprezentowanie ilości wystąpień

        for i, (ch, count) in enumerate(unique_words_dict.most_common()):
            binary_representation_for_ch = binary_representation[i]
            binary_list.append((ch, binary_representation_for_ch))

        if R != 0:
            binary_list.append(("rest", translating_to_binary_char(x, R)))

        # Tworzenie słownika dla wygodnego wykorzystanie danych
        binary_dict = dict(binary_list)

        return binary_dict

    else:
        return ""


# Funckja tłumacząca bity 0 oraz 1 na bajty


def pack_array_of_bools():
    with open(generated_file, 'r') as generated_text:

        # Pobieranie danych
        k, x, N, R = data()
        bin_array, binary_dict = list(), sort_binary_frequency_of_symbols()

        # Przedstawenie charów na bity True lub False

        for char in generated_text.read():
            if char in binary_dict:
                binary_value = binary_dict[char]
                for bin_value_to_save in binary_value:
                    bin_array.append(True if bin_value_to_save == '1' else False)
        # Sprawdzenie czy bity uzupełniające nie równe zero:

        if R != 0:
            for char in binary_dict['rest']:
                for bin_value_to_save in char:
                    bin_array.append(True if bin_value_to_save == '1' else False)

        return bin_array


# Funkcja zapisywania kodu do pliku w postaci bajtów

def saving_to_file():
    with open(destination_file, 'wb') as destination:
        bin_array = pack_array_of_bools()
        try:
            chunks = [bin_array[i:i + 8] for i in range(0, len(bin_array), 8)]
            for chunk in chunks:
                packed_bytes = 0
                for i, bit in enumerate(chunk):
                    packed_bytes |= bit << (7 - i)
                destination.write(struct.pack('B', packed_bytes))
        except TypeError:
            print("File is empty!")


# Funckja dekompresji
def decompression():
    with open(destination_file, "rb") as destination:
        packed_data = destination.read()

    # Wczytanie każdej wartości kompresowanego pliku, czyli każdego bajtu

    bool_array = list()
    for byte in packed_data:
        for i in range(7, -1, -1):
            # Tłumaczenie każdego bitu na str
            bool_array.append(chr(ord('0') + ((byte >> i) & 1)))

    bin_dict = sort_binary_frequency_of_symbols()

    # Odwrócenie słownika: wartości i kluczów

    reversed_bin_dict = {ch: freq for freq, ch in bin_dict.items()}

    k, x, N, R = data()

    # Odcięcie bitów uzupełniających w przypadku je istnienia

    if R != 0:
        bool_array = bool_array[:-R]

    decompressed_data = list()

    # Sprawdzenie każdej N odległości pomiędzy bitami

    for i in range(0, len(bool_array), N):
        compressed_data = "".join(bool_array[i:i + N])
        decompressed_data.append(reversed_bin_dict[compressed_data])

    # Zapisanie danych do pliku

    with open(decompression_file, 'w') as decompressed_text:
        for each_value in decompressed_data:
            decompressed_text.write(each_value)


# Głowna funkcja
def main():
    saving_to_file()
    decompression()


if __name__ == "__main__":
    main()

