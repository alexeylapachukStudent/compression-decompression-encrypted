from compression import compression
from decompression import decompression
generated_file = "generate_to_compress.txt"
compressed_file = "compressed.txt"
private_key_file = "private_key.pem"
destination_file = 'destination_file.txt'

if __name__ == "__main__":
    compression(generated_file, compressed_file)
    decompression(compressed_file, private_key_file, destination_file)