# -*- coding: utf-8 -*-
import sys
class Config():
    """
    Конфигурационный файл
    """
    def __init__(self, nso_path='', login='', password=''):
        """ 
        nso_path:   Путь до NSO Python API в ОС
        login:      NSO логин
        password:   NSO пароль
        """
        
        if nso_path == '':
                print("You must set position argument nso_path='path/to/nso'")
        else:
            self.nso_path = nso_path
            
        if login == '':
            print("You must set position argument login='admin'")
        else:    
            self.login = login
            
            
        if password == '':
            print("You must set position argument password='admin'")
        else:    
            self.password = password


        # Добавляем в PYTHONPATH путь до NSO PyAPI и импортируем NSO 
        sys.path.append(self.nso_path) 
        
       
        
        
    # TODO: геттер сеттер!!!    
    def show():
        """ DEBUG. Информация о конфигурации """
        return "Path: {} \nLogin: {} \nPassord: ".format(self.nso_path, self.login, self.password)