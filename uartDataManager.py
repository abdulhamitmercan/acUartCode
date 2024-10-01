class setDataval:
    
    def __init__(self):
        self._maxChargeVal = 0
        self._bazVal = 0
        self._transactionVal = 0
        self._startChargeVal = 0
        
    # max_charge_val 
    def set_max_charge_val(self, value):
        
        self._maxChargeVal =  value

    def get_max_charge_val(self):
        return self._maxChargeVal

    # baz_val   
    def set_baz_val(self, value):
        self._bazVal = value

    def get_baz_val(self):
        return self._bazVal

    #transaction val
    def set_transaction_val(self, value):
        self._transactionVal = value

    def get_transaction_val(self):
        return self._transactionVal   

    def set_start_charge_val(self, value):
        self._startChargeVal = value

    def get_start_charge_val(self):
        return self._startChargeVal   
       
    
class SetDataResponse:
    def __init__(self):
        self._runControl = 0
        self._clearChargeSession = 0
        self._endTransaction = 0

    def setRunControl(self, value):
        self._runControl = value
    def getRunControl(self):
        return self._runControl

    def setClearChargeSession(self, value):
        self._clearChargeSession = value
    def getClearChargeSession(self):
        return self._clearChargeSession

    def setEndTransaction(self, value):
        self._endTransaction = value
    def getEndTransaction(self):
        return self._endTransaction


class ReadDataResponse:
    def __init__(self):
        self._chargingStartStop = 0
        self._energyTotalComplate = 0
        self._timeSeconds = 0
        self._timeMinutes = 0
        self._timeHours = 0
        self._rmsPowerValue = 0
        self._errorType = 0
        self._chargeFinished = 0
        self._chargeComplete = 0
        self._chargingStatus = 0
        self._connectorStatus = 0
        self._deviceId = 0
        

    def setChargingStartStop(self, value):
        self._chargingStartStop = value
    def getChargingStartStop(self):
        return self._chargingStartStop

    def setEnergyTotalComplate(self, value):
        self._energyTotalComplate = value
    def getEnergyTotalComplate(self):
        return self._energyTotalComplate

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

    def setRmsPowerValue(self, value):
        self._rmsPowerValue = value
    def getRmsPowerValue(self):
        return self._rmsPowerValue

    def setErrorType(self, value):
        self._errorType = value
    def getErrorType(self):
        return self._errorType
    
    def setChargeFinished(self, value):
        self._chargeFinished = value
    def getChargeFinished(self):
        return self._chargeFinished
    
    def setChargeComplete(self, value):
        self._chargeComplete = value
    def getChargeComplete(self):
        return self._chargeComplete

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







