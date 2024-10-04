#ifndef PROXIMITYPILOT_H_
#define PROXIMITYPILOT_H_


#define DUTY_20A                                    ((unsigned int)(33))
#define DUTY_32A                                    ((unsigned int)(53))
#define DUTY_63A                                    ((unsigned int)(89))
#define DUTY_ERR                                    ((unsigned int)(0))

#define isCable20A(i)                               (i>=_IQ(0.429) && i<_IQ(0.456))
#define isCable32A(i)                               (i>=_IQ(0.189) && i<_IQ(0.206))
#define isCable60A(i)                               (i>=_IQ(0.095) && i<_IQ(0.105))





typedef struct {
    t_mvngAvg avg;
    _iq qout;
    float out;
    unsigned int dutyRatio;
} t_ppVoltage;

t_ppVoltage ppLevel;

void pp_VoltageLevel(_iq voltage){
    ppLevel.avg.qoutVal = dsp_MovingAvg(ppLevel.avg.buffer, &ppLevel.avg.sum, ppLevel.avg.pos, LENGTH_OF_MOVIG_AVG, voltage);
    ppLevel.qout = ppLevel.avg.qoutVal;

    ppLevel.out = _IQtoF(ppLevel.qout);
    ppLevel.avg.pos++;
    if (ppLevel.avg.pos >= LENGTH_OF_MOVIG_AVG){
        ppLevel.avg.pos = 0;
    }

}

void pp_SetMaxCurrent(_iq voltage){
    static unsigned int dutyCycle = 0;
    static unsigned int dutyCycleOld = 0;

    if(isCable20A(voltage)){
        dutyCycle = DUTY_20A;
    }
    else if(isCable32A(voltage)){
        dutyCycle = DUTY_32A;
    }
    else if(isCable60A(voltage)){
        dutyCycle = DUTY_63A;
    }
    else
    {
        dutyCycle = dutyCycleOld;
    }

    dutyCycleOld = dutyCycle;
    ppLevel.dutyRatio = dutyCycle;
}


void pp_Handle(_iq voltage){
    pp_VoltageLevel(voltage);
    pp_SetMaxCurrent(ppLevel.qout);
}


#endif /* PROXIMITYPILOT_H_ */
