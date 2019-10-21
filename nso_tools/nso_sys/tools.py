# -*- coding: utf-8 -*-
from datetime import datetime

class Tools(object):
    def __init__(self, conf):
        self.conf = conf
    
    def synk_from(self, hostname):
        """ 
        Синхронизация NSO от устройства
        hostname:  устройство как они называются в NSO 
        """
        import ncs
        with ncs.maapi.single_write_trans(self.conf.login, self.conf.password) as t:
            root = ncs.maagic.get_root(t)
            start_time = datetime.now()
            try:
                #root.devices.device[hostname].ssh.fetch_host_keys()    # TODO: WTF?
                output = root.devices.device[hostname].sync_from()
                # root.devices.device[device_name].state.admin_state = "southbound-locked" # TODO: WTF?
                
                # Для логирования
                result = output.result
                info = output.info
                
                if output.result == True:
                    t.apply()
                else:
                    pass

            except Exception as e:
                """ На случай непредвиденных обстоятельств """
                result='Exception: '
                info = e

            end_time = datetime.now()
            # stdout log
            print('{} - {} | Hostname: {}, SynkStatus: {}, Info: {}'.format(start_time.strftime("%Y-%m-%d %H:%M:%S"), 
                                                                           end_time.strftime("%H:%M:%S"), 
                                                                           hostname, 
                                                                           result, 
                                                                           info))
            # TODO: Писать в лог файл        
      
    
    def get_device_list(self, keywords):
        """ 
        Вернет список устройств который содержит совпадение по keywords в hostname 
        """
        import ncs
        result = []
        with ncs.maapi.single_read_trans(self.conf.login, 'python', groups=['ncsadmin']) as t:
            root = ncs.maagic.get_root(t)
            devicelist = root.devices.device
            i = 0
            result = []
            for device in devicelist:
                if keywords in device.name:
                    i += 1
                    result.append(device.name)   
            #print(i, result)  # Debug
            return result, i
        