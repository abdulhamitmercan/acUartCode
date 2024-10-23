import serial
import asyncio
from dataclasses import dataclass
import serial_asyncio

@dataclass
class UARTFrame:
    header: int = 0x62  # Sabit değer
    cmd_type: int = 0x00
    msg_type: int = 0x00
    dataH: int = 0x00
    dataL: int = 0x00
    eof: int = 0x6B  # Sabit değer

    def __post_init__(self):
        # Her değeri 1 byte (0xFF)
        self.cmd_type &= 0xFF
        self.msg_type &= 0xFF
        self.dataH &= 0xFF
        self.dataL &= 0xFF

    @property
    def rsv1(self):
        return 0x00  # Sabit değer

    @property
    def rsv0(self):
        return 0x00  # Sabit değer

    def get_cmd_type(self):
        return self.cmd_type

    def get_msg_type(self):
        return self.msg_type

    def get_dataH(self):
        return self.dataH

    def get_dataL(self):
        return self.dataL

    def set_cmd_type(self, value):
        self.cmd_type = value & 0xFF

    def set_msg_type(self, value):
        self.msg_type = value & 0xFF

    def set_dataH(self, value):
        self.dataH = value & 0xFF

    def set_dataL(self, value):
        self.dataL = value & 0xFF

sendframe = UARTFrame()
recieveframe = UARTFrame()

ser = serial.Serial("/dev/ttyS0", 9600)

class RxTxFonk:
    def __init__(self, logger=None):
        self.recieve_message_err_status = None
        self.rxSuccess = 0
        self.logger = logger
        self.buffer = bytearray()  # Buffer to accumulate received data

    def uartformat_to_rawdata_send_message(self): 
        byte_list = [
            sendframe.header,
            sendframe.get_cmd_type(),
            sendframe.get_msg_type(),
            sendframe.rsv1,
            sendframe.rsv0,
            sendframe.get_dataH(),
            sendframe.get_dataL(),
            sendframe.eof,
        ]
        return bytearray(byte_list)

    def rawdata_to_uartformat_recieve_message(self, received_message):
        if len(received_message) != 8:
            self.logger.error("", filename="uartHal.py", category="message situation", status=f"Geçersiz mesaj uzunluğu: {len(received_message)}")
            return None
        else:
            byte_list = [0] * 8
            
            for index, byte in enumerate(received_message):
                byte_list[index] = byte

            if byte_list[0] == 0x62 and byte_list[3] == 0x00 and byte_list[4] == 0x00 and byte_list[7] == 0x6B:
                recieveframe.set_cmd_type(byte_list[1])
                recieveframe.set_msg_type(byte_list[2])
                recieveframe.set_dataH(byte_list[5])
                recieveframe.set_dataL(byte_list[6])
                self.recieve_message_err_status = 0                
                self.rxSuccess = 1
                
                return self.recieve_message_err_status
            else:
                self.logger.error("", filename="uatHal.py", category="message situation", status="Hatalı mesaj alındı")
                self.recieve_message_err_status = 1
                return self.recieve_message_err_status

    def send_message(self):
        formatted_message = self.uartformat_to_rawdata_send_message()
        ser.write(formatted_message)

    async def receive_message(self):
        while True:
            if ser.in_waiting >= 8:
                # Okunan verileri al
                received_data = ser.read(8)
                self.buffer.extend(received_data)

                # Mesajı işleme
                while len(self.buffer) >= 8:
                    data_to_process = self.buffer[:8]
                    self.buffer = self.buffer[8:]
                    recieve_message_err_status = self.rawdata_to_uartformat_recieve_message(data_to_process)

                    if recieve_message_err_status == 1:
                        self.logger.error("", filename="uatHal.py", category="message situation", status="Alınan veri")
                        for index, byte in enumerate(data_to_process):
                            self.logger.error("", filename="uartHal.py", category="message situation", status=f"Bayt {index}: {byte:02X}")

            await asyncio.sleep(0.01)  # Bekleme süresi

    def connection_made(self, transport):
        self.transport = transport
        print("Bağlandı!")

    def data_received(self, data):
        self.buffer.extend(data)
        while len(self.buffer) >= 8:
            data_to_process = self.buffer[:8]
            self.buffer = self.buffer[8:]

            recieve_message_err_status = self.rawdata_to_uartformat_recieve_message(data_to_process)

            if recieve_message_err_status == 1:
                self.logger.error("", filename="uatHal.py", category="message situation", status="Alınan veri")
                for index, byte in enumerate(data_to_process):
                    self.logger.error("", filename="uartHal.py", category="message situation", status=f"Bayt {index}: {byte:02X}")

    def connection_lost(self, exc):
        print("Bağlantı kesildi!")
        asyncio.get_event_loop().stop()





"""
async def main():
    logger = None  # Logger'ı buraya ekleyin
    rx_tx_fonk = RxTxFonk(logger)

    while True:
        await rx_tx_fonk.receive_message()

if __name__ == "__main__":
    asyncio.run(main())
"""