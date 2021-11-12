# Hammer To Fall

killerqueenCTF

```python
'''
-ZeroDayTea
Dynamically sized integers huh
'''
import numpy as np

a = np.array([0], dtype=int)
val = int(input("THis hammer hits so hard it creates negative matter\n"))
if(val == -1):
	exit()
a[0] = val
a[0] = (a[0] * 7) + 1
print(a[0])
if(a[0] == -1):
	print("flag!")
```

python int data type in range **2147483648** through **2147483647**. (32bit)

and [-2^63, 2^63 – 1] = **[ -9223372036854775808 , 9223372036854775807 ]** (64bit)

```python
Python 2.7.18
>>> 9223372036854775807 / 7
1317624576693539401
>>> (9223372036854775807 + 9223372036854775807) / 7
2635249153387078802L
```

```
1317624576693539401 => -9223372036854775808
2635249153387078802 => -1
```