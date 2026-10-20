#include "board.h"

volatile unsigned char blink_state;

void timer0_isr(void) interrupt 1
{
    TH0 = 0x4C;
    TL0 = 0x00;
    ms_ticks++;
    if (ms_ticks >= 20)
    {
        ms_ticks = 0;
        if (blink_state == 0)
            blink_state = 1;
        else
            blink_state = 0;
    }
}

void main(void)
{
    board_init();
    blink_state = 0;
    ms_ticks = 0;
    TMOD = (TMOD & 0xF0) | 0x01;
    TH0 = 0x4C;
    TL0 = 0x00;
    ET0 = 1;
    EA = 1;
    TR0 = 1;

    while (1)
    {
        if (blink_state == 0)
            led_write(0x00);
        else
            led_write(0xFF);
    }
}
