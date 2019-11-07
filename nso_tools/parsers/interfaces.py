# -*- coding: utf-8 -*-
from nso_tools.parsers.nso_utils import NsoUtils


class NsoInterfaceParser():
    """
    Парсинг интерфейсов из NSO
    Запуск:
    ifint = NsoInterfaceParser()
    ifint.run([list_devivces])
    """    
    def __init__(self, conf):
        self.conf = conf # Получаем доступ к конфигурационному файлу
        
    
        
    def show(self, hostname):
        """
        Парсер менеджер, в зависимости от типа устройств, отправляет в нужный парсер
        после выводит на печать в print() 
        """
        nso_utils = NsoUtils(self.conf)
        software = nso_utils.get_device_family(hostname)
        
        if str(software) == 'cisco-ios-xr':
            item = self.__ios_xr_intf(hostname)
            self.__print_csv(item) # csv
                
        elif str(software) == 'cisco-ios':
            item = self.__ios_intf(hostname)
            self.__print_csv(item) # csv
            
    def list_interfaces(self, hostname):
        """ Альтернативное представление show() вернет список набитый dict{} """
        nso_utils = NsoUtils(self.conf)
        software = nso_utils.get_device_family(hostname)
        
        list_of_interfaces = []
        
        if str(software) == 'cisco-ios-xr':
            item = self.__ios_xr_intf(hostname)
            list_of_interfaces += item
                
        elif str(software) == 'cisco-ios':
            item = self.__ios_intf(hostname)
            list_of_interfaces += item
        
        return list_of_interfaces
    
                        
                    
    def __ios_xr_intf(self, hostname):    
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
                    # xpath в nso к списку нужных интерфейсов 
                    be_subif_list = root.devices.device[hostname]['config']['cisco-ios-xr:interface']['Bundle-Ether-subinterface']['Bundle-Ether']
                    te_subif_list = root.devices.device[hostname]['config']['cisco-ios-xr:interface']['TenGigE-subinterface']['TenGigE']
                    gi_subif_list = root.devices.device[hostname]['config']['cisco-ios-xr:interface']['GigabitEthernet-subinterface']['GigabitEthernet']
                    
                    hu_list = root.devices.device[hostname]['config']['cisco-ios-xr:interface']['HundredGigE']
                    te_list = root.devices.device[hostname]['config']['cisco-ios-xr:interface']['TenGigE']
                    gi_list = root.devices.device[hostname]['config']['cisco-ios-xr:interface']['GigabitEthernet']
                    lo_list = root.devices.device[hostname]['config']['cisco-ios-xr:interface']['Loopback']
                    bvi_list = root.devices.device[hostname]['config']['cisco-ios-xr:interface']['BVI']
                    
                    # Регистрируем 
                    interface_range = [be_subif_list, te_subif_list, gi_subif_list, hu_list, te_list, gi_list, lo_list]
                    
                    # Список в который добавляем интерфейсы, который вернется как рузультат работы метода
                    device_interfaces = []    
                    
                    for interfaces in interface_range:
                        for i in interfaces:
                            intif = {}
                            intif['hostname'] = str(hostname)
                            intif['intif_name'] = str(i)
                            intif['intif_id'] = str(i['id'])
                            # Vlans временно выключены, т.к нет реализации для IOS
                            #if i['encapsulation']['dot1q']['vlan-id']:
                            #    for vlan in i['encapsulation']['dot1q']['vlan-id']:
                            #        intif['vlan'] = str(vlan)
                            #else:
                            #    intif['vlan'] = 'None'
                            intif['vrf'] = str(i['vrf'])
                            intif['ipv4'] = str(i['ipv4']['address']['ip'])
                            intif['mask'] = str(i['ipv4']['address']['mask'])
                            
                            if i['ipv6']['address']['prefix-list']:
                                for ipv6_pl in i['ipv6']['address']['prefix-list']:
                                    intif['ipv6'] = str(ipv6_pl['prefix'])
                            else:
                                intif['ipv6'] = 'None'
                            # ipv4 еще не готов
                            #if i['ipv4']['address-secondary-list']
                            #    for ipv4_sec_list  in i['ipv4']['address-secondary-list']['address']:
                            #        ipv4_secondary = str(ipv4_sec_list['ip'])
                            #else:
                            #    ipv4_secondary = 'None'
                            
                            intif['description'] = str(i['description'])
                            intif['service_policy_input'] = str(i['service-policy']['input']['name'])
                            intif['service_policy_output'] = str(i['service-policy']['output']['name'])
                            intif['mtu'] = str(i['mtu'])
                            intif['qos_trust'] = 'XR_ParserNotRealised'
                            
                            device_interfaces.append(intif)
                            #print(intif)
                    #print(intif)
                    return device_interfaces
           
    def __ios_intf(self, hostname):
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
                    # xpath в nso к списку нужных интерфейсов                 
                    lo_list = root.devices.device[hostname]['config']['ios:interface']['Loopback']
                    vlan_list = root.devices.device[hostname]['config']['ios:interface']['Vlan'] 
                    po_list = root.devices.device[hostname]['config']['ios:interface']['Port-channel']
                    gi_list = root.devices.device[hostname]['config']['ios:interface']['GigabitEthernet']
                    te_list = root.devices.device[hostname]['config']['ios:interface']['TenGigabitEthernet']
                    
                    # Регистрируем 
                    interface_range = [vlan_list, lo_list, po_list, gi_list, te_list]
                    
                    # Список в который добавляем интерфейсы, который вернется как рузультат работы метода
                    device_interfaces = []    
   
                    for interfaces in interface_range:
                        for term in interfaces:
                            intif = {}
                            intif['hostname'] = str(hostname)
                            intif['intif_name'] = str(term)
                            intif['intif_id'] = str(term['name'])
                            # Vlans временно выключены, т.к нет реализации для IOS
                            #if term['encapsulation']['dot1Q']['vlan-id']:
                            #    for vlan in term['encapsulation']['dot1q']['vlan-id']:
                            #        intif['vlan'] = str(vlan)
                            #else:
                            #    intif['vlan'] = 'None'
                            intif['vrf'] = str(term['ip-vrf']['ip']['vrf']['forwarding'])
                            intif['ipv4'] = str(term['ip']['address']['primary']['address'])
                            intif['mask'] = str(term['ip']['address']['primary']['mask'])
                            intif['ipv6'] = 'IOS_ParserNotRealised'
                            intif['description'] = str(term['description'])
                            intif['service_policy_input'] = str(term['service-policy']['input']) 
                            intif['service_policy_output'] = str(term['service-policy']['output'])
                            intif['mtu'] = str(term['mtu'])
                            
                            if term['mls']['qos']['trust']['dscp']:
                                intif['qos_trust'] = str(term['mls']['qos']['trust']['dscp']) 
                            elif term['mls']['qos']['vlan-based']:
                                intif['qos_trust'] = str(term['mls']['qos']['vlan-based']) 
                            else:
                                intif['qos_trust'] = 'None' 
                            device_interfaces.append(intif)
                    return device_interfaces
        
                    
    def __print_csv(self, interfaces):
        """
        Пишем в консоль в формате csv (via ;)
        """
        #print(vrfs)
        print('Hostname; IfName; IfId; VRF; ipv4; Mask; ipv6; Description; ServicePoliciIn; ServicePolicyOut; MTU; QosTrust')
        for i in interfaces:
            print('{}; {}; {}; {}; {}; {}; {}; {}; {}; {}; {}; {}'.format(i['hostname'],
                                                                    i['intif_name'], 
                                                                    i['intif_id'], 
                                                                    #i['vlan'], 
                                                                    i['vrf'], 
                                                                    i['ipv4'],
                                                                    i['mask'],
                                                                    i['ipv6'],
                                                                    i['description'],
                                                                    i['service_policy_input'],
                                                                    i['service_policy_output'],
                                                                    i['mtu'],
                                                                    i['qos_trust'],
                                                                    ))

                   

#if __name__ == "__main__":
#    
#    si = NsoInterfaceParser()
#    software = si.get_device_family('MSN_11_0005_4')
#    #print(software)
#    devices = ['MSN_11_0005_1', 'MSN_11_0005_2', 'MSN_11_0005_4']
#    for device in devices:
#        si.run(device)
#    #sys.exit(pasrser.main(category_id=5))