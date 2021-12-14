```css
Arch:     amd64-64-little
RELRO:    Partial RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      PIE enable
```

```c
int main(int argc, const char **argv, const char **envp)
{
  int v4; // [rsp+1Ch] [rbp-4h]

  setvbuf(_bss_start, 0LL, 2, 0LL);
  setvbuf(stdin, 0LL, 2, 0LL);
  puts("What is your shellcode?");
	// prot = 7 (rwx)
  if ( mmap((void *)0x133713370000LL, 0x1000uLL, 7, 50, -1, 0LL) != (void *)0x133713370000LL )
  {
    puts("mmap failed");
    exit(-1);
  }
  LenInp = read(0, (void *)(8LL * (len / 8) + 0x133713370000LL), 0x800uLL);
  if ( *(_BYTE *)(len + (__int64)LenInp - 1 + 0x133713370000LL) == 10 )
    *(_BYTE *)(--LenInp + (__int64)len + 0x133713370000LL) = 0;
  if ( (unsigned int)check(len + 0x133713370000LL, LenInp - 1) )
  {
    puts("Bad Character found");
    exit(-1);
  }
  ((void (*)(void))(len + 0x133713370000LL))();
  return 0;
}

// we want return 0
check(__int64 a1, int LastIdx)
{
  int v2; // eax
  while ( LastIdx >= 0 )
  {
    v2 = LastIdx--;
		// only accept even bytes for input
    if ( (*(_BYTE *)(v2 + a1) & 1) != 0 )
      return 1LL;
  }
  return 0LL;
}
```

code `((void (*)(void))(len + 0x133713370000LL))();` obivous this is shellcode chal,  `NX enabled` prompt is lying, it actually use `mmap` to create memory mapping at 0x133713370000 has `rwx` perm. Then executed our input, to solve this chall you must write your shellcode not include odd byte.

https://github.com/knittingirl/CTF-Writeups/tree/main/pwn_challs/MetaCTF21/Two's_Compliment

https://github.com/Surg-Dev/writeups/blob/master/Cybergames2021/Two's%20Compliment.md