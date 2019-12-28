import sys, getopt, os
import requests
import struct, codecs
from Crypto.PublicKey import RSA

# Factorizes the modulus using a remote service.
def factorize_modulus(modulus):
   print "[*] Factorizing modulus."
   
   remote_service = "http://factordb.com/api"
   print "[*] Contacting service: {}.".format(remote_service)
   response = requests.get(remote_service, params={"query": str(modulus)}).json()
   
   if response is not None and len(response["factors"]) != 2:
      print "[!] {} factors returned.".format(len(response["factors"]))
      sys.exit(2)

   p = int(response["factors"][0][0])
   q = int(response["factors"][1][0])
   print "[*] p ..........: {}".format(p)
   print "[*] q ..........: {}".format(q)
   
   return p, q

# Computes value for decrypt operation.
def compute_values(exponent, p, q):
   print "[*] Computing values."
   
   # Compute phi(n).
   phi = (p - 1) * (q - 1)
   print "[*] phi ........: {}".format(phi)

   # Compute modular inverse of e.
   gcd, a, b = egcd(exponent, phi)
   d = a
   d = d % phi;
   if d < 0:
      d += phi
   print "[*] d ..........: {}".format(d)
   
   return d

# Modular inverse.
def egcd(a, b):
   x,y, u,v = 0,1, 1,0
   while a != 0:
      q, r = b//a, b%a
      m, n = x-u*q, y-v*q
      b,a, x,y, u,v = a,r, u,v, m,n
      gcd = b
   return gcd, x, y

# Decrypting the encrypted content.
def decrypt(content_to_decrypt, modulus, d):
   plain_content = ""
   for c in content_to_decrypt:
      p = pow(int(c, 16), d, modulus)
      plain_content += codecs.decode(str(hex(p)).replace("0x", "").replace("L", ""), "hex")
   return plain_content

# Main execution.
if __name__ == "__main__":
   try:
      modulus = 25693197123978473
      exponent = 65537
      enc_flag = ['0x2135d36aa0c278', '0x3e8f43212dafd7', '0x7a240c1672358', '0x37677cfb281b26', '0x26f90fe5a4bed0', '0xb0e1c482daf4', '0x59c069723a4e4b', '0x8cec977d4159']
      p, q = factorize_modulus(modulus)
      d = compute_values(exponent, p, q)
      plain_content = decrypt(enc_flag, modulus, d)
      print plain_content
   except KeyboardInterrupt:
      print "[-] Interrupted!"
   except:
      print "[!] Unexpected exception: {}".format(sys.exc_info()[0])
   print "Finished."
