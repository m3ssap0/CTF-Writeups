# Access Denied 1.2 2018 – ASSEMBLY 

* **Category:** reverse
* **Points:** 400

## Challenge

> 0xeax stumbled upon Shellphish team. They gave him an **asm** file that is broken and **another file** which has the data section of that asm file.
>
> See if you can help 0xeax in getting the flag so that he can join Shellphish.
>
> Download files from :
>
> Assembly File : [https://accessd.sfo2.digitaloceanspaces.com/assembly350/asmb.asm](asmb.asm)
>
> Data Section : [https://accessd.sfo2.digitaloceanspaces.com/assembly350/data](data)

## Solution

It is sufficient to merge the ASM code provided into two files and to execute it, e.g. an [on-line tool](https://www.tutorialspoint.com/compile_assembly_online.php) can be used.

```assembly
section	.text
	global main       
main:
    mov ecx, 41
lop:
    mov eax, msg
    add eax, ecx
    mov edx, 0
    mov edx, [eax]
    xor edx, 0xb
    mov [eax], edx
    mov edx, 0
    mov dx, [eax]
    rol dx, 0x5
    mov edx, 0
    mov dl, [eax]
    ror dl, 0x9d
    sub ecx, 1
    cmp ecx, 0
    jge lop
	mov	edx, 41
	mov	ecx, msg    
	mov	ebx, 1	    
	mov	eax, 4	    
	int	0x80        
	mov	eax, 1	   
	int	0x80

section .data
   msg	db	0x6a, 0x68, 0x68, 0x6e, 0x78, 0x78, 0x6f, 0x6e, 0x65, 0x62, 0x6e, 0x6f, 0x70, 0x3a, 0x54, 0x67, 0x3b, 0x7d, 0x38, 0x54, 0x73, 0x33, 0x3d, 0x54, 0x3f, 0x78, 0x78, 0x38, 0x66, 0x69, 0x67, 0x72, 0x54, 0x3e, 0x3d, 0x33, 0x33, 0x7a, 0x78, 0x3e, 0x76
```

The flag is:

```
accessdenied{1_l0v3_x86_4ss3mbly_5688qs5}
```