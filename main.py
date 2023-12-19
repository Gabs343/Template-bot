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
        self.__settings_services = [setting(bot_name=self.__bot_name) for setting in (BotSetting, TaskManagerSetting)]
        
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
        self.__execution_begun()
        
        #Your code goes here
        
        ####################
          
        self.__execution_completed()
                
    def pause(self):
        self.__notify_status(new_status='PAUSED')
            
    def unpause(self):
        self.__notify_status(new_status='RUNNING')
        
    def stop(self):
        self.__notify_status(new_status='CLOSING BOT')
        
    def __execution_begun(self) -> None:
        self.__logs_services = [log() for log in (LogTxt, LogXlsx)]
        bot_setting_service: BotSetting = self.__get_setting_service(setting_type=BotSetting)
        bot_setting_service.settings['executions'] += 1
        self.__notify_status(new_status="RUNNING")
             
    def __execution_completed(self, had_error: bool = False):
        bot_setting_service: BotSetting = self.__get_setting_service(setting_type=BotSetting)
        if(had_error):  
            bot_setting_service.settings['bad_executions'] += 1
        else:
            bot_setting_service.settings['good_executions'] += 1
            
        bot_setting_service.update()
        self.__close_logs()
        self.__notify_status(new_status="READY")
        
    def __notify_status(self, new_status: str) -> None:
        self.__status = new_status
        logTxt: LogTxt = self.__get_log_service(log_type=LogTxt)
        logTxt.write_info(message=f'Bot {new_status}')
        if self.__status_callback:
            self.__status_callback(new_status)
        
    def __get_log_service(self, log_type: LogService) -> LogService:
        return next(log for log in self.__logs_services if isinstance(log, log_type))
    
    def __get_setting_service(self, setting_type: SettingService) -> SettingService:
        return next(service for service in self.__settings_services if isinstance(service, setting_type))
    
    def __execute_action(self, function, *args):
        logTxt: LogTxt = self.__get_log_service(log_type=LogTxt)
        if(self.__status == 'PAUSED'):
            while True:
                if(self.__status=='RUNNING'):
                    break
        return logTxt.write_and_execute(function, *args)
    
    def __close_logs(self) -> None:
        for log in self.__logs_services:
            log.close()
                       
            
if __name__ == "__main__":
    st = time.time()
    main = Main()
    main.start()
    et = time.time()
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')
        
    
