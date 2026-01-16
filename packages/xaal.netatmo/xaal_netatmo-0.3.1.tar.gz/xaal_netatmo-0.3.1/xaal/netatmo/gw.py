from xaal.lib import tools, Device, helpers

from . import netatmo
import platform
import logging

RATE = 300 # update every 5 min
PACKAGE_NAME = "xaal.netatmo"
logger = logging.getLogger(PACKAGE_NAME)




class GW:
    def __init__(self,engine):
        filename=tools.get_cfg_filename(PACKAGE_NAME)
        self.cfg=tools.load_cfg_file(filename)
        self.eng = engine
        self.modules=[]
        self.setup()
        self.read_weather_stations()
         
    def setup(self):
        # check config file
        config=netatmo.ConfigParser(self.cfg)    
        config.update()

        # load modules from confile file
        self.load_modules_config()

        # GW 
        gw            = Device("gateway.basic")
        gw.address    = tools.get_uuid(self.cfg['config']['addr'])
        gw.vendor_id  = "NETATMO"
        gw.product_id = "Netatmo Weather Station"
        gw.info       = "%s@%s" % (PACKAGE_NAME,platform.node())
        gw.url        = "https://dev.netatmo.com/"
        gw.version    = 0.2
        self.eng.add_device(gw)

        # embedded
        emb = gw.new_attribute('embedded',[]).value
        for mod in self.modules :
            for gw in mod.sensors:
                self.eng.add_device(gw)
                emb.append(gw.address)

        self.eng.add_timer(self.read_weather_stations,RATE)


    def load_modules_config(self):
        """init all modules"""
        assert self.cfg
        devices=self.cfg["devices"]
        for _id,value in devices.items():
            group=tools.get_uuid(value["group_addr"])
            addr=tools.get_uuid(value["base_addr"])
            if value["type"]=="NAMain":
                sensors_type=["thermometer","hygrometer","barometer","co2meter","soundmeter","wifimeter"]
            elif value["type"]=="NAModule1":  # addition outdoor
                sensors_type=["thermometer","hygrometer","radiometer","battery"]
            elif value["type"]=="NAModule4":  #additional indoor
                sensors_type=["thermometer","hygrometer","co2meter","radiometer","battery"]
            elif value["type"]=="NAModule2":  # additon wind gauge
                sensors_type=["windgauge","radiometer","battery"]
            elif value["type"]=="NAModule3":  # addition rain gauge
                sensors_type=["rainmeter","radiometer","battery"]
            else:
                logger.warning("invalid modules!!!")

            module=netatmo.NAModule(addr,group,_id,value['type'])
            module.new_sensors(sensors_type) 
            self.modules.append(module)

    def update_modules(self,macId,attr):
        for m in self.modules :
            if m.macId == macId :
                m.update_sensors(attr)   

    @helpers.spawn
    def read_weather_stations(self):
        netatmo_data = netatmo.API(self.cfg).get_data()
        if netatmo_data is None:
            logger.warning("Unable to read getstationsdata")
            return
        main_indoor = netatmo_data["devices"][0] # dic
        netatmo_modules= main_indoor["modules"] # list

        try:# main indoor
            macId=main_indoor["_id"]
            attr={}
            data = main_indoor["dashboard_data"]
            attr["rssi"] = main_indoor["wifi_status"]            
            attr["temperature"] = data["Temperature"]
            attr["humidity"]    = data["Humidity"]
            attr["pressure"]    = data["Pressure"]
            attr["co2"]         = data["CO2"]
            attr["sound"]       = data["Noise"]

            self.update_modules(macId,attr)
        except Exception as e:
            logger.warning(e)

        try: # update modules
            logger.info("update additional modules")
            for m in netatmo_modules :     
                macId=m["_id"]
                attr={"radio_status": m["rf_status"],
                     "level": m["battery_percent"]}
                data =m.get('dashboard_data',None)
                if not data:
                    logger.warning('Not data from %s' % macId)
                    continue
                try :
                    # addition outdoor
                    if m["type"]=="NAModule1": 
                        attr["temperature"]= data["Temperature"]
                        attr["humidity"]   = data["Humidity"]

                    # additon wind gauge
                    elif m["type"]=="NAModule2":
                        # in API we can also get history of wind, here we don't
                        attr["windstrength"] = data["WindStrength"]
                        attr["windangle"]    = data["WindAngle"]
                        attr["guststrength"] = data["GustStrength"]
                        attr["gustangle"]    = data["GustAngle"]

                    # addition rain gauge
                    elif m["type"]=="NAModule3" : 
                        attr["rain"]=  data["Rain"]

                    #additional indoor 
                    elif m["type"]=="NAModule4" : 
                        attr["temperature"] = data["Temperature"]
                        attr["humidity"]    = data["Humidity"]
                        attr["co2"]         = data["CO2"]
                    else :
                        logger.warning("invalid netatmo module type !!! =>%s" % m["type"])
               
                    self.update_modules(macId,attr)
                except:
                    logger.warning("addition module update failed macId=%s"%macId)

        except Exception as e:
            logger.warning(e)
            logger.warning("Something goes wrong in __readweatherstation")


def setup(engine):
    GW(engine)
    return True

