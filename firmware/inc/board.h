#ifndef _BOARD_H_
#define _BOARD_H_

#ifdef CHIP_AT89C51
#include <REG51.H>
#else
#include <REGX52.H>
#endif

#include <STRING.H>

#ifdef __C51__
#include <INTRINS.H>
#define NOP() _nop_()
#else
#define NOP() __asm nop __endasm
#endif

#define XTAL_HZ      11059200UL
#define BUS          P0
#define SWITCH       P1

#define LED_SAFE     0x01
#define LED_WARN     0x02
#define LED_ALARM    0x04
#define LED_RELAY    0x08
#define LED_BUZZER   0x10
#define LED_HEART    0x20

#define SEG_DOT      0x80

#define TH0_5MS      0xEE
#define TL0_5MS      0x00
#define TH1_9600     0xFD

sbit LED_LE    = P2^0;
sbit SEG_LE    = P2^1;
sbit LCD_E     = P2^2;
sbit LCD_RS    = P2^3;
sbit LCD_RW    = P2^4;
sbit ADC_WR    = P2^5;
sbit ADC_RD    = P2^6;
sbit ADC_INTR  = P2^7;

sbit RELAY     = P3^4;
sbit SQW       = P3^4;
sbit BUZZER    = P3^5;
sbit DIG1      = P3^6;
sbit DIG2      = P3^7;

sbit PB_EMERG  = P3^2;
sbit PB_MODE   = P3^3;

volatile unsigned char bus_shadow;
volatile unsigned char seg_digit[2];
volatile unsigned char seg_pos;
volatile unsigned int  ms_ticks;
volatile unsigned char flag_int0;
volatile unsigned char flag_int1;

unsigned char code SEG7[10] = { 0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F };
unsigned char code MSG_SPACE[17] = "                ";

void delay_1ms(void)
{
    unsigned char i;
    i = 250;
    do { } while (--i);
    i = 250;
    do { } while (--i);
}

void delay_ms(unsigned int ms)
{
    while (ms--)
        delay_1ms();
}

void delay_short(void)
{
    NOP();
    NOP();
    NOP();
    NOP();
    NOP();
    NOP();
    NOP();
    NOP();
}

void bus_put(unsigned char v)
{
    bus_shadow = v;
    BUS = v;
}

void board_init(void)
{
    bus_shadow = 0x00;
    seg_digit[0] = 0x00;
    seg_digit[1] = 0x00;
    seg_pos = 0;
    ms_ticks = 0;
    flag_int0 = 0;
    flag_int1 = 0;
    BUS = 0x00;
    LED_LE = 0;
    SEG_LE = 0;
    LCD_E = 0;
    LCD_RS = 0;
    LCD_RW = 0;
    ADC_WR = 1;
    ADC_RD = 1;
    RELAY = 0;
    BUZZER = 0;
    DIG1 = 0;
    DIG2 = 0;
}

void led_write(unsigned char v)
{
    unsigned char ea_state;
    ea_state = EA;
    EA = 0;
    bus_put(v);
    LED_LE = 1;
    delay_short();
    LED_LE = 0;
    EA = ea_state;
}

void seg_latch(unsigned char v)
{
    unsigned char ea_state;
    ea_state = EA;
    EA = 0;
    bus_put(v);
    SEG_LE = 1;
    delay_short();
    SEG_LE = 0;
    EA = ea_state;
}

void seg_direct(unsigned char pattern)
{
    seg_latch(pattern);
    DIG2 = 0;
    DIG1 = 1;
}

void seg_number(unsigned char v)
{
    if (v > 99)
        v = 99;
    seg_digit[0] = SEG7[v / 10];
    seg_digit[1] = SEG7[v % 10];
}

void seg_hex(unsigned char v)
{
    unsigned char hi;
    unsigned char lo;
    hi = (v >> 4) & 0x0F;
    lo = v & 0x0F;
    seg_digit[0] = SEG7[hi];
    seg_digit[1] = SEG7[lo];
}

void seg_tick(void)
{
    unsigned char s;
    s = bus_shadow;
    DIG1 = 0;
    DIG2 = 0;
    if (seg_pos == 0)
    {
        BUS = seg_digit[0];
        SEG_LE = 1;
        delay_short();
        SEG_LE = 0;
        DIG1 = 1;
        seg_pos = 1;
    }
    else
    {
        BUS = seg_digit[1];
        SEG_LE = 1;
        delay_short();
        SEG_LE = 0;
        DIG2 = 1;
        seg_pos = 0;
    }
    bus_put(s);
}

void display_init(void)
{
    TMOD = (TMOD & 0xF0) | 0x01;
    TH0 = TH0_5MS;
    TL0 = TL0_5MS;
    ET0 = 1;
    EA = 1;
    TR0 = 1;
}

