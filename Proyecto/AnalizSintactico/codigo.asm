.386
.model flat, stdcall
option casemap :none
include \masm32\include\windows.inc
include \masm32\include\kernel32.inc
include \masm32\include\masm32.inc
includelib \masm32\lib\kernel32.lib
includelib \masm32\lib\masm32.lib

.data
    i DWORD 0
    str_1 db 'Iteracion', 10, 13, 0
    x DWORD 0
    str_2 db 'X es igual a 10', 10, 13, 0
    buffer db 20 dup(0)
    fmt db '%d', 10, 13, 0

.code
start:
    mov eax, 0
    mov i, eax
Label_1_WHILE_INICIO:
    mov eax, i
    mov ecx, eax
    mov eax, 3
    cmp ecx, eax
    jge Label_2_WHILE_FIN
    invoke StdOut, addr str_1
    invoke wsprintf, addr buffer, addr fmt, i
    invoke StdOut, addr buffer
    mov eax, i
    mov ebx, eax
    mov eax, 1
    add eax, ebx
    mov i, eax
    jmp Label_1_WHILE_INICIO
Label_2_WHILE_FIN:
    mov eax, 10
    mov x, eax
    mov eax, x
    mov ecx, eax
    mov eax, 10
    cmp ecx, eax
    jne Label_3_IF_FIN
    invoke StdOut, addr str_2
Label_3_IF_FIN:
    invoke ExitProcess, 0
end start
