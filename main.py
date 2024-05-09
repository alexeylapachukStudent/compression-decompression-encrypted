from generator import generate_random_string
from compression import compression
from decompression import decompression

generated_file = "generated_to_compress.txt"
compressed_file = "compressed.txt"
private_key_file = "private_key.pem"
destination_file = 'destination_file.txt'

if __name__ == "__main__":
    generate_random_string(2, 2, generated_file)
    compression(generated_file, compressed_file)
    decompression(compressed_file, private_key_file, destination_file)
