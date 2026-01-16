from xaal.zwave import core
from functools import partial

class PowerNode6(core.ZDevice):
    """ Greenwave Power Noe 6 port"""
    
    MANUFACTURER_ID = '0x0099'
    PRODUCTS = ['0x0004:0x0003',]
    
    def setup(self):
        for i in range(0,6):
            # powerrelay 
            relay = self.new_device("powerrelay.basic")
            on = partial(self.rel_on,i)
            off = partial(self.rel_off,i)
            relay.add_method('turn_on',on)
            relay.add_method('turn_off',off)
            relay.new_attribute("power")
            self.monitor_value('relay_%s' % i,core.COMMAND_CLASS.SWITCH_BINARY,i+2,0)

        for i in range(0,6):
            # powermeter
            power = self.new_device("powermeter.basic")
            power.new_attribute("power")
            # map zwave var to 
            value = 'power_%s' % i
            self.monitor_value(value,core.COMMAND_CLASS.METER,i+2,8)
            self.gw.engine.add_timer(self.get_value(value).refresh,30)

    def rel_on(self,r_id):
        self.set_value('relay_%s' % r_id,True)

    def rel_off(self,r_id):
        self.set_value('relay_%s'% r_id,False)
        
    def handle_value_changed(self,value):
        for i in range(0,6):
            tmp = self.get_value('relay_%s' % i)
            if value == tmp:
                self.devices[i].attributes['power']=value.data
                # force a power refresh on state change
                self.gw.engine.add_timer(self.get_value('power_%s' % i).refresh,2,2)
                
        for i in range(0,6):
            tmp = self.get_value('power_%s' % i)
            if value == tmp:
                power = round(value.data)
                if power >= 0:
                    self.devices[i+6].attributes['power']=power
