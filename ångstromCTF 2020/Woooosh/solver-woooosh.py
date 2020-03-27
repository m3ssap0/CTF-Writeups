#!/usr/bin/python

import requests
import time
import math

verbose = True

target_site = "https://wooooosh.2020.chall.actf.co/"
target_endpoint_without_sid = target_site + "socket.io/?EIO=3&transport=polling&t={}"
target_endpoint = target_endpoint_without_sid + "&sid={}"
headers = {
   "User-Agent": "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US);", 
   "Content-Type": "text/plain;charset=UTF-8",
   "Accept-Encoding": "gzip, deflate, br",
   "Origin": "https://wooooosh.2020.chall.actf.co",
   "Referer": "https://wooooosh.2020.chall.actf.co/",
}

def log_message(message):
    if verbose:
        print(message)


def log_data(answer):
    if verbose:
        print("-----------------------------------")
        print(answer)
        print("-----------------------------------")


def get_sid_from_cookies(cookies):
    sid = None
    #log_message("[*] Cookies:")
    for cookie in cookies:
        #log_message("[*]   - {}={}".format(cookie.name, cookie.value))
        if cookie.name == "io":
            sid = cookie.value
            #log_message("[*] Found sid: {}.".format(sid))
    return sid


def generate_t_param():
    timestamp = int(round(time.time() * 1000))
    return yeast_encode(timestamp)


# https://github.com/unshiftio/yeast/blob/28d15f72fc5a4273592bc209056c328a54e2b522/index.jsL17
def yeast_encode(num):
    alphabet = list("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_")
    length = len(alphabet)
    encoded = ""
    
    while True:
        encoded = alphabet[num % length] + encoded
        num = math.floor(num / length)
        if num <= 0:
            break
    
    return encoded


def generate_payload(payload):
    return "{}:{}".format(str(len(payload)), payload)


def generate_start_payload():
    start_payload = generate_payload("42[\"start\"]")
    #log_data(start_payload)
    return start_payload


def generate_answer_payload(x, y):
    answer_payload = generate_payload("42[\"click\",{},{}]".format(x, y))
    #log_data(answer_payload)
    return answer_payload


t = generate_t_param()
url = target_endpoint_without_sid.format(t)
#log_message("[*] Getting sid. {}".format(url))
r = requests.get(url, headers=headers)
cookies = r.cookies
#log_data(r.text)
sid = get_sid_from_cookies(cookies)

t = generate_t_param()
url = target_endpoint.format(t, sid)
#log_message("[*] Starting the game. {}".format(url))
r = requests.post(url, headers=headers, cookies=cookies, data=generate_start_payload())
cookies = r.cookies
#log_data(r.text)

#log_message("[*] Playing the game.")
score = ""
start_time = int(round(time.time() * 1000))
bad_gateway_retries = 0
while True:

    while True:
        t = generate_t_param()
        url = target_endpoint.format(t, sid)
        #log_message("[*] Polling. {}".format(url))
        r = requests.get(url, headers=headers, cookies=cookies)
        cookies = r.cookies
        content = r.text
        #log_data(content)
    
        if r.status_code == 502:
            bad_gateway_retries += 1
            t = generate_t_param()
            url = target_endpoint_without_sid.format(t)
            #log_message("[*] Getting sid. {}".format(url))
            r = requests.get(url, headers=headers)
            cookies = r.cookies
            #log_data(r.text)
            sid = get_sid_from_cookies(cookies)
        else:
            break
    
    if "actf{" in content:
        print("                                         ")
        print("[*] =====================================")
        print("[*] =====================================")
        print("[*] =====================================")
        print("[*] vvvvvvvvvvvv FLAG FOUND! vvvvvvvvvvvv")
        print("                                         ")
        print(content)
        print("                                         ")
        print("[*] ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print("[*] =====================================")
        print("[*] =====================================")
        print("[*] =====================================")
        print("                                         ")
        break
    elif "terrible" in content or "disconnected" in content:
        end_time = int(round(time.time() * 1000))
        total_time = (end_time - start_time) / 1000
        print("[*] FAILED! Score: {} ({} secs, {} 502 retries)".format(score, str(total_time), str(bad_gateway_retries)))
        break
    elif "shapes" in content:
        #log_message("[*][shapes] Response intercepted.")
        coordinates = content[21:34].replace("{", "").replace("}", "").replace("[", "").replace("]", "").replace("\"", "").replace("x", "").replace("y", "").replace(":", "")
        best_x = coordinates.split(",")[0]
        best_y = coordinates.split(",")[1]
        #log_message("[*][shapes] The best position is at {}, {}.".format(best_x, best_y))
        if "score" in content:
            score = content[-5:-1].replace("]", "").replace(",", "").replace("\"", "").replace("e", "")
            #log_message("[*][shapes] Score: {}.".format(score))
        t = generate_t_param()
        url = target_endpoint.format(t, sid)
        #log_message("[*] Send answer. {}".format(url))
        r = requests.post(url, headers=headers, cookies=cookies, data=generate_answer_payload(best_x, best_y))
        cookies = r.cookies
        content = r.text
        #log_data(content)
    elif "score" in content:
        #log_message("[*][score] Response intercepted.")
        score = content[-5:-1].replace("]", "").replace(",", "").replace("\"", "").replace("e", "")
        #log_message("[*][score] Score: {}.".format(score))