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
    
    @property   
    def status_callback(self) -> str:
        return self.__status_callback
    
    @status_callback.setter
    def status_callback(self, callback) -> None:
        self.__status_callback = callback
        
    def start(self) -> None:
        self.__logs_services = [log() for log in (LogTxt, LogXlsx)]
        self.__notify_status(new_status="RUNNING")
        
        #Your code goes here
        
        ####################
          
        self.__notify_status(new_status="READY")
        
    def pause(self):
        self.__notify_status(new_status='PAUSED')
            
    def unpause(self):
        self.__notify_status(new_status='RUNNING')
        
    def __notify_status(self, new_status: str) -> None:
        self.__status = new_status
        logTxt: LogTxt = self.__get_log(log_type=LogTxt)
        logTxt.write_info(message=f'Bot {new_status}')
        if self.__status_callback:
            self.__status_callback(new_status)
        
    def __get_log(self, log_type: LogService) -> LogService:
        return next(log for log in self.__logs_services if isinstance(log, log_type))
    
    def __execute_action(self, function, *args):
        logTxt: LogTxt = self.get_log(log_type=LogTxt)
        if(self.__status == 'PAUSED'):
            while True:
                if(self.__status=='RUNNING'):
                    break
        return logTxt.write_and_execute(function, *args)
                       
            
if __name__ == "__main__":
    st = time.time()
    main = Main()
    main.start()
    et = time.time()
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')
        
    
