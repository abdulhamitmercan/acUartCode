#ifndef RS485_H_
#define RS485_H_

#include "HAL_UART.h"
#include "msp430.h"


#define RS485_EN BIT0   // P4.0 RS485 transceiver enable pin

static inline void RS485_EnableTransmit() {
    P4OUT |= RS485_EN; // RS485 veri g�nderim modunu etkinle�tir
}

static inline void RS485_DisableTransmit() {
    P4OUT &= ~RS485_EN; // RS485 veri g�nderim modunu devre d��� b�rak
}


static inline void RS485_Init(){
    // UART ve RS485 pinlerini ayarla
    P4DIR |= RS485_EN;
    RS485_DisableTransmit();

    HAL_UART_INIT();

}



#endif /* RS485_H_ */
