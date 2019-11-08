# -*- coding: utf-8 -*-
""" 
Парсинг NSO объектов для получения информации о интерфейсах, vrf и т.д.
После парсинга, кладем в БД Nethead
"""


from nso_tools import NsoTools
nt = NsoTools(nso_path='~/MSN/nso_msn_moscow/src/ncs/pyapi/', login='admin', password='admin')
            
            
if __name__ == '__main__':
    for i in nt.bgp.neighbor_list('MSN_77_100100_11'):
        print(i)
    #nt.bgp.neighbor_list('MSN_95_001_1')