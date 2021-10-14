```apl
Arch:     amd64-64-little
RELRO:    Partial RELRO	# GOT
Stack:    No canary found # BOF
NX:       NX enabled
PIE:      No PIE (0x400000) # ROP
```

```c
main(void){
  undefined local_c [4];
  alarm(0x25);
  read(0,local_c,0x200);
  return 0;
}
```

**ret2csu**

```assembly
4011b0:   4c 89 f2                mov    rdx,r14
4011b3:   4c 89 ee                mov    rsi,r13
4011b6:   44 89 e7                mov    edi,r12d
4011b9:   41 ff 14 df             call   QWORD PTR [r15+rbx*8]
4011bd:   48 83 c3 01             add    rbx,0x1
4011c1:   48 39 dd                cmp    rbp,rbx
4011c4:   75 ea                   jne    4011b0 <__libc_csu_init+0x40>
4011c6:   48 83 c4 08             add    rsp,0x8
4011ca:   5b                      pop    rbx
4011cb:   5d                      pop    rbp
4011cc:   41 5c                   pop    r12
4011ce:   41 5d                   pop    r13
4011d0:   41 5e                   pop    r14
4011d2:   41 5f                   pop    r15
4011d4:   c3                      ret
```

No GOT functions that will emit anything, so no easy way to leak libc.

First pass with *ret2csu*. This will call `read(stdin, elf.got.alarm, read 1 byte)`. When this executes, `read` will *read* one byte and store it at the address of `alarm` in the GOT overwriting its LSB. Because we brute force since we dont know about remote libc.

Second pass with *ret2csu*. Assuming that after first pass `alarm` is `syscall`, we want to setup for `execve`, but first we need to *read* in the string `/bin/sh\0` to memory. Above, `read` will be used again, but this time to *read* from stdin the string `/bin/sh\0` + padding for a total of `0x3b` bytes. This will yield two benefits, first, we will have the string `/bin/sh` in memory for `execve`, and second, `rax` will be set to `0x3b`, which is the syscall number for `execve` .

 `read(stdin, elf.bss, 59)` -> `io.send(b'/bin/sh\0' + (0x3b - 8) * b'A')`

Third pass, with ret2csu, setup reg and call `execve(elf.bss, 0, 0)` by call r15 = elf.got.alarm.

