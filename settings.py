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