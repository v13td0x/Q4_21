# Single number[easy]

Given a **non-empty** array of integers `nums`, every element appears *twice* except for one. Find that single one.

You must implement a solution with a linear runtime complexity and use only constant extra space.

**Ex1:**

```
Input: nums = [2,2,1]
Output: 1
```

**Ex2:**

```
Input: nums = [4,1,2,1,2]
Output: 4
```

***Ex3:***

```
Input: nums = [1]
Output: 1
```

---

solution:
```
0 xor x = x
x xor x = 0
(a xor b) xor c = a xor (b xor c)
```

```cpp
int x = 0;
for(int e : nums)
	x ^= e;
return x;
```