void lcd_write(unsigned char rs, unsigned char v)
{
    unsigned char ea_state;
    ea_state = EA;
    EA = 0;
    bus_put(v);
    LCD_RS = rs;
    LCD_RW = 0;
    delay_short();
    LCD_E = 1;
    delay_short();
    LCD_E = 0;
    delay_short();
    EA = ea_state;
}

void lcd_cmd(unsigned char c)
{
    lcd_write(0, c);
    delay_ms(2);
}

void lcd_data(unsigned char d)
{
    lcd_write(1, d);
    delay_short();
}

void lcd_init(void)
{
    delay_ms(30);
    lcd_cmd(0x38);
    lcd_cmd(0x38);
    lcd_cmd(0x0C);
    lcd_cmd(0x06);
    lcd_cmd(0x01);
    delay_ms(5);
}

void lcd_gotoxy(unsigned char col, unsigned char row)
{
    if (row == 0)
        lcd_cmd(0x80 + col);
    else
        lcd_cmd(0xC0 + col);
}

void lcd_string(char *s)
{
    while (*s)
    {
        lcd_data(*s);
        s++;
    }
}

void lcd_clear_line(unsigned char row)
{
    lcd_gotoxy(0, row);
    lcd_string(MSG_SPACE);
    lcd_gotoxy(0, row);
}

void lcd_number(unsigned int v)
{
    unsigned char d;
    unsigned char started;
    unsigned int div;
    started = 0;
    for (div = 10000; div > 0; div = div / 10)
    {
        d = (unsigned char)(v / div);
        if (d != 0 || started != 0 || div == 1)
        {
            lcd_data('0' + d);
            started = 1;
        }
        v = v - (unsigned int)d * div;
    }
}

unsigned char adc_read(void)
{
    unsigned char v;
    unsigned char ea_state;
    unsigned int guard;
    ea_state = EA;
    EA = 0;
    ADC_RD = 1;
    ADC_WR = 1;
    delay_short();
    ADC_WR = 0;
    delay_short();
    ADC_WR = 1;
    guard = 0;
    while (ADC_INTR == 0)
    {
        guard++;
        if (guard > 60000)
            break;
    }
    guard = 0;
    while (ADC_INTR == 1)
    {
        guard++;
        if (guard > 60000)
            break;
    }
    BUS = 0xFF;
    ADC_RD = 0;
    delay_short();
    v = BUS;
    ADC_RD = 1;
    bus_put(bus_shadow);
    EA = ea_state;
    return v;
}

unsigned int adc_to_celsius(unsigned char raw)
{
    return (unsigned int)raw * 25 / 32;
}

void uart_init(void)
{
    TMOD = (TMOD & 0x0F) | 0x20;
    PCON = PCON & 0x7F;
    TH1 = TH1_9600;
    TL1 = TH1_9600;
    SCON = 0x50;
    TR1 = 1;
    TI = 1;
}

void uart_tx(unsigned char c)
{
    while (TI == 0);
    TI = 0;
    SBUF = c;
}

void uart_string(char *s)
{
    while (*s)
    {
        uart_tx(*s);
        s++;
    }
}

void uart_crlf(void)
{
    uart_tx('\r');
    uart_tx('\n');
}

void uart_hex(unsigned char v)
{
    unsigned char n;
    n = (v >> 4) & 0x0F;
    uart_tx(n < 10 ? '0' + n : 'A' + n - 10);
    n = v & 0x0F;
    uart_tx(n < 10 ? '0' + n : 'A' + n - 10);
}

void uart_number(unsigned int v)
{
    unsigned char d;
    unsigned char started;
    unsigned int div;
    started = 0;
    for (div = 10000; div > 0; div = div / 10)
    {
        d = (unsigned char)(v / div);
        if (d != 0 || started != 0 || div == 1)
        {
            uart_tx('0' + d);
            started = 1;
        }
        v = v - (unsigned int)d * div;
    }
}

unsigned char uart_rx_ready(void)
{
    return RI;
}

unsigned char uart_rx(void)
{
    while (RI == 0);
    RI = 0;
    return SBUF;
}

unsigned char switch_read(void)
{
    unsigned char a;
    unsigned char b;
    a = SWITCH;
    do
    {
        delay_ms(5);
        b = SWITCH;
    } while (b != a);
    return b;
}

unsigned char rol8(unsigned char v)
{
    return (unsigned char)((v << 1) | ((v >> 7) & 0x01));
}

unsigned char ror8(unsigned char v)
{
    return (unsigned char)((v >> 1) | ((v << 7) & 0x80));
}

#endif
