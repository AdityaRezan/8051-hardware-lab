#include "board.h"

volatile unsigned char counter;
volatile unsigned char led_state;

void timer0_isr(void) interrupt 1
{
    TH0 = TH0_5MS;
    TL0 = TL0_5MS;
    seg_tick();
}

void int0_isr(void) interrupt 0
{
    if (led_state == 0)
        led_state = 1;
    else
        led_state = 0;
}

void int1_isr(void) interrupt 2
{
    counter++;
    if (counter > 99)
        counter = 0;
}

void main(void)
{
    board_init();
    counter = 0;
    led_state = 0;
    display_init();
    IT0 = 1;
    IT1 = 1;
    EX0 = 1;
    EX1 = 1;
    EA = 1;

    while (1)
    {
        seg_number(counter);
        if (led_state == 0)
            led_write(0x0F);
        else
            led_write(0xF0);
    }
}
