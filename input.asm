main:andi a3, zero, 0xf
    lh a0, 0(a3)
    lh a1,2(a3)
    beq a0, a1, main
    sh a4, 0b110(x15)
    sub a0,s1,s2
    or t0,a1 ,s2
fim:
    srl a7, x6, x7
teste: