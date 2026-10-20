#include "board.h"

void timer0_isr(void) interrupt 1
{
    TH0 = TH0_5MS;
    TL0 = TL0_5MS;
    seg_tick();
}

void main(void)
{
    unsigned char i;
    unsigned char p;
    unsigned char raw;
    unsigned char fail;
    unsigned int t;

    board_init();
    display_init();
    uart_init();
    fail = 0;

    uart_string("8051 HARDWARE LAB");
    uart_crlf();
    uart_string("POWER ON SELF TEST");
    uart_crlf();
    uart_crlf();

    uart_string("LED BANK      : ");
    p = 0x01;
    for (i = 0; i < 8; i++)
    {
        led_write(p);
        delay_ms(80);
        p = rol8(p);
    }
    led_write(0xFF);
    delay_ms(200);
    led_write(0x00);
    uart_string("OK");
    uart_crlf();

    uart_string("7 SEGMENT     : ");
    for (i = 0; i <= 99; i++)
    {
        seg_number(i);
        delay_ms(20);
    }
    seg_number(0);
    uart_string("OK");
    uart_crlf();

    uart_string("RELAY DRIVER  : ");
    for (i = 0; i < 3; i++)
    {
        RELAY = 1;
        delay_ms(150);
        RELAY = 0;
        delay_ms(150);
    }
    uart_string("OK");
    uart_crlf();

    uart_string("BUZZER        : ");
    for (i = 0; i < 3; i++)
    {
        BUZZER = 1;
        delay_ms(120);
        BUZZER = 0;
        delay_ms(120);
    }
    uart_string("OK");
    uart_crlf();

    uart_string("LCD 16X2      : ");
    lcd_init();
    lcd_gotoxy(0, 0);
    lcd_string("8051 HARDWARE");
    lcd_gotoxy(0, 1);
    lcd_string("LAB - SELF TEST");
    uart_string("OK");
    uart_crlf();

    uart_string("ADC0804 + LM35: ");
    adc_read();
    delay_ms(20);
    raw = adc_read();
    if (raw == 0x00 || raw == 0xFF)
        fail = 1;
    t = adc_to_celsius(raw);
    uart_string("RAW=");
    uart_hex(raw);
    uart_string(" T=");
    uart_number(t);
    uart_string("C");
    uart_crlf();

    uart_crlf();
    if (fail)
        uart_string("SELF TEST: FAIL - CHECK LM35 AND ADC0804 WIRING");
    else
        uart_string("SELF TEST: PASS");
    uart_crlf();

    while (1)
    {
        if (fail)
            led_write(0xAA);
        else
            led_write(0x55);
        delay_ms(300);
        if (fail)
            led_write(0x55);
        else
            led_write(0xAA);
        delay_ms(300);
    }
}
