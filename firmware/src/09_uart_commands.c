#include "board.h"

char line[24];
unsigned char len;

void to_upper(void)
{
    unsigned char i;
    for (i = 0; i < len; i++)
    {
        if (line[i] >= 'a' && line[i] <= 'z')
            line[i] = line[i] - 32;
    }
}

unsigned char hex_nibble(unsigned char c)
{
    if (c >= '0' && c <= '9')
        return c - '0';
    if (c >= 'A' && c <= 'F')
        return c - 'A' + 10;
    return 0;
}

unsigned char hex_byte(unsigned char h, unsigned char l)
{
    return (unsigned char)((hex_nibble(h) << 4) | hex_nibble(l));
}

unsigned int parse_dec(unsigned char idx)
{
    unsigned int v;
    unsigned char i;
    v = 0;
    for (i = idx; i < len; i++)
    {
        if (line[i] >= '0' && line[i] <= '9')
            v = v * 10 + (unsigned int)(line[i] - '0');
    }
    return v;
}

void timer0_isr(void) interrupt 1
{
    TH0 = TH0_5MS;
    TL0 = TL0_5MS;
    seg_tick();
}

void execute(void)
{
    unsigned char v;
    unsigned int n;

    to_upper();
    line[len] = 0;

    if (strncmp(line, "HLP", 3) == 0)
    {
        uart_string("LED HH   SET LED BANK, HEX");
        uart_crlf();
        uart_string("SEG NN   SHOW 0-99 ON DISPLAY");
        uart_crlf();
        uart_string("RLY N    RELAY 1=ON 0=OFF");
        uart_crlf();
        uart_string("BUZ N    BUZZER 1=ON 0=OFF");
        uart_crlf();
        uart_string("TMP      READ LM35 AND ADC0804");
        uart_crlf();
    }
    else if (strncmp(line, "LED", 3) == 0 && len >= 6)
    {
        v = hex_byte(line[4], line[5]);
        led_write(v);
        uart_string("LED=");
        uart_hex(v);
        uart_crlf();
    }
    else if (strncmp(line, "SEG", 3) == 0 && len >= 4)
    {
        n = parse_dec(4);
        if (n > 99)
            n = 99;
        seg_number((unsigned char)n);
        uart_string("SEG=");
        uart_number(n);
        uart_crlf();
    }
    else if (strncmp(line, "RLY", 3) == 0 && len >= 5)
    {
        n = parse_dec(4);
        RELAY = (n == 0) ? 0 : 1;
        uart_string("RELAY=");
        uart_number(n == 0 ? 0 : 1);
        uart_crlf();
    }
    else if (strncmp(line, "BUZ", 3) == 0 && len >= 5)
    {
        n = parse_dec(4);
        BUZZER = (n == 0) ? 0 : 1;
        uart_string("BUZZER=");
        uart_number(n == 0 ? 0 : 1);
        uart_crlf();
    }
    else if (strncmp(line, "TMP", 3) == 0)
    {
        v = adc_read();
        uart_string("RAW=");
        uart_hex(v);
        uart_string(" T=");
        uart_number(adc_to_celsius(v));
        uart_string("C");
        uart_crlf();
    }
    else
    {
        uart_string("ERR");
        uart_crlf();
    }
}

void main(void)
{
    unsigned char c;

    board_init();
    uart_init();
    display_init();
    len = 0;

    uart_string("8051 HARDWARE LAB COMMAND SHELL");
    uart_crlf();
    uart_string("TYPE HLP FOR THE COMMAND LIST");
    uart_crlf();
    uart_string("> ");

    while (1)
    {
        if (uart_rx_ready())
        {
            c = uart_rx();
            if (c == '\r' || c == '\n')
            {
                uart_crlf();
                execute();
                len = 0;
                uart_string("> ");
            }
            else if (len < 22)
            {
                line[len] = c;
                len++;
                uart_tx(c);
            }
        }
    }
}
