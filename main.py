import os
import time
import logging
import pandas as pd
from datetime import datetime

class LogService:
    def create() -> None: raise NotImplementedError
    def write_info(message: str) -> None: raise NotImplementedError
    def write_error() -> None: raise NotImplementedError
    def close() -> None: raise NotImplementedError
    
    def create_folder(self, path: str) -> None:
        if(not os.path.exists(path)):
            os.makedirs(path)
    
class LogTxt(LogService):
    def __init__(self) -> None:
        super().__init__()
        self.__path: str = f'{os.path.dirname(os.path.abspath(__file__))}\\logs\\logsTxt'
        self.__name: str = f'Log-{datetime.now().strftime("%d.%m.%Y_%H%M%S")}'
        self.__logger: logging.Logger = None
        self.create_folder(path=self.__path)
        self.create()
            
    def create(self) -> None:
        logger_file: str = f'{self.__path}\\{self.__name}.txt'
        formatter: logging.Formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler: logging.FileHandler = logging.FileHandler(logger_file)
        
        self.__logger = logging.getLogger(self.__name)
        self.__logger.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        self.__logger.addHandler(handler)
        
    def write_info(self, message: str) -> None:
        self.__logger.info(message)
        
    def write_and_execute(self, function, *args):
        some_data = None
        if(args): 
            self.write_info(message=f'executing function: {function.__name__} with arguments: {args}')
            some_data = function(*args)
        else:
            self.write_info(message=f'executing function: {function.__name__} with no arguments: {args}') 
            some_data = function()
        self.write_info(message=f'function: {function.__name__} finished')
        return some_data
        
    def write_error(self, message: str, detail: str = None) -> None:
        self.__logger.critical(f'{message} - {detail}')

    def close(self) -> None:
        for handler in self.__logger.handlers[:]:
            self.__logger.removeHandler(handler)
            handler.close()
            
    def __str__(self) -> str:
        return "Log Txt"
            
class LogXlsx(LogService):
    def __init__(self) -> None:
        super().__init__()
        self.__path: str = f'{os.path.dirname(os.path.abspath(__file__))}\\logs\\logsXlsx'
        self.__name: str = f'Log-{datetime.now().strftime("%d.%m.%Y_%H%M%S")}'
        self.__row: int = 1
        self.__log: dict = {}
        self.create_folder(path=self.__path)
        self.create()
            
    def create(self, columns: list[str] = None) -> None:
        log_columns: list[str] = ["Time", "Title", "Status", "Detail"]
        if(columns):
            log_columns.extend(columns)
        self.__log = dict.fromkeys(log_columns)
        
        for key in self.__log.keys():
            self.__log[key] = {}
        
    def write_info(self, message: str) -> None:
        self.__log["Time"][self.__row] = datetime.now().strftime("%H:%M:%S")
        self.__log["Title"][self.__row] = message
        self.__log["Status"][self.__row] = "OK"
        self.__row += 1
        
    def write_error(self, message: str, detail: str = None) -> None:
        self.__log["Time"][self.__row] = datetime.now().strftime("%H:%M:%S")
        self.__log["Title"][self.__row] = message
        self.__log["Detail"][self.__row] = detail
        self.__log["Status"][self.__row] = "ERROR"
        self.__row += 1
        
    def write_in_column(self, column: str, message: str):
        self.__log[column][self.__row] = message
        
    def close(self):
        dataframe = pd.DataFrame.from_dict(self.__log, orient="index").T
        dataframe.to_excel(f'{self.__path}\\{self.__name}.xlsx')
        
    def __str__(self) -> str:
        return "Log Xlsx"

class SettingService: 
    def __init__(self):
        self.__settings: dict = {}

    @property
    def settings(self) -> dict:
        return self.__settings
        
    @settings.setter
    def settings(self, setting) -> None:
        self.__settings = setting

class SettingBot(SettingService):
    
    def __init__(self) -> None:
        super().__init__()
        self.settings = dict.fromkeys(["key_one"])
        self.settings["key_one"] = "test"
        
    def __str__(self) -> str:
        return "Setting Bot"
        
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
        
    
