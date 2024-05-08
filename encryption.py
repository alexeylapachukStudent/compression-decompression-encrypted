from random import choice


def generate_prime_numbers(num):
    if num < 2:
        return []

    sieve = [True] * (num + 1)
    sieve[0] = sieve[1] = False

    for i in range(2, int(num ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, num + 1, i):
                sieve[j] = False

    return [prime for prime, is_prime in enumerate(sieve) if is_prime]


def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1


def main_rsa(key_size):
    prime_array = generate_prime_numbers(key_size // 2)
    p, q = 0, 0
    while p == q:
        p, q = choice(prime_array), choice(prime_array)

    mod, phi = p * q, (p - 1) * (q - 1)

    phi_prime_numbers = generate_prime_numbers(phi)
    filtred_phi_prime_numbers = [each_value for each_value in phi_prime_numbers if phi % each_value != 0]

    e = choice(filtred_phi_prime_numbers)
    d = mod_inverse(e, phi)

    public_key, private_key = (e, mod), (d, mod)

    with open('public_key.pem', 'w') as f:
        f.write(str(public_key[0]) + '\n')
        f.write(str(public_key[1]) + '\n')

    with open('private_key.pem', 'w') as f:
        f.write(str(private_key[0]) + '\n')
        f.write(str(private_key[1]) + '\n')


def encrypt_message_RSA(message_to_encrypt, public_key):
    e, mod = public_key

    encrypt = [pow(ord(value), e, mod) for value in message_to_encrypt]
    return encrypt


def decrypt_message_RSA(encrypt_message, private_key):
    d, mod = private_key

    decrypt = [chr(pow(value, d, mod)) for value in encrypt_message]
    return ''.join(decrypt)


main_rsa(1024)
