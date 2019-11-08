# -*- coding: utf-8 -*-
from nso_tools.parsers.nso_utils import NsoUtils


class NsoBgpNeighborsParser():
    def __init__(self, conf):
        self.conf = conf        # Получаем доступ к конфигурационному файлу
        
    #def show(self, hostname):
    #    """
    #    Парсер менеджер, в зависимости от типа устройств, отправляет в нужный парсер
    #    после выводит на печать в print() 
    #    """
    #    pass
    
    """
    """
    
    def neighbor_list(self, hostname):
        """ Альтернативное представление show() вернет список набитый dict{} """
        nso_utils = NsoUtils(self.conf)
        software = nso_utils.get_device_family(hostname)
        
        list_of_interfaces = []
        
        if str(software) == 'cisco-ios-xr':
            item = self.__ios_xr_bgp_neighbor(hostname)
            list_of_interfaces += item
                
        elif str(software) == 'cisco-ios':
            item = self.__ios_bgp_neighbor(hostname)
            list_of_interfaces += item
        
        return list_of_interfaces
    
    
    
    
    def __ios_xr_bgp_neighbor(self, hostname):  
        """
        Парсинг interfaces для IOS XR из модели NSO
        hostname: Имя устройства в NSO
        return: list[{interface1}, {interface2}, ...]
        """ 
        import ncs
        with ncs.maapi.Maapi() as m:
            with ncs.maapi.Session(m, self.conf.login, self.conf.password):
                with m.start_read_trans() as t:
                    root = ncs.maagic.get_root(t)
                    
                    # Получаем все BGP из NSO
                    bgp_config = root.devices.device[hostname]['config']['cisco-ios-xr:router']['bgp']['bgp-no-instance']
                    
                    # Список в который добавляем BGP neighbors, который вернется как рузультат работы метода
                    bgp_neighbors = []  
                                
                    for router_as in bgp_config:
                        for vrf in router_as['vrf']:
                            for neighbor in vrf['neighbor']:
                                
                                # BGP - в него собираем остальные элементы
                                bgp = {}
                                
                                # Подготавливаем BFD
                                bfd = {}
                                if neighbor['bfd']['minimum-interval'] is not None:
                                    bfd['min_interval'] = str(neighbor['bfd']['minimum-interval'])
                                    bfd['fast_detect'] = str(neighbor['bfd']['fast-detect'])
                                    bfd['multiplier'] = str(neighbor['bfd']['multiplier'])
                                   
                                # Подготавливаем address-family 
                                af = {}    
                                if neighbor['address-family'] is not None:   
                                    af['address-family'] = str(neighbor['address-family']['ipv4'])
                                    af['type'] = str(neighbor['address-family']['ipv4']['unicast'])
                                      
                                      
                                # Подготавливаем route policy
                                route_policy = {}
                                for rp in neighbor['address-family']['ipv4']['unicast']['route-policy']:
                                    route_policy[str(rp['direction'])] = str(rp['name'])
                                   
                                # Исключаем все не VPN BGP neighbors 
                                if vrf['name'] != 'all':    
                                    #print(router_as['id'], vrf['name'], bgp_atr, route_policy)
                                    bgp['hostname'] = str(hostname)
                                    #bgp['router_as'] = str(router_as['id'])
                                    bgp['vrf'] = vrf['name'].upper()
                                    bgp['neighbor'] = str(neighbor['id'])
                                    
                                    bgp['remote_as'] = str(neighbor['remote-as'])
                                    bgp['local_as'] = str(neighbor['local-as']['as-number'])
                                    bgp['max_prefix'] = str(neighbor['address-family']['ipv4']['unicast']['maximum-prefix']['max-prefix-limit'])
                                    # TODO: BFD, AF, default-originate                                     
                                    bgp['bfd'] = bfd
                                    bgp['af'] = '' # TODO af
                                    #print(neighbor['address-family']['ipv4']['unicast']['default-originate'])
                                    #if str(neighbor['address-family']['ipv4']['unicast']['default-originate']) == 'default-originate':
                                    #    bgp['default'] = str(neighbor['address-family']['ipv4']['unicast']['default-originate'])
                                    #else:
                                    #    bgp['default'] = ''
                                    bgp['default'] = ''
                                    bgp['route_policy'] = route_policy
                                    
                                    bgp_neighbors.append(bgp)
        return bgp_neighbors    
                   
    def __ios_bgp_neighbor(self, hostname):
    #def neighbor_list(self, hostname):
        """
        Парсинг interfaces для IOS из модели NSO
        hostname: Имя устройства в NSO
        return: list[{interface1}, {interface2}, ...]
        """ 
        import ncs
        with ncs.maapi.Maapi() as m:
            with ncs.maapi.Session(m, self.conf.login, self.conf.password):
                with m.start_read_trans() as t:
                    root = ncs.maagic.get_root(t)         
                    
                    # Получаем все BGP из NSO для IOS
                    bgp_config = root.devices.device[hostname]['config']['ios:router']['bgp']
                    
                    # Список в который добавляем BGP neighbors, который вернется как рузультат работы метода
                    bgp_neighbors = []  
                    
                    for router_as in bgp_config:
                        for address_family in router_as['address-family']['with-vrf']['ipv4']:
                            print(address_family) # ipv4 unicast
                            # Подготавливаем BFD
                            bfd = {} # TODO
                            
                            # Подготавливаем address-family 
                            # TODO: BFD, AF, default-orig
                            af = {}   
                            if address_family['af'] == 'unicast':   
                                af['address-family'] = 'ipv4'
                                af['type'] = 'unicast'
                                    
                            for vrf in address_family['vrf']:
                                #print(vrf['name'])  # 3g_data
                                for neighbor in vrf['neighbor']:
                                    
                                    # BGP - в него собираем остальные элементы
                                    bgp = {}
                                    bgp['hostname'] = str(hostname)
                                    bgp['router_as'] = str(router_as['as-no'])
                                    bgp['vrf'] = str(vrf['name']).upper()
                                    bgp['neighbor'] = str(neighbor['id'])
                                    bgp['remote_as'] = str(neighbor['remote-as'])
                                    bgp['local_as'] = neighbor['local-as']['as-no']
                                    bgp['max_prefix'] = str(neighbor['maximum-prefix']['max-prefix-no'])
                                    bgp['max_prefix_thold'] = str(neighbor['maximum-prefix']['threshold']) # Only for IOS
                                    bgp['bfd'] = bfd
                                    bgp['af'] = af
                                    bgp['default'] = str(neighbor['default-originate'])
                                                                        
                                    # Подготавливаем route policy
                                    route_policy = {}
                                    for rp in neighbor['prefix-list']:
                                        route_policy[str(rp['direction'])] = str(rp['prefix-list-name'])
                                    
                                    bgp['route_policy'] = route_policy
                                    
                                    bgp_neighbors.append(bgp)
        return bgp_neighbors
                                    

                        