#include "board.h"

void timer0_isr(void) interrupt 1
{
    TH0 = TH0_5MS;
    TL0 = TL0_5MS;
    seg_tick();
}

void main(void)
{
    unsigned char raw;
    unsigned int t;

    board_init();
    display_init();

    while (1)
    {
        raw = adc_read();
        t = adc_to_celsius(raw);
        if (t > 99)
            t = 99;
        seg_number((unsigned char)t);
        delay_ms(250);
    }
}
