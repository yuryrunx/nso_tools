# -*- coding: utf-8 -*-
from nso_tools.parsers.nso_utils import NsoUtils
import re

class NsoStaticrouteParser():
    def __init__(self, conf):
        self.conf = conf        # Получаем доступ к конфигурационному файлу
        
    
    def routes(self, hostname):
        """ Альтернативное представление show() вернет список набитый dict{} """
        nso_utils = NsoUtils(self.conf)
        software = nso_utils.get_device_family(hostname)
        
        list_of_interfaces = []
        
        if str(software) == 'cisco-ios-xr':
            item = self.__ios_xr_static_route(hostname)
            
            list_of_interfaces += item
                
        elif str(software) == 'cisco-ios':
            item = self.__ios_static_route(hostname)
            list_of_interfaces += item
        
        return list_of_interfaces
    
    
    def __ios_xr_static_route(self, hostname):
        """ Парсим static route для XR """
        import ncs
        
        with ncs.maapi.Maapi() as m:
            with ncs.maapi.Session(m, self.conf.login, self.conf.password):
                with m.start_read_trans() as t:
                    root = ncs.maagic.get_root(t)
                    route_list = []
                    # Получаем все Static Routes из NSO
                    for vrf in root.devices.device[hostname]['config']['cisco-ios-xr:router']['static']['vrf']:
                        for route in vrf['address-family']['ipv4']['unicast']['routes']:
                            
                            static_route = {}
                            static_route['hostname'] = str(hostname)
                            static_route['vrf'] = str(vrf['name']).upper()
                            static_route['network'] = str(route['net'])
                            static_route['interface'] = str(route['interface'])
                            static_route['next_hop'] = str(route['address'])
                            static_route['description'] = str(route['description'])
                                             
                        route_list.append(static_route)
        return route_list    
    
    
    def __ios_static_route(self, hostname):
        """ Парсим static route для IOS """
        import ncs
        
        with ncs.maapi.Maapi() as m:
            with ncs.maapi.Session(m, self.conf.login, self.conf.password):
                with m.start_read_trans() as t:
                    root = ncs.maagic.get_root(t)
                    route_list = []
                    # Получаем все Static Routes из NSO
                    for vrf in root.devices.device[hostname]['config']['ios:ip']['route']['vrf']:
                        for route in vrf['ip-route-interface-forwarding-list']:
                            static_route = {}
                            
                            mask = self.__bit_mask(route['mask'])
                            
                            static_route['hostname'] = str(hostname)
                            static_route['vrf'] = str(vrf['name']).upper()
                            static_route['network'] = str(route['prefix']) + '' + mask 
                            static_route['interface'] = str(route['interface'])
                            static_route['next_hop'] = str(route['forwarding-address'])
                            static_route['description'] = ''
                            
                            route_list.append(static_route)
        return route_list 
    
    
    def __bit_mask(self, netmask):
        """ Принимает десятичную маску, возвращает битовую"""
        bit_mask_list = re.findall(r"[0-2][0-9][0-9]\.[0-2][0-9][0-9]\.[0-2][0-9][0-9]\.0|[0-9][0-5][0-9]\.[0-2][0-9][0-9]\.[0-2][0-9][0-9]\.[0-2][0-9][0-9]", netmask)                             
        if len(bit_mask_list) != 0:
            bit_mask = sum([bin(int(x)).count("1") for x in bit_mask_list[0].split(".")])
            return "/{}".format(bit_mask)
        else:
            return netmask