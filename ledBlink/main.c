#include <msp430.h>
#include "stdint.h"
#include <HAL.h>
#include <dspLib.h>
#include "measurements.h"
#include "DISPLAY.h"
#include "simulationAC.h"
#include "lm75.h"
#include "TB67H451FNG.h"
#include "rgbLed.h"
#include "buzzer.h"

#include "communication/uart_api.h"
#include "communication/uartProtocol.h"

#include "control/proximityPilot.h"
#include "control/chargeTime.h"
#include "control/chargerCtrl.h"
#include "control/charger.h"
#include "control/controlPilot.h"

#include <acmeter/HAL_UART.h>
#include "acmeter/rs485.h"
#include "acmeter/PetitModbus.h"
#include "acmeter/acmeter.h"
#include "acmeter/timeX.h"
#include "meter.h"



//#define SIMULATION_ENERGY_MEASUREMENT
//#define SIMULATION_CONTROL_PILOT
//#define SIMULATION_RELAY
//#define USE_AC_METER


#define Q_1_OVER_36                                    _IQ(0.0002778) // (1/3600)*100
unsigned int ADC_Result[64] = {0};                      // ADC conversion result array
unsigned long ChResults[7];

//const int i = 0;
unsigned int windex = 0;
unsigned int xintCount = 0;


int start = 0;
int Vsimcp = 12.0;
float vcpFirst = 0.0;
_iq Vcpmid = _IQ(1.1475);
_iq Vcpconst = _IQ(10.45);
uint16_t actuatorMotor = 0;

uint16_t run = 0;


int chargeCompleteFlag = 0;
int endTransaction = 0;
int buzzerVal = 0;
int rly1 = 1;
#define VCP_MID         _IQ(1.1475)
#define VCP_CONSTANT    _IQ(10.45)

enum{
    ERR_MAX_LINE1_VOLTAGE,
    ERR_MIN_LINE1_VOLTAGE,
    ERR_MAX_LINE1_CURRENT,
    reserved3,

    ERR_MAX_LINE2_VOLTAGE,
    ERR_MIN_LINE2_VOLTAGE,
    ERR_MAX_LINE2_CURRENT,
    reserved7,

    ERR_MAX_LINE3_VOLTAGE,
    ERR_MIN_LINE3_VOLTAGE,
    ERR_MAX_LINE3_CURRENT,
    reserved11,

    ERR_LEAKAGE_CURRENT,
};


float meterStart = 0.0;
float meterStop = 0.0;
t_zcParams zc;
_iq deltaT = _IQ(0.005);

typedef struct {
    unsigned int errorState;
    unsigned long errorCount;
    _iq maxLine_V;
    _iq minLine_V;
    _iq maxLine_C;
} t_limits;

t_limits limits;


t_rmsParams qVrms[3], qIrms[3];


void calculateEnergyUsage() {
#ifdef USE_AC_METER
    energyMeter_calculateEnergy(&meter.energy, meterStop, meterStart);
#else
    measurements_calculateEnergy(&meter.energy, meter.power, Q_1_OVER_36);
#endif
}


t_relays rly;
#define FLAG16(a) (1L<<a)

unsigned int startTimeout = 0;
uint32_t dataBuf[10] = {0};




void initAcEvseLimits(t_limits* in)
{
    in->maxLine_V = _IQ(3.7334); // +220%20
    in->minLine_V = _IQ(-3.7334); // -220%20
    in->maxLine_C = _IQ(5.67);
}

unsigned int checkLimits()
{
    unsigned int err=0;
    err |= (qemeter.VL[0] > limits.maxLine_V ? FLAG16(ERR_MAX_LINE1_VOLTAGE) :0);
    err |= (qemeter.VL[1] > limits.maxLine_V ? FLAG16(ERR_MAX_LINE2_VOLTAGE) :0);
    err |= (qemeter.VL[2] > limits.maxLine_V ? FLAG16(ERR_MAX_LINE3_VOLTAGE) :0);

    err |= (qemeter.VL[0] < limits.minLine_V ? FLAG16(ERR_MIN_LINE1_VOLTAGE) :0);
    err |= (qemeter.VL[1] < limits.minLine_V ? FLAG16(ERR_MIN_LINE2_VOLTAGE) :0);
    err |= (qemeter.VL[2] < limits.minLine_V ? FLAG16(ERR_MIN_LINE3_VOLTAGE) :0);

    err |= (qemeter.IL[0] > limits.maxLine_C ? FLAG16(ERR_MAX_LINE1_CURRENT) :0);
    err |= (qemeter.IL[1] > limits.maxLine_C ? FLAG16(ERR_MAX_LINE2_CURRENT) :0);
    err |= (qemeter.IL[2] > limits.maxLine_C ? FLAG16(ERR_MAX_LINE3_CURRENT) :0);

    err |= (xintCount > 0 ? FLAG16(ERR_LEAKAGE_CURRENT) :0);
    return(err);
}

