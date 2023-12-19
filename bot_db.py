import sqlite3

class BotDB:
    
    def __init__(self, bot_name: str) -> None:
        self.__bot_name: str = bot_name
    
    def connect(self) -> None:
        self.connection = sqlite3.connect(f'{self.__bot_name}.bd')
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        
    def create(self) -> None: raise NotImplementedError
    def insert(self) -> None: raise NotImplementedError
    def get(self) -> dict: raise NotImplementedError
    def update(self, data: dict) -> None: raise NotImplementedError

class SettingTable(BotDB):
    def __init__(self, bot_name: str, setting_name: str, settings: dict) -> None:
        super().__init__(bot_name=bot_name)
        self.__setting_table: str = setting_name
        self.__settings: dict = settings 
    
    def create(self) -> None:
        self.connect()

        columns = ''
        for key, value in self.__settings.items():
            column_type = ''
            if(type(value) is str):
                column_type = 'VARCHAR'
            elif(type(value) is int):
                column_type = 'INTEGER'
                
            columns += f'{key} {column_type} NOT NULL,'
        
        query = f'''CREATE TABLE IF NOT EXISTS {self.__setting_table} ({columns[:-1]});'''
                
        self.cursor.execute(query)
        
        self.connection.commit()
        self.connection.close()
        
        if(not self.get()): self.insert() 
    
    def insert(self) -> None:
        self.connect()
        keys: list[str] = self.__settings.keys()
        items: list[str] = ['?'] * len(keys)
        query = f'''INSERT INTO {self.__setting_table} ({','.join(keys)}) VALUES ({','.join(items)})'''
        self.cursor.execute(query, tuple(self.__settings.values()))
        self.connection.commit()
        self.connection.close()
    
    def get(self) -> dict:
        self.connect()
        query = f'SELECT * FROM {self.__setting_table} WHERE ROWID = 1'
        data = self.cursor.execute(query).fetchone()
        self.connection.commit()
        self.connection.close()
        if(data != None): return dict(data)
        else: return dict() 
    
    def update(self, data: dict) -> None:
        self.connect()
        
        columns = ''
        for key in self.__settings.keys():
            columns += f'{key} = ?,'
            
        query = f'''UPDATE {self.__setting_table} SET {columns[:-1]} WHERE ROWID = 1'''
        self.cursor.execute(query, tuple(data.values()))
        
        self.connection.commit()
        self.connection.close()