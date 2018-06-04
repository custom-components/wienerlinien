# custom_component to get info about next departures
![Version](https://img.shields.io/badge/version-1.1.1-green.svg?style=for-the-badge)

A component which allows you to get information about next departure from spesified stop. 

To get started:   
Put `/custom_components/sensor/wienerlinien.py` here:  
`<config directory>/custom_components/sensor/wienerlinien.py`  


You can find out the Stop ID (rbl number) thanks to Matthias Bendel (https://github.com/mabe-at)
https://till.mabe.at/rbl/ 

You can also request your own API key here:
https://www.wien.gv.at/formularserver2/user/formular.aspx?pid=3b49a23de1ff43efbc45ae85faee31db&pn=B0718725a79fb40f4bb4b7e0d2d49f1d1
Mainpage of the API
https://www.data.gv.at/katalog/dataset/add66f20-d033-4eee-b9a0-47019828e698


Example configuration.yaml:  
```yaml
sensor:
  - platform: wienerlinien
    apikey: iuvds8793889dsd
    stops:
      - 4429
      - 3230
```
 #### Sample overview
![Sample overview](overview.png)

This component is using the [Wienerlinien API](http://www.wienerlinien.at) API to get the information.
„Datenquelle: Stadt Wien – data.wien.gv.at“
Lizenz (CC BY 3.0 AT)
