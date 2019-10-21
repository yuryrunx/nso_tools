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
nt.tools.get_device_list(keywords)      # return. Вернет список устройств, у которых keywords входит в Hostname 
nt.interfaces.show(hostname)            # stdout. Вернет все интерфейсы на устройстве (hostname)
nt.vrf.show(hostname)                   # stdout. Вернет все VRF на устройстве (hostname)
```


# TODO:
- tests

# ChangeLog

- 21.10.19 - Setup added
- 18.10.19 - Release
