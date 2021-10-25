import pyaes


class Aes(object):
    @staticmethod
    def encrypt(plaintext, key):
        plaintext_bytes = [ord(c) for c in plaintext]

        aes = pyaes.AES(key.encode("UTF-8"))

        ciphertext = aes.encrypt(plaintext_bytes)

        return "".join(chr(i) for i in ciphertext)

    @staticmethod
    def decrypt(ciphertext, key):
        ciphertext_bytes = [ord(c) for c in ciphertext]

        aes = pyaes.AES(key.encode("UTF-8"))

        plaintext = aes.decrypt(ciphertext_bytes)

        return "".join(chr(i) for i in plaintext)

    @staticmethod
    def cbc_encrypt(plaintext, init_vector, key, block_size=16):
        plaintext = Aes.add_padding(plaintext, block_size)
        vector = str(init_vector)

        blocks = [plaintext[i:i+block_size] for i in range(0, len(plaintext), block_size)]
        ciphertext = ""

        for block in blocks:
            block_to_encrypt_as_list = [chr(ord(char1) ^ ord(char2)) for char1, char2 in zip(vector, block)]
            block_to_encrypt = "".join(block_to_encrypt_as_list)
            cipher_block = Aes.encrypt(block_to_encrypt, key)
            ciphertext += cipher_block
            vector = cipher_block

        return ciphertext

    @staticmethod
    def add_padding(plaintext, block_size=16):
        padding = ""

        for space_remaining in range(len(plaintext) % block_size, (len(plaintext) // block_size + 1) * block_size):
            padding += " "

        plaintext += padding
        return plaintext

    @staticmethod
    def cbc_decrypt(ciphertext, init_vector, key, block_size=16):
        vector = str(init_vector)

        cipher_blocks = [ciphertext[i:i + block_size] for i in range(0, len(ciphertext), block_size)]
        plaintext = ""

        for cipher_block in cipher_blocks:
            decrypted_block = Aes.decrypt(cipher_block, key)
            block_as_list = [chr(ord(char1) ^ ord(char2)) for char1, char2 in zip(vector, decrypted_block)]
            block = "".join(block_as_list)
            plaintext += block
            vector = cipher_block

        return plaintext.rstrip()

    @staticmethod
    def ecb_encrypt(plaintext, key, block_size=16):
        plaintext = Aes.add_padding(plaintext, block_size)

        blocks = [plaintext[i:i + block_size] for i in range(0, len(plaintext), block_size)]
        ciphertext = ""

        for block in blocks:
            cipher_block = Aes.encrypt(block, key)
            ciphertext += cipher_block

        return ciphertext

    @staticmethod
    def ecb_decrypt(ciphertext, key, block_size=16):
        cipher_blocks = [ciphertext[i:i + block_size] for i in range(0, len(ciphertext), block_size)]
        plaintext = ""

        for cipher_block in cipher_blocks:
            block = Aes.decrypt(cipher_block, key)
            plaintext += block

        return plaintext.rstrip()
