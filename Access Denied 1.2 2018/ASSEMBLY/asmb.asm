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