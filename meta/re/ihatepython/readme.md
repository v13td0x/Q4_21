# Untitled

```python
print(c)
kn = [47, 123, 113, 232, 118, 98, 183, 183, 77, 64, 218, 223, 232, 82, 16, 72, 68, 191, 54, 116, 38, 151, 174, 234, 127]
valid = len(list(filter(lambda s: kn[s[0]] == s[1], enumerate(c))))
if valid == 25:
	print("Password is correct! Flag:", x)
else:
	print("WRONG!!!!!!")
```

combo of `filter` with `lambda` is cmp `kn[s[0]]` and `s[1]` , s[0] is idx of list c and s[1] is value of list c, so `c` must equal with `kn`, now we have already known `list c`

---

U can ezly find a, k. Now we find the password x

```python
a = { b: do_thing(ord(c), d) for (b, c), d in zip(enumerate(x), k) }
```

before that, let's look `do_thing` funct

```python
def do_thing(a, b):
    return ((a << 1) & b) ^ ((a << 1) | b)
```

```python
# solve
import string
for i in range(25):
	for c in string.printable:
		if(do_thing(ord(c), k[i]) == a[i]):
			print(c, end ='')
# MetaCTF{yOu_w!N_th1$_0n3}
```