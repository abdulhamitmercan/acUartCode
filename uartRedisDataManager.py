import redis.asyncio as redis
import asyncio
from uartDataManager import readDataResponse, setdataval, setDataResponse

class SetDatavalManager:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)


    async def run(self):
        while True:
            #setdataval getting redis and write data menegement
            # setdataval.setMaxChargeVal((int)(await self.redis_client.hget("Uart", "maxChargeVal")))
            # setdataval.setBazVal((int)(await self.redis_client.hget("Uart", "bazVal")))
            # setdataval.setClearSessionval((int)(await self.redis_client.hget("Uart", "ClearSessionval")))
            # setdataval.setStartChargeVal((int)(await self.redis_client.hget("Uart", "startChargeVal")))

            
            await asyncio.sleep(0.1)


class SetDataResponseManager:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

    async def run(self):
        while True:
            #setdataresponse getting data menegement and write redis
            await self.redis_client.hset("Uart", "runControlValueResponse", setDataResponse.getRunControlValueResponse())
            await self.redis_client.hset("Uart", "buzzerValueResponse", setDataResponse.getBuzzerValueResponse())
            await self.redis_client.hset("Uart", "clearSessionValueResponse", setDataResponse.getClearSessionValueResponse())
            await self.redis_client.hset("Uart", "maxChargeValueResponse", setDataResponse.getMaxChargeValueResponse())
            
            await asyncio.sleep(0.1)


class ReadDataResponseManager:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

    async def run(self):
        while True:
            #readdataresponse getting data menegement and write redis
            await self.redis_client.hset("Uart", "chargingStartStop", readDataResponse.getChargingStartStop())
            await self.redis_client.hset("Uart", "energy", readDataResponse.getEnergy())
            await self.redis_client.hset("Uart", "timeSeconds", readDataResponse.getTimeSeconds())
            await self.redis_client.hset("Uart", "timeMinutes", readDataResponse.getTimeMinutes())
            await self.redis_client.hset("Uart", "timeHours", readDataResponse.getTimeHours())
            await self.redis_client.hset("Uart", "power", readDataResponse.getPower())
            await self.redis_client.hset("Uart", "errorType", readDataResponse.getErrorType())
            await self.redis_client.hset("Uart", "chargingStatus", readDataResponse.getChargingStatus())
            await self.redis_client.hset("Uart", "connectorStatus", readDataResponse.getConnectorStatus())
            await self.redis_client.hset("Uart", "deviceId", readDataResponse.getDeviceId())
            await self.redis_client.hset("Uart", "EVChargeTermination", readDataResponse.getEVChargeTermination())

            # print("redis read data response set")
            await asyncio.sleep(0.1)


# async def main():
    
#     setdataval_manager = SetDatavalManager()
#     setdataresponse_manager = SetDataResponseManager()
#     readdataresponse_manager = ReadDataResponseManager()

    
#     await asyncio.gather(setdataval_manager.run(),setdataresponse_manager.run(),readdataresponse_manager.run())


# if __name__ == '__main__':
#     asyncio.run(main())