void resetErrors()
{
    limits.errorState &= 0x0000;
    limits.errorCount &= 0x00000000;
}


void checkandHandleLimits(){
    unsigned int err=0;
/*
    err |= checkLimits();
    if(err == 0)
        limits.errorCount=0;
    else
        limits.errorCount++;


    if(limits.errorCount > 0){
        limits.errorState = err;
    }
*/
}


void handleCharging(void) {
    if (start == 1) {
        meterStop = acMeterData.energy;
    }
    if (vngEvse.stopReqEv) {
        if (start == 1) {
            start = 0;
        }
        chargeCompleteFlag = 1;
        vngEvse.stopReqEv = AC_EVSEChargeStopFromEV_NOT_STOP;
    }

    run = !vngEvse.stopReqEv && (vngEvse.chargeReq == 1) ? AC_EVSEChargeRequest_START_CHARGE : AC_EVSEChargeRequest_STOP_CHARGE;
}


static uint16_t actuatorDirection = 0;
void main(void)
{
    acevse.transition = 0;
    acevse.voltageLevel = 0;
    vngEvse.chargeReq = 0;

    initEVSE_Status(&vngEvse);

    dsp_resetMvnAvgParams(&cpLevel.avg);
    initAcEvseLimits(&limits);
    rgbLed_assign(&rgbledObj, 2, 0, 0);

    HAL_PORT_MAPPING();
    rgbLed_init();
    InitPetitModbus(1);


    HAL_SYS_INIT();
    __bis_SR_register(GIE); // Kesmeleri etkinleştir

    acMeterControl.control = 1;
    acMeterControl.index = 1;

    int i = 0;
    for(i = 0; i < 256; i++){
        getAdcResults(ADC_Result);
        mLib_getAdcVoltages(ADC_Result);
    }

    vcpFirst = emeter.Vcp;
    if(vcpFirst > 2.14 && vcpFirst < 2.35){
        Vcpmid = _IQmpy(_IQ(0.5), qemeter.Vcp);
        Vcpconst = _IQdiv(_IQ(24.0), qemeter.Vcp);
    }
    else{
        //error control pilot read
    }

    while(1){

        modbus_Process(&acMeterControl.rxReady);

        if(acMeterControl.rxReady == 1 && acMeterControl.timeout != 1 && startTimeout == 1){
            dataBuf[acMeterControl.index] = 0;
            modbus_getData(&dataBuf[acMeterControl.index]);
            acMeterControl.rxReady = 0;
            startTimeout = 0;
        }

        acMeterUpdateData(&acMeterData, dataBuf);

        if(acMeterControl.control == 1){
            acMeterControl.control = 0;
            RS485_EnableTransmit();
            acMeterControl.index = acMeterProcessTransmit();
            startTimeout = 1;
            uart3.txCounter = 0;
            UCA3IE |= UCTXIE;
            UCA3IFG |= UCTXIFG;
        }

          getAdcResults(ADC_Result);
          mLib_getAdcVoltages(ADC_Result);

          qemeter.Vcp = qemeter.Vcp - Vcpmid;
          qemeter.Vcp = _IQmpy(qemeter.Vcp, Vcpconst);

#ifdef SIMULATION_CONTROL_PILOT
          qemeter.Vcp = _IQ(Vsimcp);
#endif
          cp_VoltageLevel(qemeter.Vcp);
          cpLevel.out = _IQtoF(cpLevel.avg.qoutVal);

          pp_Handle(qemeter.Vpp);
          HAL_SET_PWMDUTY_PWM3(ppLevel.dutyRatio);

          runFSM(cpLevel.qout, pwmStatus);


          deltaT = _IQdiv(_IQ(1.0), _IQ(zc.numOfSample));



#ifdef USE_AC_METER
          meterF.E = _IQtoF(meter.energy);
          meterF.P = acMeterData.power;
#else
          meterF.E = _IQtoF(meter.energy);
          meterF.P = _IQtoF(meter.power);
#endif




          if(limits.errorCount > 0){
              vngEvse.chargeReq = 16;
          }


          handleCharging();


          if(FSM.current_state == C2){
              actuatorDirection = 0;
          }
          else if(FSM.current_state != C2 && rly.relayN_L1 == 0 && rly.relayL2_L3 == 0){
              actuatorDirection = 1;
          }

          vngEvse.connLocked = isSockedLocked(actuatorMotor);


          switch(run){
            case AC_EVSEChargeRequest_START_CHARGE: // start Charging
                if(FSM.current_state == B1){
                    PwmStartStop(1);
                }
                break;
            case AC_EVSEChargeRequest_STOP_CHARGE: // stop Charging
                PwmStartStop(0);
                break;
            default:
                PwmStartStop(0);
                break;
          }


          if(comm.rxCompletedFlg){
              uartUpdate(comm.recvBuff, comm.sendBuff, SEND_SIZE);
              comm.rxCompletedFlg = 0;
          }


          setState_Power((unsigned int)(meterF.P * 10));
          setState_Energy((int)(meterF.E * 100.0));
          setState_EVChargeTermination(chargeCompleteFlag);
          setState_ChargingStatus(vngEvse.charging);
          setState_ConnectorStatus(vngEvse.connector);
          setState_ErrStatus((int)(limits.errorState));
          setState_ChargingTimeMinSec((int)(time.minute << 8 | time.second));
          setState_ChargingTimeHours(time.hours);
          setState_DeviceId(99);

          getRunCtrl(vngEvse.chargeReq);
          getClearSession(endTransaction);
          getBuzzer(buzzerVal);
          //vngEvse.chargeReq = 1;


          if(endTransaction == 1){
              meter.energy = _IQ(0.0);
              time.hours = 0;
              time.minute = 0;
              time.second = 0;
              chargeCompleteFlag = 0;
          }

#ifdef SIMULATION_RELAY
        HAL_GPIO_WRITE_OUTRELAY1(rly1);
        HAL_GPIO_WRITE_L1RELAY(rly1);
        HAL_GPIO_WRITE_L3RELAY(rly1);
#else
        HAL_GPIO_WRITE_OUTRELAY1(rly.outRelay1);
        HAL_GPIO_WRITE_L1RELAY(rly.relayN_L1);
        HAL_GPIO_WRITE_L3RELAY(rly.relayL2_L3);
#endif
    }

}

