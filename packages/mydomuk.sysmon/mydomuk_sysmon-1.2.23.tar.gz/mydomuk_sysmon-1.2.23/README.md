# System Monitor

This module reports system performance data to an MQTT server.
Home Assistant Discovery may also be enabled to allow easy setup
for use with Home Assistant

## Installation

This is a PyPi module and can be installed into a dedicated environment
using ```pip install mydomuk.sysmon```

## Usage

A source file is required to allow communication with the MQTT server and for 
the setup of Home Assistant 

In order to create a dummy configuration file call Sysmon as below

```python -m mydomuk.sysmon -cs```

This will output a Source configuration similar to below

```
Jan10 22:21:47 - sysmon[I] - Sysmon Version 1.2.21 running on posix system linux
# Configuration File save this as a .src file and edit it
# ************** START ********************
MQTT_BROKER=127.0.0.1                               # MQTT Broker host name or IP address, required
MQTT_PORT=1883                                      # MQTT Port for connecting to broker, defaults to 1883
MQTT_USER=                                          # MQTT Username for broker, required if using authenticated MQTT Server
MQTT_PASSWORD=                                      # MQTT Password for broker
MQTT_SSL=False                                      # Use SSL True for False for connecting to broker, default False
MQTT_CACERT=                                        # Path to the CA Certficate if using SSL, optional
MQTT_TOPIC_PREFIX=MyDomUK                           # MQTT Topic Prefix, required
MQTT_DEVICE_TOPIC=sysmon/{{hostname}}               # MQTT Device Topic usually include {{hostname}}  in the string, required
MQTT_VIP_TOPIC=                                     # Optional Topic for VIP monitoring
MQTT_VIP_MONIT=                                     # Optional Comma Separated list of VIP NIC names to hostname ownership of
MQTT_NIC_MONIT=                                     # Optional Comma Separated list of NIC names to report IP addresses on
MQTT_DISK_MONIT=                                    # Optional Comma Separated list of name=mountpoint pairs
HASS_TOPIC_PREFIX=homeassistant                     # Homeassistant discovery topic prefix, default homeassistant
HASS_DISCOVERY=True                                 # Discovery on True or False, default True
HASS_DEVICE=MyDomUK Server {{hostname}}             # Homeassistant Device description can include {{hostname}}
HASS_DEVICEID=mydomuk_sysmon_{{hostname}}           # Homeassistant unique Device can include {{hostname}}
HASS_MANUFACTURER=Server Manufacturer               # Homeassistant Device manufacturer
HASS_MODEL=Server Model                             # Homeassistant Device model information
PUBLIC_IP_CHECK=False                               # Change to True to Get Public IP V4 Address
PUBLIC_IPV6_CHECK=False                             # Change to True to Get Public IP V6 Address   
PUBLIC_IP_SITES=                                    # Allow overriding the internal set of Public IP Check URLs
PUBLIC_IPV6_SITES=                                  # Allow overriding the internal set of Public IP Check URLs
# ************** ENDS  ********************
```

Copy this and edit it into a local file and then start sysmon using
```python -m mydomuk.sysmon -src sourcefilename```

To see a list of command line options simply run
```python -m mydomuk.sysmon -h```
