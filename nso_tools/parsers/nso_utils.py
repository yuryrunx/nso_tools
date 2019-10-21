# -*- coding: utf-8 -*-

class NsoUtils(object):
    """
    Все, что не попадает в другие разделы
    """
    def __init__(self, config):
        self.conf = config
    
    def get_device_family(self, hostname):
        """ Вернет тип устройства XR, IOS """
        import ncs
        with ncs.maapi.Maapi() as m:
            with ncs.maapi.Session(m, self.conf.login, self.conf.password):
                with m.start_read_trans() as t:
                    root = ncs.maagic.get_root(t)
                    software = root.devices.device[hostname]['device-type']['cli']['ned-id']    # Вернет  ['cisco-ios-xr-id', 'cisco-ios-xr'] /  ios-id:cisco-ios
                    software = software.split(":")    
                    return software[1] # Возвращаем cisco-ios-xr / cisco-ios
                
               
