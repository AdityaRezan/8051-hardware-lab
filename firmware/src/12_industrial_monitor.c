#include "board.h"

volatile unsigned char flag_1s;
volatile unsigned char heart;
volatile unsigned char emergency;

void timer0_isr(void) interrupt 1
{
    TH0 = TH0_5MS;
    TL0 = TL0_5MS;
    seg_tick();
    ms_ticks++;
    if (ms_ticks >= 200)
    {
        ms_ticks = 0;
        flag_1s = 1;
    }
}

void int0_isr(void) interrupt 0
{
    flag_int0 = 1;
}

void int1_isr(void) interrupt 2
{
    flag_int1 = 1;
}

void main(void)
{
    unsigned char raw;
    unsigned char leds;
    unsigned char zone;
    unsigned char relay_on;
    unsigned char buzzer_on;
    unsigned int t10;

    board_init();
    display_init();
    lcd_init();
    uart_init();

    IT0 = 1;
    IT1 = 1;
    EX0 = 1;
    EX1 = 1;
    EA = 1;

    zone = 0;
    relay_on = 0;
    buzzer_on = 0;
    flag_1s = 0;
    heart = 0;
    emergency = 0;
    flag_int0 = 0;
    flag_int1 = 0;

    lcd_gotoxy(0, 0);
    lcd_string("8051 ZONE MONITOR");
    lcd_gotoxy(0, 1);
    lcd_string("STARTING...");
    uart_string("8051 ZONE MONITOR 9600 8N1");
    uart_crlf();
    delay_ms(800);

    while (1)
    {
        raw = adc_read();
        t10 = (unsigned int)raw * 250 / 32;

        if (flag_int0)
        {
            flag_int0 = 0;
            emergency = 1;
        }
        if (flag_int1)
        {
            flag_int1 = 0;
            emergency = 0;
        }

        if (t10 < 400)
            zone = 0;
        else if (t10 < 700)
            zone = 1;
        else
            zone = 2;

        if (emergency == 0)
        {
            relay_on = (t10 >= 400) ? 1 : 0;
            buzzer_on = (zone == 2) ? 1 : 0;
        }
        else
        {
            relay_on = 0;
            buzzer_on = 1;
        }

        RELAY = relay_on;
        BUZZER = buzzer_on;

        leds = 0x00;
        if (emergency == 0)
        {
            if (zone == 0)
                leds = leds | LED_SAFE;
            else if (zone == 1)
                leds = leds | LED_WARN;
            else
                leds = leds | LED_ALARM;
        }
        else
        {
            leds = leds | LED_ALARM;
        }
        if (relay_on)
            leds = leds | LED_RELAY;
        if (buzzer_on)
            leds = leds | LED_BUZZER;
        if (heart)
            leds = leds | LED_HEART;
        led_write(leds);

        seg_number((unsigned char)(t10 / 10));

        lcd_gotoxy(0, 0);
        lcd_string("T=");
        lcd_number(t10 / 10);
        lcd_data('.');
        lcd_number(t10 % 10);
        lcd_string("C A=");
        lcd_number(raw);
        lcd_string("   ");

        lcd_gotoxy(0, 1);
        if (emergency)
            lcd_string("EMERGENCY STOP  ");
        else if (zone == 0)
            lcd_string("SAFE    FAN:OFF ");
        else if (zone == 1)
            lcd_string("WARNING FAN:ON  ");
        else
            lcd_string("DANGER  FAN:ON  ");

        if (flag_1s)
        {
            flag_1s = 0;
            if (heart == 0)
                heart = 1;
            else
                heart = 0;

            uart_string("T=");
            uart_number(t10 / 10);
            uart_string(".");
            uart_number(t10 % 10);
            uart_string("C ADC=");
            uart_number(raw);
            uart_string(" ZONE=");
            if (emergency)
                uart_string("EMERGENCY");
            else if (zone == 0)
                uart_string("SAFE");
            else if (zone == 1)
                uart_string("WARNING");
            else
                uart_string("DANGER");
            uart_string(" FAN=");
            uart_number(relay_on);
            uart_string(" BUZ=");
            uart_number(buzzer_on);
            uart_crlf();
        }

        delay_ms(200);
    }
}
