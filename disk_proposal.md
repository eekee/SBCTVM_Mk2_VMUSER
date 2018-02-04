Emulated disk interface proposal
----------------------------------------

This is my attempt at a simple-as-possible disk emulation for the mark 2. It imitates DMA in a simple way. I thought that would be better than copying in software, which seems particularly slow.
```
IO space:
size	description
2	linear word address (low, high)
1	memory start address
1	length
1	command
```
To write data to disk, write the start address and length of the data in memory, fill in the linear word address as the start of where to put it on the disk, and finally send the 'write' code to the command register. Read is very much the same, fill in the appropriate details and issue the command.

What happens after the command is written? The best choice is somewhat debatable, but I think the most orderly and simplest to use would be that the CPU is stopped, the data is read or written, and then the CPU resumes. Perhaps only one thread is stopped, or perhaps additional asynchronous versions of the commands could be provided later, but using either of these alternatives would require more care.

Having a linear address removes questions about what the sector size should be. There's nothing physical for a sector to correspond to, but even if there was I don't think it would be totally unrealistic. A real disk drive controller might read-modify-write a sector to write part of it. It's been a while since I read up on it, but I think the Atari 810 disk drive (for their 8-bit computers) could do this.

The linear address also allows all the room for expansion we could possibly want with the mark 2: 324 mega-words. :) The actual size of each disk could simply be the file size. A launcher feature could make blank disks with certain size options, but I've got dd handy anyway. :)

A question I can't avoid: what word size should the disk have? Anything less than 9 trits could be a nuisance for data, but anything more than 6 trits could be seen as wasted space for text and instructions. I came to the conclusion that 9 trits would probably be better, wasted space being the lesser nuisance. Another option is to read and write the instruction and data spaces together, almost like having 15-trit words. I like this best, particularly because I thought of using the instruction space within the VM to store text. For example, consider the wasted instruction space alongside the framebuffer or other images, or alongside 'compiled' Forth code which is mostly pointers.

Multiple disks would probably be a good idea regardless of their size, because copying from one disk to another helps the user organize. Perhaps another register could indicate which disk, or it could go in one trit of the command word.

The streg file format could specify which files to use as which disks. Perhaps they could be changed by menus, but I'd want the streg files first.

I'm not considering bootable disks. I feel they ought to have rom support, and I'd rather compile to rom anyway. Starting execution from the beginning of rom is entirely fuss-free. :)

I also don't want to consider a filesystem at this stage. A lot of Forth environments have done very well without them, dividing the disk into numbered blocks. One of the blocks contains a plain-text index, readable with the 'list' command. It's almost no code!
