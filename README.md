NSO Tools
-

Tools for fast get information from Cisco NSO


[More example](https://github.com/NSO-developer/nso-5-day-training/blob/master/nso_python_api_examples.py)

# How to use

```bash
pipenv install -e git+https://github.com/yuryrunx/nso_tools.git#egg=nso_tools
```

```python
from nso_tools import NsoTools
nt = NsoTools(nso_path='{path/to}/src/ncs/pyapi/', login='admin', password='admin')

# Tools

nt.tools.synk_from(hostname)            # stdout. Синхронизирует NSO устройства от реального девайса. Выведет лог в stdout
nt.tools.get_device_list(keywords)      # return. Вернет две переменные. Список устройств, у которых keywords входит в Hostname, колличество устройств.
# Interface
nt.interfaces.show(hostname)            # stdout. Вернет все интерфейсы на устройстве (hostname)
nt.interfaces.list_interfaces(hostname) # Вернет list=[] содержащий dict={}. [{interface='', vrf='', ipaddres=''}, {}, {}]
# VRF
nt.vrf.show(hostname)                   # stdout. Вернет все VRF на устройстве (hostname)
nt.vrf.list_vrfs(hostname)              # Вернет list=[] содержащий dict={}. [{name='', import='', export=''}, {}, {}]
# BGP neighbors (into VRF)
nt.bgp.neighbor_list(hostname)          # Вернет list=[] содержащий dict={}. 
# L3VPN static routes
nt.static.routes(hostname)              # Вернет list=[] содержащий dict={}.
```




# TODO:
- tests

# ChangeLog

- 08.11.19 - IOS Po subinterfaces parser added
- 08.11.19 - `nt.static.routes(hostname)` method added
- 08.11.19 - `nt.bgp.neighbor_list(hostname)` method added
- 23.10.19 - `nt.interfaces.list_interfaces(hostname)` method added
- 22.10.19 - `nt.vrf.list_vrfs(hostname)` method added
- 21.10.19 - `setup.py` added
- 18.10.19 - Release

---
## VRF list
`nt.vrf.list_vrfs(hostname)`      

Список из словарей с ключами

```python
{
    
    'hostname' = 'PE01'
    'vrf_name' = 'MY_FAVORIT_VRF'
    'rd' = 'N/A' # TODO
    'rt_import' = ['65001:1', '65002:2' , '65003:3']
    'rt_export' = ['65001:1', '65002:2']
    'description' = 'don`t touch me'
}
```

## BGP neighbors (into VRF)

`nt.bgp.neighbor_list(hostname)`         

Вернет список из словарей с ключами: 

**XR:**	
```python
{
    'router_as': '',
    'vrf': '',
    'neighbor': '',
    'remote_as': '',
    'local_as': '',
    'max_prefix': '',
    'bfd': 
        {
            'min_interval': '', 
            'fast_detect': '', 
            'multiplier': ''
        }, 
    'af':  
        {
            'address-family': '', 
            'type': ''
        },
    'default': '',  # TODO
    'route_policy': 
        {
            'in': '',
            'out': ''
        },
}
```	


**IOS:** 	
```python
{
    'router_as': '',
    'vrf': '',
    'neighbor': '',
    'remote_as': '',
    'local_as': '',
    'max_prefix': '',
    'max_prefix_thold': '',     # Only for IOS
    'bfd':  {}                    
        #{                       # TODO 
        #    'min_interval': '', # TODO 
        #    'fast_detect': '',  # TODO 
        #    'multiplier': ''    # TODO 
        #},                      # TODO 
    'af':  
        {
            'address-family': '', 
            'type': ''
        },
    'default': '',  # TODO
    'route_policy': 
        {
            'in': '',
            'out': ''
        },
}
```	

## 

`nt.static.routes(hostname)`

Вернет список из словарей с ключами: 

**XR:**
```python 
[
    {
        'network': '183.12.3.32/32', 
        'interface': 'Te0/0/0/1.100', 
        'next_hop': '183.12.0.1', 
        'description': 'to Infinity'
    },
    ...
]
```

**IOS:** 
```python
{
    'network': '10.10.173.0/27', 
    'interface': 'GigabitEthernet1/27.20', 
    'next_hop': '10.10.173.35', 
    'description': '' # TODO.
    }
```