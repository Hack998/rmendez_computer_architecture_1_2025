section .data
    filename db "cuadrante.img", 0  ; Path del archivo
    newline db 10                  ; Nueva linea ('\n')
    fd dd 0                        
    buffer db 0                    ; Buffer para la semilla

section .text
    global _start

_start:
    ; Abre archivo
    mov eax, 5          
    mov ebx, filename  
    mov ecx, 2           ; read/write
    mov edx, 0           
    int 0x80
    mov [fd], eax        ; Guarda descripcion del archivo

    ; Leer semilla
    mov eax, 3         
    mov ebx, [fd]       
    mov ecx, buffer   
    mov edx, 4        
    int 0x80

    mov edi, 5          ; Iteraciones

loop:
    mov esi, [buffer]

    inc esi

    mov [buffer], esi
test:

    dec edi
    jnz loop

    ; Cierra archivo
    mov eax, 6
    mov ebx, [fd]
    int 0x80

    ; Exit
    mov eax, 1
    xor ebx, ebx
    int 0x80
