# STEM CTF Cyber Challenge 2019 – Journey to the Center of the File

* **Category:** Grab Bag
* **Points:** 100

## Challenge

> W(e( (h(a(v(e( (t(o( (g(o( (d(e(e(p(e(r)))))))))))))))))))
> 
> download

## Solution

There are different types of files nested in each other:
* zip;
* bzip2;
* gzip;
* base64 encoded data.

Nested files are hundreds, so a [Python script](journey.py) can be written to open them all.

```python
import os, base64
import bz2, zipfile, gzip
import magic # pip install python-magic

i = 0
current_file = "flag"

while True:
   new_file = "decompressed-" + str(i)

   # Analyzing file type.
   file_type = magic.from_file(current_file)
   print "[*] File '{}' is '{}'.".format(current_file, file_type)

   # Found the flag.
   with open(current_file, "r") as cf:
      read_data = cf.read()
   if "MCA{" in read_data:
      print read_data
      break

   # Analyzing archives.

   if "bzip2" in file_type:

      with open(new_file, 'wb') as nf, open(current_file, 'rb') as cf:
         decompressor = bz2.BZ2Decompressor()
         for data in iter(lambda : cf.read(100 * 1024), b''):
            nf.write(decompressor.decompress(data))

   elif "Zip" in file_type:

      with zipfile.ZipFile(current_file) as cf:
         if len(cf.namelist()) == 1:
            file_to_be_extracted = cf.namelist()[0]
         else:
            print "[!] Too much files into the archive!"
            break
         cf.extractall()
         os.rename(file_to_be_extracted, new_file)

   elif "ASCII text" in file_type:

      with open(current_file, "r") as cf:
         encoded_data = cf.read()
      decoded_data = base64.b64decode(encoded_data)
      with open(new_file, "wb") as nf:
         nf.write(decoded_data)

   elif "gzip" in file_type:

      with gzip.open(current_file, "r") as cf:
         read_data = cf.read()
      with open(new_file, "wb") as nf:
         nf.write(read_data)

   else:
      print "[!] Unknown archive, exiting."
      break

   # Removing old file and going on with analysis.
   os.remove(current_file)
   current_file = new_file
   i += 1
```

The flag is the following.

```
MCA{Wh0_Needz_File_Extensions?}
```