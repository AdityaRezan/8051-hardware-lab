#include "board.h"

void main(void)
{
    unsigned char s;
    unsigned char flash;

    board_init();
    flash = 0;

    while (1)
    {
        s = switch_read();
        if (s >= 0x80)
        {
            if (flash == 0)
            {
                flash = 1;
                led_write(0xFF);
            }
            else
            {
                flash = 0;
                led_write(0x00);
            }
            delay_ms(100);
        }
        else
        {
            led_write(s);
        }
    }
}
