from uartHal import UARTFrame, recieveframe, RxTxFonk
from uartDataManager import setDataResponse,readDataResponse 
import asyncio

# Command and message types

class CmdTypeData: 
    SET_DATA = 0
    SET_DATA_RESPONSE = 1
    READ_DATA = 2
    READ_DATA_RESPONSE = 3


class MessageTypeData:
    MODE = 0
    RUN_CTRL = 1
    DEVICE_ID = 2  
    ENERGY = 3
    CHARGING_TIME_MIN_SEC = 4
    POWER = 5
    ERR_STATUS = 6
    EV_CHARGE_TERMINATION = 7
    BUZZER_CMD = 8 #CLEAR_CHARGE
    CLEAR_SESSION = 9#end transection
    CHARGING_STATUS = 10
    CONNECTOR_STATUS = 11
    CHARGING_TIME_HOURS = 12
    MAX_POWER= 13
    
    
messageTypeData = MessageTypeData()
cmdTypeData = CmdTypeData()




class UartProtokol:
    def __init__(self, UART_HAL):# logger=None):
        self.recieve_message_err_status = 0
        self.UART_HAL = UART_HAL
        # self.logger = logger
        
    def handleSET_DATA_RES(self):
       #  self.logger.status("charge", filename="uartProtocol.py", category="charge  stuation", status="---------------------------------set data response-------------------------------------------------------")
        print("set data response")
        if recieveframe.get_msg_type() == messageTypeData.MODE:
            pass
        elif recieveframe.get_msg_type() == messageTypeData.RUN_CTRL:
            setDataResponse.setRunControl(recieveframe.get_dataL())
            # self.logger.status("charge", filename="uartProtocol.py", category="charge  stuation", status=f"runcntrl: {recieveframe.get_dataL()}")
            print(f"runcntrl: {recieveframe.get_dataL()}")

            
        elif recieveframe.get_msg_type() == messageTypeData.BUZZER_CMD:
            setDataResponse.setBuzzer(recieveframe.get_dataL())
           #  self.logger.status("charge", filename="uartProtocol.py", category="charge  stuation", status=f"buzzer:{recieveframe.get_dataL()}")
            print(f"buzzer:{recieveframe.get_dataL()}")
            
        elif recieveframe.get_msg_type() == messageTypeData.CLEAR_SESSION:
            setDataResponse.setClearSession(recieveframe.get_dataL())
            # self.logger.status("charge", filename="uartProtocol.py", category="charge  stuation", status=f"clear session:{recieveframe.get_dataL()}")
            print(f"clear session:{recieveframe.get_dataL()}")
            
        elif recieveframe.get_msg_type() == messageTypeData.MAX_POWER:
            setDataResponse.setMaxChargeValueResponse(recieveframe.get_dataL())
            # self.logger.status("charge", filename="uartProtocol.py", category="charge  stuation", status=f"Max Charge Value Response :{recieveframe.get_dataL()}")
            print(f"Max Charge Value Response:{recieveframe.get_dataL()}")

    def handleREAD_DATA_RES(self):
        print("read data response")
        if recieveframe.get_msg_type() == messageTypeData.MODE:
            pass
        elif recieveframe.get_msg_type() == messageTypeData.RUN_CTRL:
            readDataResponse.setChargingStartStop(recieveframe.get_dataL())
           #  self.logger.status("charge", filename="uartProtocol.py", category="charge  stuation", status=f"charging start stop:{recieveframe.get_dataL()}")
            print(f"charging start stop:{recieveframe.get_dataL()}")
            
        elif recieveframe.get_msg_type() == messageTypeData.ENERGY:
            readDataResponse.setEnergy(recieveframe.get_dataL())
           #  self.logger.status("charge", filename="uartProtocol.py", category="charge  stuation", status=f"read energy:{recieveframe.get_dataL()}")
            print(f"read energy:{recieveframe.get_dataL()}") 
            
        elif recieveframe.get_msg_type() == messageTypeData.CHARGING_TIME_MIN_SEC:
            readDataResponse.setTimeSeconds(recieveframe.get_dataL())
            readDataResponse.setTimeMinutes(recieveframe.get_dataH())
            # self.logger.status("charge", filename="uartProtocol.py", category="charge  stuation", status=f"read timesaniye{recieveframe.get_dataL()}")
            # self.logger.status("charge", filename="uartProtocol.py", category="charge  stuation", status=f"read timedakika{recieveframe.get_dataH()}")
            print(f"read timesaniye{recieveframe.get_dataL()}")
            print(f"read timedakika{recieveframe.get_dataH()}")
        
        elif recieveframe.get_msg_type() == messageTypeData.CHARGING_TIME_HOURS :
            readDataResponse.setTimeHours(recieveframe.get_dataL())
            # self.logger.status("charge", filename="uartProtocol.py", category="charge  stuation", status=f"read device time hours {recieveframe.get_dataL()}")
            print("read device time hours ")  
            
        elif recieveframe.get_msg_type() == messageTypeData.POWER:
            readDataResponse.setPower(recieveframe.get_dataL())
            # self.logger.status("charge", filename="uartProtocol.py", category="charge  stuation", status=f"read rms value of power:{recieveframe.get_dataL()}")
            print(f"read rms value of power:{recieveframe.get_dataL()}")
            
        elif recieveframe.get_msg_type() == messageTypeData.ERR_STATUS:
            readDataResponse.setErrorType(recieveframe.get_dataL())
            # self.logger.status("charge", filename="uartProtocol.py", category="charge  stuation", status=f"type of error:{recieveframe.get_dataL()}")
            print(f"type of error:{recieveframe.get_dataL()}")
            
        elif recieveframe.get_msg_type() == messageTypeData.EV_CHARGE_TERMINATION:
            readDataResponse.setEVChargeTermination(recieveframe.get_dataL())
           #  self.logger.status("charge", filename="uartProtocol.py", category="charge  stuation", status=f"charge finish:{recieveframe.get_dataL()}")
            print(f"charge finish:{recieveframe.get_dataL()}")
            
        elif recieveframe.get_msg_type() == messageTypeData.CHARGING_STATUS:
            readDataResponse.setChargingStatus(recieveframe.get_dataL())
            # self.logger.status("charge", filename="uartProtocol.py", category="charge  stuation", status=f"charge status:{recieveframe.get_dataL()}")
            print(f"charge status:{recieveframe.get_dataL()}")       
            
            
        elif recieveframe.get_msg_type() == messageTypeData.CONNECTOR_STATUS:
            readDataResponse.setConnectorStatus(recieveframe.get_dataL())
            # self.logger.status("charge", filename="uartProtocol.py", category="charge  stuation", status=f"conn status:{recieveframe.get_dataL()}")
            print(f"conn status:{recieveframe.get_dataL()}")
            
        elif recieveframe.get_msg_type() == messageTypeData.DEVICE_ID :
            readDataResponse.setDeviceId(recieveframe.get_dataL())
           # self.logger.status("charge", filename="uartProtocol.py", category="charge  stuation", status=f"read device id{recieveframe.get_dataL()}")
            print(f"read device id{recieveframe.get_dataL()}")
 

    async def reciveHandleUartFrame(self):
        while True:
            if(self.UART_HAL.rxSuccess == 1):
                if recieveframe.get_cmd_type() == cmdTypeData.SET_DATA_RESPONSE:
                    self.handleSET_DATA_RES()
                elif recieveframe.get_cmd_type() == cmdTypeData.READ_DATA_RESPONSE:
                    self.handleREAD_DATA_RES()
                    
                self.UART_HAL.rxSuccess = 0
                
                

            await asyncio.sleep(0.1)
