class Token:
    @staticmethod
    def generate_token(text, length=16):
        import hashlib
        hash_object = hashlib.md5(text.encode())
        token = hash_object.hexdigest()[:length]
        return token

    @staticmethod
    def validate_token(token, text):
        expected_token = Token.generate_token(text, length=len(token))
        return token == expected_token

    @staticmethod
    def help():
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                          TOKEN HELP                               ║
╠══════════════════════════════════════════════════════════════════╣
║ Token generates and validates confirmation tokens.              ║
║                                                                   ║
║ Tokens are MD5 hashes of content, ensuring that if content      ║
║ changes between preview and execution, the token won't match.   ║
║                                                                   ║
║ METHODS:                                                          ║
║   generate_token(text, length=16)  - Create token from text     ║
║   validate_token(token, text)      - Check if token matches     ║
╚══════════════════════════════════════════════════════════════════╝
""")
