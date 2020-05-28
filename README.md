[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

### Description

This App will dim your lights for **X** minutes until it's finally off.

### Requirements

You need an [Xiaomi Mijia Smart Switch](https://www.banggood.com/Original-Xiaomi-Mijia-Smart-Home-Zig-bee-Wireless-Smart-Switch-Touch-Button-ON-OFF-WiFi-Remote-Control-Switch-p-1049175.html?rmmds=buy&cur_warehouse=HK). I think it will work with others too as long as they have two different event codes and the event comes via deconz.

### Device Events

| Action           | Code     | Description    |
| -------------- | -------- | -------------- |
| SINGLE_CLICK   | 1002     | start diming   |
| DOUBLE_CLICK   | 1004     | stop diming    |

### Configuration

This is an example for your `apps.yaml` following entries are possible:
* module (required)
* class (required)
* light_ids (required) - comma separated if you which more lights to be controlled
* switch_id (required)
* switch_single_click_event_code (optional) - single click event code
* switch_double_click_event_code (optional) - double click event code
* durationInSeconds (optional) - default are 120 seconds
* start_birghtness (optional) - an integer which can go from 0 to 254. While 0 means off and 254 means maximum
```
goodnightt:
  module: Goodnight
  class: Goodnight
  light_ids: light.osramlightbedroom,light.osramlightstrip02
  switch_id: round02
  switch_single_click_event_code: 1002
  switch_double_click_event_code: 1004
  durationInSeconds: 600 # 10 min (default 120 - 2min)
  start_brightness: 254
```