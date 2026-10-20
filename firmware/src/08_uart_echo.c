#include "board.h"

void main(void)
{
    unsigned char c;

    board_init();
    uart_init();
    uart_string("8051 HARDWARE LAB");
    uart_crlf();
    uart_string("9600 8N1 - TYPE TO ECHO");
    uart_crlf();

    while (1)
    {
        if (uart_rx_ready())
        {
            c = uart_rx();
            uart_tx(c);
            if (c == '\r')
                uart_crlf();
            led_write(c);
        }
    }
}
