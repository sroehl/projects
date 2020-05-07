from cryptography.fernet import Fernet


class Encryption:

    def decrypt(self, encrypted_content):
        return self.f.decrypt(encrypted_content.encode('utf-8')[2:])

    def encrypt(self, content):
        return self.f.encrypt(content.encode('utf-8'))

    def load_key(self):
        try:
            file = open(self.key_file, 'rb')
            self.key = file.read()
            file.close()
        except FileNotFoundError:
            self.key = Fernet.generate_key()
            file = open('key.key', 'wb')
            file.write(self.key)
            file.close()

    def __init__(self, key_file):
        self.key_file = key_file
        self.key = None
        self.load_key()
        self.f = Fernet(self.key)


