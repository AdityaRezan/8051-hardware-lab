#include "board.h"

void timer0_isr(void) interrupt 1
{
    TH0 = 0xFE;
    TL0 = 0x34;
    if (SQW == 0)
        SQW = 1;
    else
        SQW = 0;
}

void main(void)
{
    board_init();
    SQW = 0;
    TMOD = (TMOD & 0xF0) | 0x01;
    TH0 = 0xFE;
    TL0 = 0x34;
    ET0 = 1;
    EA = 1;
    TR0 = 1;

    while (1)
    {
    }
}
