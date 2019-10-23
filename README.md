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
```


# TODO:
- tests

# ChangeLog

- 23.10.19 - `nt.interfaces.list_interfaces(hostname)` method added
- 22.10.19 - `nt.vrf.list_vrfs(hostname)` method added
- 21.10.19 - `setup.py` added
- 18.10.19 - Release