// Timer1 A0 interrupt service routine
#pragma vector=TIMER1_A0_VECTOR
__interrupt void TIMER1_A0_ISR(void)
{

    //HAL_SET_GPIO_LEDRED();

    PetitModBus_TimerValues();

    is_1s_Occured(&acMeterControl.control, 1000);
    acMeterControl.timeout = timeoutProcess(startTimeout, 1000, 1);


    mLib_getSigmaDeltaDVoltages(ChResults);

    windex = (++windex % 50);

#ifdef SIMULATION_ENERGY_MEASUREMENT
        voltageBuffer[windex] = ((float *)(&emeter))[voltageSelect];
#else
        voltageBuffer[zc.freqCount] = ((float *)(&emeter))[voltageSelect];
#endif

#ifdef SIMULATION_ENERGY_MEASUREMENT
    qemeter.VL[0] = _IQ(V1sim[windex]);
    qemeter.VL[1] = _IQ(V1sim[windex]);
    qemeter.VL[2] = _IQ(V1sim[windex]);
    qemeter.IL[0] = _IQ(V1sim[windex]);
    qemeter.IL[1] = _IQ(V1sim[windex]);
    qemeter.IL[2] = _IQ(V1sim[windex]);
#endif
    qVrms[0].inVal = qemeter.VL[0];
    qVrms[1].inVal = qemeter.VL[1];
    qVrms[2].inVal = qemeter.VL[2];
    qIrms[0].inVal = qemeter.IL[0];
    qIrms[1].inVal = qemeter.IL[1];
    qIrms[2].inVal = qemeter.IL[2];
    meter.power = measurements_calculatePower(qVrms, qIrms, deltaT, windex);


    zc.zcPoint = dsp_ZeroCrossDetector(qemeter.VL[0]);
    if(zc.zcPoint == 1){
        zc.numOfSample = zc.freqCount;
        zc.freqCount &= 0x0000;
    }
    else{
        ++zc.freqCount;
    }

    updateBuzzer(buzzerVal, &buzzerRsp);

    checkCableStatus(&vngEvse, &FSM);
    //HAL_RESET_GPIO_LEDRED();
}


#pragma vector=TIMER2_A0_VECTOR
__interrupt void TIMER2_A0_ISR(void)
{
    readLM75();
    rgbLed_assign(&rgbledObj, run, vngEvse.connector, vngEvse.charging);
    rgbLed_drive(&rgbledObj, &rgbledObjOld);

    checkandHandleLimits();

    if (vngEvse.charging) {
        if (start == 0 && acMeterData.energy != 0) {
            meterStart = acMeterData.energy;
            start = 1;
        }

        calculateEnergyUsage();
        updateTime(&time);
    }

    actuatorMotor = readMotorInput();
    updateMotorInput(actuatorDirection);
    rly.relayN_L1 = rly.relayL2_L3 = relayCtrl(vngEvse.charging, vngEvse.connLocked, 0);
}


