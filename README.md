# custom_component to get info about next departures.
  
![Version](https://img.shields.io/badge/version-component_version'
'1.1.1'
COMPONENT_VERSIO-green.svg?style=for-the-badge) ![mantained](https://img.shields.io/maintenance/yes/2018.svg?style=for-the-badge)   
A platform which allows you to get information about next departure from spesified stop. 
  
To get started put `/custom_components/sensor/wienerlinien.py` here:  
`<config directory>/custom_components/sensor/wienerlinien.py`  
  
**Example configuration.yaml:**
```yaml
sensor:
  platform: wienerlinien
  apikey: 2190400
  stops:
    - '4429'
    - '3230'
```
**Configuration variables:**  
  
key | description  
:--- | :---  
**platform (Required)** | The platform name.  
**apikey (Required)** | Your API key from wien.gv.at.  
**stops (Required)** | RBL stop ID's  
  
#### Sample overview
![Sample overview](overview.png)
  
You can find out the Stop ID (rbl number) thanks to [Matthias Bendel](https://github.com/mabe-at) [https://till.mabe.at/rbl/](https://till.mabe.at/rbl/)
You can also request your own API key [here](https://www.wien.gv.at/formularserver2/user/formular.aspx?pid=3b49a23de1ff43efbc45ae85faee31db&pn=B0718725a79fb40f4bb4b7e0d2d49f1d1)
[Mainpage of the API](https://www.data.gv.at/katalog/dataset/add66f20-d033-4eee-b9a0-47019828e698)  
This platform is using the [Wienerlinien API](http://www.wienerlinien.at) API to get the information.
'Datenquelle: Stadt Wien – data.wien.gv.at'
Lizenz (CC BY 3.0 AT)  
***
Due to how `custom_componentes` are importerd, it is normal to see a `ModuleNotFoundError` error on first boot after adding this, to resolve it, restart Home-Assistant.