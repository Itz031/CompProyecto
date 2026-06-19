.386
.model flat, stdcall
option casemap :none
include \masm32\include\windows.inc
include \masm32\include\kernel32.inc
include \masm32\include\masm32.inc
includelib \masm32\lib\kernel32.lib
includelib \masm32\lib\masm32.lib

.data
    txt_sum db "Suma (5+3): ", 0
    fmt db "%d", 10, 13, 0
.bss
    buffer db 20 dup(?)
.code
start:
    invoke StdOut, addr txt_sum
    mov eax, 5
    mov ebx, 3
    add eax, ebx
    invoke wsprintf, addr buffer, addr fmt, eax
    invoke StdOut, addr buffer
    invoke ExitProcess, 0
end start