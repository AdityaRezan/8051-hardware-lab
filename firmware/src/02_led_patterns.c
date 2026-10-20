#include "board.h"

void main(void)
{
    unsigned char p;
    unsigned char i;

    board_init();

    while (1)
    {
        p = 0x01;
        for (i = 0; i < 8; i++)
        {
            led_write(p);
            delay_ms(120);
            p = rol8(p);
        }
        p = 0x80;
        for (i = 0; i < 8; i++)
        {
            led_write(p);
            delay_ms(120);
            p = ror8(p);
        }
        led_write(0xAA);
        delay_ms(300);
        led_write(0x55);
        delay_ms(300);
        led_write(0xFF);
        delay_ms(150);
        led_write(0x00);
        delay_ms(150);
    }
}
