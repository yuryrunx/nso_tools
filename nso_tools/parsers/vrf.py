# -*- coding: utf-8 -*-
from nso_tools.parsers.nso_utils import NsoUtils


class NsoVrfParser():
    """
    Парсинг VRF
    """
    def __init__(self, conf):
        self.conf = conf # Получаем доступ к конфигурационному файлу


    def show(self, hostname):
        """
        Парсер менеджер, в зависимости от типа устройств, отправляет в нужный парсер
        после выводит в print() 
        """
        nso_utils = NsoUtils(self.conf)
        software = nso_utils.get_device_family(hostname)   
        
        if str(software) == 'cisco-ios-xr':
            item = self.__ios_xr_vrf(hostname)
            self.__print_csv(item) # csv
                
        elif str(software) == 'cisco-ios':
            item = self.__ios_vrf(hostname)
            self.__print_csv(item) # csv
           

    def __ios_xr_vrf(self, hostname):       
        """
        Парсинг VRF для IOS XR из модели NSO
        hostname: Хостнейм устройства в БД NSO
        return: list[{dev1}, {dev2}, ...]
        """ 
        import ncs
        with ncs.maapi.Maapi() as m:
            with ncs.maapi.Session(m, self.conf.login, self.conf.password):
                with m.start_read_trans() as t:
                    root = ncs.maagic.get_root(t)
                    vrf_list = root.devices.device[hostname]['config']['cisco-ios-xr:vrf']['vrf-list']
            
                    vrfs = []
                    
                    for vrf in vrf_list:
                        # Dict для каждого отдельного vrf
                        set_vrf = {}
                        set_vrf['hostname'] = str(hostname)
                        set_vrf['vrf_name'] = vrf['name']
                        # RD. Пока не работает...
                        #ios_xr_rd(vrf['name'])
                        set_vrf['rd'] = 'N/A'
                        # RT Import
                        set_vrf['rt_import'] = self.__rt_nso_xr(vrf['address-family']['ipv4']['unicast']['import']['route-target']['address-list'])
                        # RT Export
                        set_vrf['rt_export'] = self.__rt_nso_xr(vrf['address-family']['ipv4']['unicast']['export']['route-target']['address-list'])
                        set_vrf['description'] = vrf['description']
                        vrfs.append(set_vrf)
                    return vrfs
                
    def __ios_vrf(self, hostname): 
        """
        Парсинг VRF для IOS из модели NSO
        hostname: Хостнейм устройства в БД NSO
        return: list[{dev1}, {dev2}, ...]
        """    
        import ncs    
        with ncs.maapi.Maapi() as m:
            with ncs.maapi.Session(m, self.conf.login, self.conf.password):
                with m.start_read_trans() as t:
                    root = ncs.maagic.get_root(t)
                    vrf_list = root.devices.device[hostname]['config']['ios:ip']['vrf']
                    vrfs = []
                    for vrf in vrf_list:
                        set_vrf = {}
                        set_vrf['hostname'] = str(hostname)
                        set_vrf['vrf_name'] = vrf['name']
                        # RD
                        set_vrf['rd'] = vrf['rd']
                        # RT import
                        set_vrf['rt_import'] = self.__rt_nso_ios(vrf['route-target']['import'])
                        # RT export
                        set_vrf['rt_export'] = self.__rt_nso_ios(vrf['route-target']['export'])
                        # Description
                        set_vrf['description'] = vrf['description']
                        vrfs.append(set_vrf)
                    return vrfs
                
    def __rt_nso_xr(self, vrfs): 
        """ Парсим RT для IOS """
        rt_list = []
        for rt in vrfs:
            rt_list.append(rt['name'])
            
        if len(rt_list) == 0:
            rt_list.append('N/A')
            
        return rt_list


    def __rt_nso_ios(self, vrfs): # list
        """ Парсим RT для IOS XR """
        rt_list = []
        for rt in vrfs:
            rt_list.append(rt['asn-ip'])
            
        if len(rt_list) == 0:
            rt_list.append('N/A')
            
        return rt_list


    def __print_csv(self, vrfs):
        """
        Пишем в консоль с csv формате
        """
        #print(vrfs)
        for i in vrfs:
            print('{}; {}; {}; {}; {}'.format(i['hostname'], i['vrf_name'], i['rt_import'], i['rt_export'], i['description']))

      

