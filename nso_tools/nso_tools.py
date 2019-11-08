# -*- coding: utf-8 -*-

"""
Набот инструментов для работы с NSO
Инструкция в README.md
"""

from nso_tools.settings.config import Config
from nso_tools.nso_sys.tools import Tools
from nso_tools.parsers.interfaces import NsoInterfaceParser
from nso_tools.parsers.vrf import NsoVrfParser
from nso_tools.parsers.nso_utils import NsoUtils
from nso_tools.parsers.bgp_neighbors import NsoBgpNeighborsParser
from nso_tools.parsers.static_route import NsoStaticrouteParser

class NsoTools(object):
     
    def __init__(self, nso_path, login, password):
        self.conf = Config(nso_path, login, password)
        
        # Передаем объект для конфигурации внутренних классов
        self.nso_utils = NsoUtils(self.conf) 
        self.interfaces = NsoInterfaceParser(self.conf)
        self.vrf = NsoVrfParser(self.conf)
        self.tools = Tools(self.conf)
        self.bgp = NsoBgpNeighborsParser(self.conf)
        self.static = NsoStaticrouteParser(self.conf)

        

