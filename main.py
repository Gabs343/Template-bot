import time

from logs import *
from settings import *
  
class Main:
    __settings_services: list[SettingService] = []
    __logs_services: list[LogService] = []
    __bot_name: str = "TEST"
    __status: str = "READY"
    
    def __init__(self) -> None:
        self.__settings_services = [setting() for setting in (SettingBot,)]
        self.__logs_services = [log() for log in (LogTxt, LogXlsx)]
    
    @property   
    def settings_services(self) -> list[SettingService]:
        return self.__settings_services
    
    @property   
    def logs_services(self) -> list[LogService]:
        return self.__logs_services
    
    @property   
    def bot_name(self) -> str:
        return self.__bot_name
    
    @property   
    def status(self) -> str:
        return self.__status
        
    def start(self) -> None:
        #Your code goes here
        for service in self.__settings_services:
            print(service.settings)
        
        for log in self.__logs_services:
            log.write_info(log)
            log.close()
                 
        
            
if __name__ == "__main__":
    st = time.time()
    main = Main()
    main.start()
    et = time.time()
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')
        
    
