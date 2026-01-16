xAAL Netatmo Weather Station Gateway
=====================================

This package provides an xAAL gateway for Netatmo Weather Station devices, allowing you to integrate your Netatmo weather data into the xAAL home automation ecosystem.

Features
--------

* **OAuth 2.0 Authentication**: Modern authentication with automatic token refresh
* **Multi-module Support**: Main indoor station and all additional modules
* **Real-time Data**: Weather data updated every 5 minutes
* **Auto-discovery**: Automatic detection and configuration of Netatmo modules
* **Debug Mode**: Optional verbose logging for troubleshooting

Supported Devices
-----------------

* **NAMain**: Main indoor station (temperature, humidity, pressure, CO2, noise, WiFi)
* **NAModule1**: Outdoor module (temperature, humidity, battery)
* **NAModule2**: Wind gauge (wind strength, angle, gusts, battery)
* **NAModule3**: Rain gauge (rain measurement, battery)
* **NAModule4**: Additional indoor module (temperature, humidity, CO2, battery)


Configuration
-------------

Edit ~/.xaal/xaal/netatmo.ini with your Netatmo credentials 


Getting OAuth Tokens
--------------------

1. Go to https://dev.netatmo.com/apps
2. Create an application or use existing one
3. Generate access and refresh tokens
4. Copy them to your configuration file

Architecture
------------

The gateway consists of:

* **TokenManager**: Handles OAuth 2.0 tokens with automatic refresh
* **API**: Netatmo API client with optimized token usage
* **Gateway**: Main xAAL device management
* **Modules**: Individual sensor modules for each Netatmo device

Troubleshooting
---------------

**No data received**:
1. Check internet connection
2. Verify Netatmo station is online
3. Validate OAuth tokens are correct
4. Enable debug mode: ``debug = True``

**Token errors**:
1. Regenerate tokens from Netatmo developer portal
2. Update configuration file
3. Restart the gateway

**Module not detected**:
1. Ensure module is paired with main station
2. Check module battery
3. Verify RF signal strength

License
-------

GPL v3 License - see LICENSE file for details.
