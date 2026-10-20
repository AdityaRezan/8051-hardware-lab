#include "board.h"

void main(void)
{
    board_init();

    while (1)
    {
        led_write(0xFF);
        delay_ms(500);
        led_write(0x00);
        delay_ms(500);
    }
}
