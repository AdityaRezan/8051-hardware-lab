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
    unsigned char bars;
    unsigned char i;
    unsigned int t10;

    board_init();
    display_init();
    lcd_init();

    lcd_gotoxy(0, 0);
    lcd_string("LM35 + ADC0804");
    delay_ms(600);

    while (1)
    {
        raw = adc_read();
        t10 = (unsigned int)raw * 250 / 32;

        lcd_gotoxy(0, 0);
        lcd_string("T=");
        lcd_number(t10 / 10);
        lcd_data('.');
        lcd_number(t10 % 10);
        lcd_string("C A=");
        lcd_number(raw);
        lcd_string("  ");

        bars = raw / 16;
        lcd_gotoxy(0, 1);
        for (i = 0; i < 16; i++)
        {
            if (i < bars)
                lcd_data('#');
            else
                lcd_data('-');
        }

        seg_number((unsigned char)(t10 / 10));
        delay_ms(250);
    }
}
