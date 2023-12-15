import time

from logs import *
from settings import *
  
class Main:
    __settings_services: list[SettingService] = []
    __logs_services: list[LogService] = []
    __bot_name: str = "TEST"
    __status: str = "READY"
    __status_callback = None
    
    def __init__(self) -> None:
        self.__settings_services = [setting() for setting in (SettingBot,)]
    
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
    
    def set_status_changed_callback(self, callback) -> None:
        self.__status_callback = callback

    def __notify_status(self, new_status: str) -> None:
        self.__status = new_status
        if self.__status_callback:
            self.__status_callback(new_status)
        
    def start(self) -> None:
        self.__logs_services = [log() for log in (LogTxt, LogXlsx)]
        self.__notify_status(new_status="RUNNING")
        
        #Your code goes here
        
        ####################
          
        self.__notify_status(new_status="READY")
                 
        
            
if __name__ == "__main__":
    st = time.time()
    main = Main()
    main.start()
    et = time.time()
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')
        
    