#pragma vector=SD24B_VECTOR
__interrupt void SD24BISR(void)
 {
    switch (SD24BIV)
    {
        case SD24BIV_SD24OVIFG:             // SD24MEM Overflow
            break;
        case SD24BIV_SD24TRGIFG:            // SD24 Trigger IFG
            break;
        case SD24BIV_SD24IFG0:              // SD24MEM0 IFG
            break;
        case SD24BIV_SD24IFG2:              // SD24MEM2 IFG
            break;
        case SD24BIV_SD24IFG6:              // SD24MEM5 IFG
            HAL_SET_GPIO_LEDRED();
            mlib_getSigmaDeltaValues(ChResults);
            HAL_RESET_GPIO_LEDRED();
            break;
    }
}



#pragma vector=DMA_VECTOR
__interrupt void DMA0_ISR(void)
{
    switch (__even_in_range(DMAIV, 16))
    {
        case DMAIV_NONE: break;                   // No interrupts
        case DMAIV_DMA0IFG:                       // DMA0IFG = DMA Channel 0
            // sequence of conversions complete
            ADC10CTL0 &= ~ADC10ENC;               // Disable ADC conversion
            break;
        case DMAIV_DMA1IFG: break;                // DMA1IFG = DMA Channel 1
        case DMAIV_DMA2IFG: break;                // DMA2IFG = DMA Channel 2
        case  8: break;                           // Reserved
        case 10: break;                           // Reserved
        case 12: break;                           // Reserved
        case 14: break;                           // Reserved
        case 16: break;                           // Reserved
        default: break;
    }
}


#pragma vector=TIMER3_A0_VECTOR
__interrupt void TIMER3_A0_ISR(void)
{

}




#pragma vector = USCI_B0_VECTOR
__interrupt void USCI_B0_ISR(void)
{
  switch(__even_in_range(UCB0IV, USCI_I2C_UCBIT9IFG))
  {
    case USCI_NONE:          break;         // Vector 0: No interrupts
    case USCI_I2C_UCALIFG:   break;         // Vector 2: ALIFG
    case USCI_I2C_UCNACKIFG:                // Vector 4: NACKIFG
      break;
    case USCI_I2C_UCSTTIFG:  break;         // Vector 6: STTIFG
    case USCI_I2C_UCSTPIFG:  break;         // Vector 8: STPIFG
    case USCI_I2C_UCRXIFG3:  break;         // Vector 10: RXIFG3
    case USCI_I2C_UCTXIFG3:  break;         // Vector 12: TXIFG3
    case USCI_I2C_UCRXIFG2:  break;         // Vector 14: RXIFG2
    case USCI_I2C_UCTXIFG2:  break;         // Vector 16: TXIFG2
    case USCI_I2C_UCRXIFG1:  break;         // Vector 18: RXIFG1
    case USCI_I2C_UCTXIFG1:  break;         // Vector 20: TXIFG1
    case USCI_I2C_UCRXIFG0:                 // Vector 22: RXIFG0
        I2C_LM75_RX_ISR();
        break;
    case USCI_I2C_UCTXIFG0:                 // Vector 24: TXIFG0
        I2C_LM75_TX_ISR();
        break;
    default: break;
  }
}



// USCI_A0 interrupt service routine
#pragma vector=USCI_A0_VECTOR
__interrupt void USCI_A0_ISR(void)
{
    switch (__even_in_range(UCA0IV, 4))
    {
        case USCI_NONE: break;              // No interrupt
        case USCI_UART_UCRXIFG:             // RXIFG
            comm.rxCompletedFlg = handleUartRxISR(comm.recvBuff, RECV_SIZE);
            break;
        case USCI_UART_UCTXIFG: break;      // TXIFG
        case USCI_UART_UCSTTIFG: break;     // TTIFG
        case USCI_UART_UCTXCPTIFG: break;   // TXCPTIFG
        default: break;
    }
}


#pragma vector=PORT2_VECTOR
__interrupt void Port_2(void)
{
    //xintCount++;
    P2IFG &= ~0x08;
}




// USCI_A0 interrupt service routine
#pragma vector=USCI_A3_VECTOR
__interrupt void USCI_A3_ISR(void)
{
  switch (__even_in_range(UCA3IV, 4))
  {

      case USCI_NONE: break;              // No interrupt
      case USCI_UART_UCRXIFG:
          acMeterHandleRxISR();
          break;    // RXIFG
      case USCI_UART_UCTXIFG:
          acMeterHandleTxISR(&uart3, Petit_Tx_Buf, 8);
          break;      // TXIFG
      case USCI_UART_UCSTTIFG: break;     // TTIFG
      case USCI_UART_UCTXCPTIFG:
          acMeterHandleTxCompleteISR(&uart3, 8);

          break;   // TXCPTIFG
      default: break;
  }
}
