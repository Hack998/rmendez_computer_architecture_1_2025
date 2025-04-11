section .data
    filename db "cuadrante.img", 0  ; Path del archivo
    fileout db "r.img", 0
    fd_in dd 0                        
    fd_out dd 0                        
    temp_r db 0
    temp_l db 0
    pos_1 db 0
    pos_2 db 0
    pos_3 db 0
    pos_4 db 0
    buffer db 0                    ; Buffer

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

    mov edi, 9801         ; Iteraciones

loop:

    ; Leer primera linea
    mov eax, 3         
    mov ebx, [fd_in]       
    mov ecx, buffer   
    mov edx, 4        
    int 0x80

    mov esi, [buffer]

    mov eax, esi
    
    mov [pos_1], al    ; 0a = 10
    shr eax, 8
    
    mov [pos_2], al    ; 14 = 20
    shr eax, 8
    
    mov [pos_3], al    ; 1e = 30
    shr eax, 8

    mov [pos_4], al    ; 28 = 40

    xor esi, esi
    ;_______________________Fila 1___________________________
    ; ----- Posicion (4,1) -----
    mov bl, [pos_2]
    mov al, bl
    shl eax, 24     
    or esi, eax

    ; ----- Posicion (3,1) -----
    mov ebx, [pos_2]
    movzx ebx, bl
    mov eax, [pos_1]
    movzx eax, al
    add eax, ebx
    add eax, ebx
test:
    mov edx, 0      
    mov ecx, 3    
    div ecx
    shl eax, 16
    or esi, eax
    
    ; ----- Posicion (2,1) -----
    mov eax, [pos_2]
    movzx eax, al
    mov ebx, [pos_1]
    movzx ebx, bl
    add eax, ebx
    add eax, ebx
    mov edx, 0      
    mov ecx, 3    
    div ecx
    shl eax, 8
    or esi, eax

    ; ----- Posicion (1,1) -----
    mov bl, [pos_1]
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
    
    xor esi, esi
    ;_______________________Fila 2___________________________
    ; ----- Posicion (4,2) -----
    mov ebx, [pos_2]
    movzx ebx, bl
    mov eax, [pos_4]
    movzx eax, al
    add eax, ebx
    add eax, ebx
    mov edx, 0      
    mov ecx, 3    
    div ecx
    mov [temp_r], al
    shl eax, 24
    or esi, eax

    ; ----- Posicion (1,2) -----
    mov eax, [pos_3]
    movzx eax, al
    mov ebx, [pos_1]
    movzx ebx, bl
    add eax, ebx
    add eax, ebx
    mov edx, 0      
    mov ecx, 3    
    div ecx
    mov [temp_l], al
    or esi, eax

    ; ----- Posicion (3,2) -----
    mov ebx, [temp_r]
    movzx ebx, bl
    mov eax, [temp_l]
    movzx eax, al
    add eax, ebx
    add eax, ebx
    mov edx, 0      
    mov ecx, 3    
    div ecx
    shl eax, 16
    or esi, eax

    ; ----- Posicion (2,2) -----
    mov eax, [temp_r]
    movzx eax, al
    mov ebx, [temp_l]
    movzx ebx, bl
    add eax, ebx
    add eax, ebx
    mov edx, 0      
    mov ecx, 3    
    div ecx
    shl eax, 8
    or esi, eax

    mov [buffer], esi

    ; Escribe
    mov eax, 4
    mov ebx, [fd_out]
    mov ecx, buffer
    mov edx, 4
    int 0x80

    xor esi, esi
    ;_______________________Fila 3___________________________
    ; ----- Posicion (4,3) -----
    mov ebx, [pos_4]
    movzx ebx, bl
    mov eax, [pos_2]
    movzx eax, al
    add eax, ebx
    add eax, ebx
    mov edx, 0      
    mov ecx, 3    
    div ecx
    mov [temp_r], al
    shl eax, 24
    or esi, eax

    ; ----- Posicion (1,3) -----
    mov eax, [pos_1]
    movzx eax, al
    mov ebx, [pos_3]
    movzx ebx, bl
    add eax, ebx
    add eax, ebx
    mov edx, 0      
    mov ecx, 3    
    div ecx
    mov [temp_l], al
    or esi, eax

    ; ----- Posicion (3,3) -----
    mov ebx, [temp_r]
    movzx ebx, bl
    mov eax, [temp_l]
    movzx eax, al
    add eax, ebx
    add eax, ebx
    mov edx, 0      
    mov ecx, 3    
    div ecx
    shl eax, 16
    or esi, eax

    ; ----- Posicion (2,3) -----
    mov eax, [temp_r]
    movzx eax, al
    mov ebx, [temp_l]
    movzx ebx, bl
    add eax, ebx
    add eax, ebx
    mov edx, 0      
    mov ecx, 3    
    div ecx
    shl eax, 8
    or esi, eax

    mov [buffer], esi

    ; Escribe
    mov eax, 4
    mov ebx, [fd_out]
    mov ecx, buffer
    mov edx, 4
    int 0x80

    xor esi, esi
    ;_______________________Fila 4___________________________
    ; ----- Posicion (4,4) -----
    mov bl, [pos_4]
    mov al, bl
    shl eax, 24     
    or esi, eax

    ; ----- Posicion (3,4) -----
    mov ebx, [pos_4]
    movzx ebx, bl
    mov eax, [pos_3]
    movzx eax, al
    add eax, ebx
    add eax, ebx
    mov edx, 0      
    mov ecx, 3    
    div ecx
    shl eax, 16
    or esi, eax
    
    ; ----- Posicion (2,4) -----
    mov eax, [pos_4]
    movzx eax, al
    mov ebx, [pos_3]
    movzx ebx, bl
    add eax, ebx
    add eax, ebx
    mov edx, 0      
    mov ecx, 3    
    div ecx
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
