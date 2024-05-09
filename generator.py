import random
import string


# Funckja generowania danych dla kompresji


def generate_random_string(kbites, num_of_unique_symbols, generate_file):
    # Ogólna ilość bajtów dla generaowania danych

    num_chars = kbites * 1024

    if 0 < num_of_unique_symbols < 128

        # Generowanie listy unikalnych wartości za pomocą string.printable oraz random

        unique_chars = random.sample(string.printable, min(num_of_unique_symbols, len(string.printable)))

        # Tworzenie stringa zgodnie z ilośćią bajtów i ilością unikalnych wartości

        string_of_unique_chars = "".join(random.choice(unique_chars) for _ in range(num_chars))

    else:
        return None

    # Zapisywanie zgenerowanych danych dla kompresji w plik

    with open(generate_file, 'w') as f:
        f.write(string_of_unique_chars)
