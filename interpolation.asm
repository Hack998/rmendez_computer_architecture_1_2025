section .data
    filename db "cuadrante.img", 0  ; Path del archivo
    fileout db "r.img", 0
    newline db 10                  ; Nueva linea ('\n')
    fd_in dd 0                        
    fd_out dd 0                        
    buffer db 0                    ; Buffer
    pos_1 db 0
    pos_2 db 0
    pos_3 db 0
    pos_4 db 0

section .text
    global _start

_start:
    ; Abre archivo
    mov eax, 5          
    mov ebx, filename  
    mov ecx, 2           ; read/write
    mov edx, 0           
    int 0x80
    mov [fd_in], eax        ; Guarda descripcion del archivo

    ; Abre archivo
    mov eax, 5          
    mov ebx, fileout  
    mov ecx, 2           ; read/write
    mov edx, 0           
    int 0x80
    mov [fd_out], eax        ; Guarda descripcion del archivo

    ; Leer primera linea
    mov eax, 3         
    mov ebx, [fd_in]       
    mov ecx, buffer   
    mov edx, 4        
    int 0x80

    mov edi, 1          ; Iteraciones

loop:
    mov esi, [buffer]

    mov eax, esi  ; Copia el valor completo de esi a eax
    
    mov [pos_1], al    ; 0a = 10
    shr eax, 8
    
    mov [pos_2], al    ; 14 = 20
    shr eax, 8
    
    mov [pos_3], al    ; 1e = 30
    shr eax, 8

    mov [pos_4], al    ; 28 = 40

    xor esi, esi

    ; ----- Posicion (4,4) -----
    mov bl, [pos_4]
    mov al, bl
    shl eax, 24     ; Desplazamos 24 bits para la posición más significativa
    or esi, eax

    ; ----- Posicion (3,4) -----
    mov bl, [pos_4]
    mov ch, [pos_3]
    add bl, ch
    mov al, bl
    shl eax, 16
    or esi, eax
    
    ; ----- Posicion (2,4) -----
    mov bl, [pos_4]
    mov ch, [pos_3]
    add bl, ch
    xor eax, eax
    mov al, bl
    shl eax, 8
    or esi, eax

    ; ----- Posicion (1,4) -----
    mov bl, [pos_3]
    xor eax, eax
    mov al, bl  
    or esi, eax

    mov [buffer], esi

    ; Escribe
    mov eax, 4
    mov ebx, [fd_out]
    mov ecx, buffer
    mov edx, 4
    int 0x80

test:

    dec edi
    jnz loop

    ; Cierra archivo
    mov eax, 6
    mov ebx, [fd_in]
    int 0x80

    ; Cierra archivo
    mov eax, 6
    mov ebx, [fd_out]
    int 0x80

    ; Exit
    mov eax, 1
    xor ebx, ebx
    int 0x80
