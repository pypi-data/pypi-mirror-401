from xaal.zwave import core

class ZW096(core.ZDevice):
    """ Fibaro FGWPE/F Wall Plug"""
    
    MANUFACTURER_ID = '0x0086'
    PRODUCTS = ['0x0060:0x0003']
    
    def setup(self):
        # powerrelay 
        relay = self.new_device("powerrelay.basic")
        relay.add_method('turn_on',self.turn_on)
        relay.add_method('turn_off',self.turn_off)
        relay.new_attribute("power")
        # powermeter
        power = self.new_device("powermeter.basic")
        power.new_attribute("power")
        # map zwave var to 
        self.monitor_value('relay',core.COMMAND_CLASS.SWITCH_BINARY)
        self.monitor_value('power',core.COMMAND_CLASS.METER,1,8)
        
    def turn_on(self):
        self.set_value('relay',True)

    def turn_off(self):
        self.set_value('relay',False)
        
    def handle_value_changed(self,value):
        if value == self.get_value('relay'):
            self.devices[0].attributes['power']=value.data

        if value == self.get_value('power'):
            power = round(value.data)
            if power >= 0:
                self.devices[1].attributes['power']=power
