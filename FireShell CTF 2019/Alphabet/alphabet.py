import hashlib

print "[*] Creating dictionaries."
dictionary_md5 = {}
dictionary_sha256 = {}
for i in range(32, 127):
   plain_char = chr(i)
   print "[*] Hashing char: {}".format(plain_char)
   dictionary_md5[hashlib.md5(plain_char).hexdigest()] = plain_char
   dictionary_sha256[hashlib.sha256(plain_char).hexdigest()] = plain_char

print "[*] Reading file."
with file("submit_the_flag_that_is_here.txt") as f:
   file_content = f.read()
hashed_chars = file_content.split(" ");

print "[*] Decrypting message."
decrypted_message = ""
for h in hashed_chars:
   
   decrypted_char = None
   if len(h) == 32:
      decrypted_char = dictionary_md5[h]
   elif len(h) == 64:
      decrypted_char = dictionary_sha256[h]
   
   #print "[*] Un-hashed char: {}".format(decrypted_char)
   if decrypted_char is not None:
      decrypted_message += decrypted_char

print "[*] Decrypted message:"
print decrypted_message

#Congratulations!_T#e_Flag_Is_F#{Y3aH_Y0u_kN0w_mD5_4Nd_Sh4256}