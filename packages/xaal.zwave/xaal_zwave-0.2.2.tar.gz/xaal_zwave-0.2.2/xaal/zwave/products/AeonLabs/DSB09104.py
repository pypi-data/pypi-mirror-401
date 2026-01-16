from xaal.zwave import core

class DSB09104(core.ZDevice):
    """Aeon Labs Home Energy Meter"""
    
    MANUFACTURER_ID = '0x0086'
    PRODUCTS = ['0x0009:0x0002',]
    
    def setup(self):
        for i in range(0,4):
            power = self.new_device("powermeter.basic")
            power.new_attribute("power")
            # map zwave var to 
            value = 'power_%s' % i
            self.monitor_value(value ,core.COMMAND_CLASS.SENSOR_MULTILEVEL,i+1,4)
            # this device should push update on change, but I'm unable to fix this
            # so polling
            self.gw.engine.add_timer(self.get_value(value).refresh,15)
        
        
    def handle_value_changed(self,value):
        for i in range(0,4):
            tmp = self.get_value('power_%s' % i)
            if tmp == value:
                power = round(value.data)
                if power >=0:
                    self.devices[i].attributes['power'] = power
        
