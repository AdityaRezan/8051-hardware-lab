#include "board.h"

void timer0_isr(void) interrupt 1
{
    TH0 = TH0_5MS;
    TL0 = TL0_5MS;
    seg_tick();
    ms_ticks++;
}

void main(void)
{
    unsigned char v;

    board_init();
    display_init();
    v = 0;

    while (1)
    {
        seg_number(v);
        delay_ms(500);
        v++;
        if (v > 99)
            v = 0;
    }
}
