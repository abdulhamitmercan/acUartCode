import asyncio
from uartProtocol import UartProtokol, messageTypeData, cmdTypeData
from uartHal import RxTxFonk, sendframe
from uartDataManager import  setdataval
from uartRedisDataManager import SetDatavalManager, SetDataResponseManager, ReadDataResponseManager
from debug_logger import DebugLogger
class SetDataValue:
    # Sabit değerler  
    STOP_CHARGE = 2
    START_CHARGE = 1

   
    CLEAR_SESSION_ENABLE = 1 #END_TRANSACTION = 1
    CLEAR_SESSION_DISABLE = 0 #NOT_END_TRANSACTION = 0
    

class UartHandler:

    def __init__(self, txHAL,logger=None):
        self.txHAL = txHAL
        self.logger = logger
    def sendStartCharging(self):
        sendframe.set_cmd_type(cmdTypeData.SET_DATA)
        sendframe.set_msg_type(messageTypeData.RUN_CTRL)
        sendframe.set_dataL(SetDataValue.START_CHARGE)
        self.txHAL.send_message()
    
    def sendMaxPower(self):
        sendframe.set_cmd_type(cmdTypeData.SET_DATA)
        sendframe.set_msg_type(messageTypeData.MAX_POWER)
        sendframe.set_dataL(setdataval.getMaxChargeVal())
        self.txHAL.send_message()

    def sendStopCharging(self):
        sendframe.set_cmd_type(cmdTypeData.SET_DATA)
        sendframe.set_msg_type(messageTypeData.RUN_CTRL)
        sendframe.set_dataL(SetDataValue.STOP_CHARGE)
        self.txHAL.send_message()


    def sendReadDeviceId(self):
        sendframe.set_cmd_type(cmdTypeData.READ_DATA)
        sendframe.set_msg_type(messageTypeData.DEVICE_ID)
        self.txHAL.send_message()

    def sendReadEnergy(self):
        sendframe.set_cmd_type(cmdTypeData.READ_DATA)
        sendframe.set_msg_type(messageTypeData.ENERGY)
        self.txHAL.send_message()

    def sendReadChargingTimeMinSec(self):
        sendframe.set_cmd_type(cmdTypeData.READ_DATA)
        sendframe.set_msg_type(messageTypeData.CHARGING_TIME_MIN_SEC)
        self.txHAL.send_message()

    def sendReadChargingTimeHour(self):
        sendframe.set_cmd_type(cmdTypeData.READ_DATA)
        sendframe.set_msg_type(messageTypeData.CHARGING_TIME_HOURS)
        self.txHAL.send_message()

    def sendReadPower(self):
        sendframe.set_cmd_type(cmdTypeData.READ_DATA)
        sendframe.set_msg_type(messageTypeData.POWER)
        self.txHAL.send_message()

    def sendReadErr(self):
        sendframe.set_cmd_type(cmdTypeData.READ_DATA)
        sendframe.set_msg_type(messageTypeData.ERR_STATUS)
        self.txHAL.send_message()

    def sendReadEVChargeTermination(self):
        sendframe.set_cmd_type(cmdTypeData.READ_DATA)
        sendframe.set_msg_type(messageTypeData.EV_CHARGE_TERMINATION)
        self.txHAL.send_message()



    def sendClearSessionEnable(self):
        sendframe.set_cmd_type(cmdTypeData.SET_DATA)
        sendframe.set_msg_type(messageTypeData.CLEAR_SESSION)
        sendframe.set_dataL(SetDataValue.CLEAR_SESSION_ENABLE)
        self.txHAL.send_message()

    def sendClearSessionDisable(self):
        sendframe.set_cmd_type(cmdTypeData.SET_DATA)
        sendframe.set_msg_type(messageTypeData.CLEAR_SESSION)
        sendframe.set_dataL(SetDataValue.CLEAR_SESSION_DISABLE)
        self.txHAL.send_message()

    def sendReadConnectorStatus(self):
        sendframe.set_cmd_type(cmdTypeData.READ_DATA)
        sendframe.set_msg_type(messageTypeData.CONNECTOR_STATUS)
        self.txHAL.send_message()

    def sendReadChargingStatus(self):
        sendframe.set_cmd_type(cmdTypeData.READ_DATA)    
        sendframe.set_msg_type(messageTypeData.CHARGING_STATUS)   
        self.txHAL.send_message() 
    
    def sendSetBuzzer(self):    
        sendframe.set_cmd_type(cmdTypeData.SET_DATA)    
        sendframe.set_msg_type(messageTypeData.BUZZER_CMD)    
        sendframe.set_dataL(setdataval.getBazVal())    
        self.txHAL.send_message()

    async def handleSET_DATA(self):  
        
        
        self.sendMaxPower()  
        await asyncio.sleep(0.2) 
               
        self.sendSetBuzzer()
        await asyncio.sleep(0.2)
   
         
        if((setdataval.getStartChargeVal()== SetDataValue().START_CHARGE) ):
            
            self.logger.status("charge", filename="uartProtocolHandler.py", category="charge stuation", status="---------------------------------startcharge-------------------------------------------------------")
            print("---------------------------------startcharge-------------------------------------------------------")
            self.sendStartCharging()    
            await asyncio.sleep(0.2)    
        else:
            self.logger.status("charge", filename="uartProtocolHandler.py", category="charge stuation", status="---------------------------------stopcharge-------------------------------------------------------")
            print("---------------------------------stopcharge-------------------------------------------------------")
            self.sendStopCharging()
            await asyncio.sleep(0.2)
        
        if(setdataval.getClearSessionval() == SetDataValue().CLEAR_SESSION_ENABLE):
            self.sendClearSessionEnable
            await asyncio.sleep(0.2)
        else:
            self.sendClearSessionDisable()
            await asyncio.sleep(0.2)

    async def handleREAD_DATA(self):
        

        self.sendReadDeviceId()
        await asyncio.sleep(0.2)
        self.sendReadEnergy()
        await asyncio.sleep(0.2)
        self.sendReadChargingTimeMinSec()
        await asyncio.sleep(0.2)
        self.sendReadChargingTimeHour()
        await asyncio.sleep(0.2)
        self.sendMaxPower()
        await asyncio.sleep(0.2)
        self.sendReadErr()
        await asyncio.sleep(0.2)
        self.sendReadEVChargeTermination()
        await asyncio.sleep(0.2)
        self.sendReadConnectorStatus()
        await asyncio.sleep(0.2)
        
        self.sendReadChargingStatus()
        await asyncio.sleep(0.2)

    async def sendHandleUartFrame(self):
        while True:
            await self.handleREAD_DATA()
            await self.handleSET_DATA()



             
async def main():
    rxtx_fonk = RxTxFonk(logger)
    myUart = UartProtokol(rxtx_fonk,logger)
    uart_handler = UartHandler(rxtx_fonk,logger )
    logger = DebugLogger(level=DebugLogger.LEVEL_INFO, format_type=DebugLogger.FORMAT_FILE_LINE, log_file_path='uart.log')

    setdataval_manager = SetDatavalManager()
    setdataresponse_manager = SetDataResponseManager()
    readdataresponse_manager = ReadDataResponseManager()

    await asyncio.gather(
        rxtx_fonk.receive_message(),
        myUart.reciveHandleUartFrame(),
        uart_handler.sendHandleUartFrame(),

        setdataval_manager.run(),
        setdataresponse_manager.run(),
        readdataresponse_manager.run()
    )

asyncio.run(main())


 


