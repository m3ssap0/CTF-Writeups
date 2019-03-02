# STEM CTF Cyber Challenge 2019 – In Plain Text

* **Category:** Binary RE
* **Points:** 50

## Challenge

> Created by: David Maples
> 
> Starring: Mary McCormack, Fred Weller, Nichole Hiltz, Todd Williams, Lesley Ann Warren, Paul Ben-Victor, Cristián de la Fuente, Rachel Boston
> 
> [download](challenge)

## Solution

Using `strings` command on the given ELF file you will discover the flag in plain text.

```
$ strings challenge 
/lib/ld-linux.so.2
libc.so.6
_IO_stdin_used
puts
stdin
printf
fgets
__cxa_finalize
strcmp
__libc_start_main
__stack_chk_fail
GLIBC_2.1.3
GLIBC_2.4
GLIBC_2.0
_ITM_deregisterTMCloneTable
__gmon_start__
_ITM_registerTMCloneTable
UWVS
[^_]
Hey there, I know I am the challenge and all, but I forgot what the flag was...
Could you just tell me the flag real quick? Please? 
MCA{y3ah_sur3_here_y0u_g0}
That definitely rings a bell! Thank you!
That doesn't sound familiar... :/
;*2$"
GCC: (Ubuntu 7.3.0-16ubuntu3) 7.3.0
crtstuff.c
deregister_tm_clones
__do_global_dtors_aux
completed.7281
__do_global_dtors_aux_fini_array_entry
frame_dummy
__frame_dummy_init_array_entry
challenge.c
__FRAME_END__
__init_array_end
_DYNAMIC
__init_array_start
__GNU_EH_FRAME_HDR
_GLOBAL_OFFSET_TABLE_
__libc_csu_fini
strcmp@@GLIBC_2.0
_ITM_deregisterTMCloneTable
__x86.get_pc_thunk.bx
printf@@GLIBC_2.0
fgets@@GLIBC_2.0
_edata
__stack_chk_fail@@GLIBC_2.4
__x86.get_pc_thunk.dx
__cxa_finalize@@GLIBC_2.1.3
__data_start
puts@@GLIBC_2.0
__gmon_start__
__dso_handle
_IO_stdin_used
__libc_start_main@@GLIBC_2.0
__libc_csu_init
stdin@@GLIBC_2.0
_fp_hw
__bss_start
main
__stack_chk_fail_local
__TMC_END__
_ITM_registerTMCloneTable
.symtab
.strtab
.shstrtab
.interp
.note.ABI-tag
.note.gnu.build-id
.gnu.hash
.dynsym
.dynstr
.gnu.version
.gnu.version_r
.rel.dyn
.rel.plt
.init
.plt.got
.text
.fini
.rodata
.eh_frame_hdr
.eh_frame
.init_array
.fini_array
.dynamic
.data
.bss
.comment
```

The flag is the following.

```
MCA{y3ah_sur3_here_y0u_g0}
```