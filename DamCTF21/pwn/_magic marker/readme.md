> NO PIE
> 

```c
play_maze()
{
	int y0; // er14
	int v1; // eax
	int64 y; // rbx
	int64 x; // r12
	unsigned int x0; // er13
	char choice; // bp
	char s[51208]; // [rsp+10h] [rbp-C848h] BYREF
	unsigned int64 canary; // [rsp+C818h] [rbp-40h]

	memset(s, 0, 0xC800);
	y0 = rand() % 40;
	v1 = rand();
	y = y0;
	x = v1 % 40;
	x0 = v1 % 40;
	generate_maze(s);
	while (1)
	{
CHECK_NEXT_MOVE:
		puts("This room has exits to the ");
		// mov 	eax, [rsp+rbp+0C858h+var_C82C]
		EAX = *(_DWORD *)&s[1280 * y + 28 + 32 * x];
		// 8 = 0000 1000
		if ( (EAX & 8) != 0 )
		{
			puts("North");
			EAX = *(_DWORD *)&s[1280 * y + 28 + 32 * x];
		}
		// 4 = 0000 0100
		if ( (EAX & 4) != 0 )
		{
			puts("East");
			EAX = *(_DWORD *)&s[1280 * y + 28 + 32 * x];
		}
		// 2 = 0000 0010
		if ( (EAX & 2) != 0 )
		{
			puts("South");
			EAX = *(_DWORD *)&s[1280 * y + 28 + 32 * x];
		}
		// 1 = 0000 0001
		if ( (EAX & 1) != 0 )
			puts("West");
		if ( s[1280 * y + 32 * x] )
			printf("On the wall is written: %s\n", &s[1280 * y + 32 * x]);
		printf("\nWhat would you like to do? (w - go north, a - go west, s - go south, d - go east, x - write something, m - show map, q - give up): ");
		choice = fgetc(stdin);
		if (choice != 10)
			break;
invalidChoice:
		puts("I'm not sure I understand.");
	}
	while ( fgetc(stdin) != 10 )
		;
	switch ( choice )
	{
		case 'a': // left
			if ( (s[1280 * y + 28 + 32 * x] & 1) == 0 )
				goto invalidMove;
			x = (int)--x0;
			goto CHECK_NEXT_MOVE;
		case 'd': // right
			if ( (s[1280 * y + 28 + 32 * x] & 4) == 0 )
				goto invalidMove;
			x = (int)++x0;
			goto CHECK_NEXT_MOVE;
		case 'm':
			print_maze(s, (unsigned int)y0, x0);
			goto CHECK_NEXT_MOVE;
		case 'q':
			return __readfsqword(0x28u) ^ canary;
		case 's': // up
			if ( (s[1280 * y + 28 + 32 * x] & 2) == 0 )
				goto invalidMove;
			y = ++y0;
			goto CHECK_NEXT_MOVE;
		case 'w': // down
			if ( (s[1280 * y + 28 + 32 * x] & 8) != 0 )
				y = --y0;
			else
invalidMove:
				puts("There's a wall there.");
			goto CHECK_NEXT_MOVE;
		case 'x':
			puts("Your magnificently magestic magic marker magically manifests itself in your hand. What would you like to write?");
			fgets(&s[1280 * y + 32 * x], 33, stdin);
			goto CHECK_NEXT_MOVE;
		default:
			goto invalidChoice;
	}
}
```

`fgets(&s[1280 * y + 32 * x], 33, stdin)` in case 'x' and `s[1280 * y + 28 + 32 * x]` when check next move with 8, 4, 2, 1. If  we input `'\xFF'*32` we can move any direction

```c
// before we find x, y or our pos in maze size 40x40
// can write a small c prog to get 2 rand but can not right with remote
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
int main() {
  time_t t = time(0);
  srand(t);
  int n1 = rand() % 40;
  int n2 = rand() % 40;
  printf("%d\n", n1);
  printf("%d\n", n2);
  return 0;
}
```

we use bof `maze[]`  to overwrite ret addr without change canary. 2 ways are `a` (x = —x0), `w` (y = —y0) and `d` (x = ++x0), `s`(y =  ++y0) to increase index of `maze[]`

this maze is actually a array, so move to the lower right, this is at the end of the allocated buffer for the maze and not far from the return address. with `d` and `s`
