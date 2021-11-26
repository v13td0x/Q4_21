similar to [magic-marker](https://github.com/v13td0x/Q4_21/tree/main/DamCTF21/pwn/_magic%20marker), but we don't have quit option, must know right pos in maze to quit then our ROP chain will execute.
> The intended solution for sir-marksalot uses a stack leak of the pointer to the room the grue is in (move to the left at the top left corner of the maze) and calculates the address of the start of the maze using the random values for the row and column of the grue that are calculated at the start of the play_maze function (time-based random seed for stdlib rand)
>
