import hashlib

def shift(b, i):
   return(b[i:] + b[:i])
      
def put_placeholder(b, m):
   return(b[:m] + "?" + b[m:])

def find_candidate(b):
   i = len(b)
   while(i > 0):
   
      # Revert the shift operation.
      r = len(b) - i
      b = shift(b, r)
   
      # Put a placeholder where the char was dropped.
      l = len(b) + 1
      m = l % i
      b = put_placeholder(b, m)
   
      i -= 1
   
   return b
   
def set_to_zero_most_significant_bit_of_each_byte(candidate):
   l = list(candidate)
   for p in range(0, len(l)):
      if p % 8 == 0 and l[p] == "?":
         l[p] = "0"
   return "".join(l)

def set_char(string, char, position):
   l = list(string)
   l[position] = char
   return "".join(l)
   
def compose_flag(candidate):
   flag = ""
   i = 0
   while(i < len(candidate)):
      x = int(candidate[i:(i+8)], 2)
      if x < 256:
         flag += chr(x)
         i += 8
      else:
        break
   
   return flag
   
   
def find_flag_r(compressed, candidate, position):

   if position >= len(candidate):
      flag = compose_flag(candidate)
      if len(flag) == 6 and hashlib.sha256("evlz{{{}}}ctf".format(flag)).hexdigest() == "e67753ef818688790288702b0592a46c390b695a732e1b9fec47a14e2f6f25ae":
         print ">>> Found! >>> {}".format(candidate)
         print ">>>>>>>>>>>>>> evlz{{{}}}ctf".format(flag)
   else:
      if candidate[position] == "?":
          candidate = set_char(candidate, "0", position) 
          find_flag_r(compressed, candidate, position + 1)
          candidate = set_char(candidate, "1", position) 
          find_flag_r(compressed, candidate, position + 1)
          candidate = set_char(candidate, "?", position) 
      else:
         find_flag_r(compressed, candidate, position + 1)
       
       
     
compressed = "100001000100110000000100"
candidate = find_candidate(compressed)
print "Dirty candidate = {}".format(candidate)
candidate = set_to_zero_most_significant_bit_of_each_byte(candidate)
print "Clean candidate = {}".format(candidate)
find_flag_r(compressed, candidate, 0)