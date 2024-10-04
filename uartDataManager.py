class setDataval:
    
    def __init__(self):
        self._maxChargeVal = 0
        self._bazVal = 0
        self._clearSessionval = 0
        self._startChargeVal = 0
        
    # max_charge_val 
    def setMaxChargeVal(self, value):
        self._maxChargeVal =  value

    def getMaxChargeVal(self):
        return self._maxChargeVal

    # baz_val   
    def setBazVal(self, value):
        self._bazVal = value

    def getBazVal(self):
        return self._bazVal

    #transaction val
    def setClearSessionval(self, value):
        self._clearSessionval = value

    def getClearSessionval(self):
        return self._clearSessionval   

    def setStartChargeVal(self, value):
        self._startChargeVal = value

    def getStartChargeVal(self):
        return self._startChargeVal   
       
    
class SetDataResponse:
    def __init__(self):
        self._runControl = 0
        self._buzzer = 0
        self._clearSession = 0
        self._maxChargeValueResponse = 0
    def setRunControlValueResponse(self, value):
        self._runControl = value
    def getRunControlValueResponse(self):
        return self._runControl

    def setBuzzerValueResponse(self, value):
        self._buzzer = value
    def getBuzzerValueResponse(self):
        return self._buzzer

    def setClearSessionValueResponse(self, value):
        self._clearSession = value
    def getClearSessionValueResponse(self):
        return self._clearSession
    
    def setMaxChargeValueResponse(self, value):
        self._maxChargeValueResponse =  value
    def getMaxChargeValueResponse(self):
        return self._maxChargeValueResponse

class ReadDataResponse:
    def __init__(self):
        self._chargingStartStop = 0
        self._energy = 0
        self._timeSeconds = 0
        self._timeMinutes = 0
        self._timeHours = 0
        self._Power = 0
        self._errorType = 0
        self._evChargeTermination = 0
        self._chargingStatus = 0
        self._connectorStatus = 0
        self._deviceId = 0
        

    def setChargingStartStop(self, value):
        self._chargingStartStop = value
    def getChargingStartStop(self):
        return self._chargingStartStop

    def setEnergy(self, value):
        self._energy = value
    def getEnergy(self):
        return self._energy

    def setTimeSeconds(self, value):
        self._timeSeconds = value
    def getTimeSeconds(self):
        return self._timeSeconds

    def setTimeMinutes(self, value):
        self._timeMinutes = value
    def getTimeMinutes(self):
        return self._timeMinutes
    
    def setTimeHours(self, value):
        self._timeHours = value
    def getTimeHours(self):  
        return self._timeHours

    def setPower(self, value):
        self._Power = value
    def getPower(self):
        return self._Power

    def setErrorType(self, value):
        self._errorType = value
    def getErrorType(self):
        return self._errorType
    
    def setEVChargeTermination(self, value):
        self._evChargeTermination = value
    def getEVChargeTermination(self):
        return self._evChargeTermination
    

    def setChargingStatus(self, value):
        self._chargingStatus = value
    def getChargingStatus(self):
        return self._chargingStatus
    
    def setConnectorStatus(self, value):
        self._connectorStatus = value
    def getConnectorStatus(self):
        return self._connectorStatus   
    
    def setDeviceId(self, value):
        self._deviceId = value
    def getDeviceId(self):
        return self._deviceId
 
readDataResponse = ReadDataResponse()
setdataval = setDataval()
setDataResponse = SetDataResponse()
#setdataval.set_start_charge_val(1)  







