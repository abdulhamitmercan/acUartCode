#ifndef RTMEM_H_
#define RTMEM_H_


unsigned int states[50];
unsigned int commands[50];


//*****************************************************************************
//
//! STATE MEMORY
//
//*****************************************************************************
#define getState_Energy(r)            (r = (int)(states[0]));
#define getState_ChargingTimeMinSec(r)                       (r = (int)(states[1]));
#define getState_Power(r)                               (r = (int)(states[2]));
#define getState_DeviceId(r)                             (r = (int)(states[3]));
#define getState_ErrStatus(r)                          (r = (int)(states[4]));
#define getState_EVChargeTermination(r)                     (r = (int)(states[5]));
#define getState_ChargingStatus(r)                     (r = (int)(states[6]));
#define getState_ConnectorStatus(r)                    (r = (int)(states[7]));
#define getState_ChargingTimeHours(r)                  (r = (int)(states[8]));


#define setState_Energy(d)            (states[0] = d);
#define setState_ChargingTimeMinSec(d)                       (states[1] = d);
#define setState_Power(d)                               (states[2] = d);
#define setState_DeviceId(d)                             (states[3] = d);
#define setState_ErrStatus(d)                          (states[4] = d);
#define setState_EVChargeTermination(d)                     (states[5] = d);
#define setState_ChargingStatus(d)                     (states[6] = d);
#define setState_ConnectorStatus(d)                    (states[7] = d);
#define setState_ChargingTimeHours(d)                  (states[8] = d);


//*****************************************************************************
//
//! COMMAND MEMORY
//
//*****************************************************************************
#define getRunCtrl(r)                    (r = (unsigned int)(commands[0]));
#define getBuzzer(r)         (r = (unsigned int)(commands[1]));
#define getClearSession(r)             (r = (unsigned int)(commands[2]));
#define getMaxPower(r)             (r = (unsigned int)(commands[3]));

#define setRunCtrl(d)                    (commands[0] = d);
#define setBuzzer(d)         (commands[1] = d);
#define setClearSession(d)             (commands[2] = d);
#define setMaxPower(d)             (commands[3] = d);



#endif /* RTMEM_H_ */
