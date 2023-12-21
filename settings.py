from bot_db import *

class SettingService: 
    def __init__(self):
        self.__settings: dict = {}

    @property
    def settings(self) -> dict:
        return self.__settings
        
    @settings.setter
    def settings(self, setting) -> None:
        self.__settings = setting

class BotSetting(SettingService):
    
    __repository: SettingTable
    
    def __init__(self, bot_name: str) -> None:
        super().__init__()
        self.settings = self.get_new_settings()
        self.__repository = SettingTable(bot_name=bot_name, 
                                         setting_name=self.__str__(),
                                         settings=self.settings)
        self.__repository.create()
        self.settings = self.__repository.get()
        
        self.settings = self.__repository.get()
        
    def get_new_settings(self) -> dict:
        setting: dict = dict.fromkeys(['executions', 'good_executions', 'bad_executions'], 0)
        return setting
        
    def update(self) -> None:
        self.__repository.update(data=self.settings)
        
    def __str__(self) -> str:
        return type(self).__name__
    
class TaskManagerSetting(SettingService):
    
    __repository: SettingTable
    
    def __init__(self, bot_name: str):
        super().__init__()
        self.settings = self.get_new_settings()
        self.__repository = SettingTable(bot_name=bot_name, 
                                         setting_name=self.__str__(),
                                         settings=self.settings)
        self.__repository.create()
        self.settings = self.__repository.get()
        
    def get_new_settings(self) -> dict:
        setting: dict = dict.fromkeys(['task_name'])
        setting['task_name'] = 'None'
        return setting
    
    def update(self) -> None:
        self.__repository.update(data=self.settings)
    
    def __str__(self) -> str:
        return type(self).__name__