from xaal.zwave import core


class RGBBulb(core.ZDevice):
    MANUFACTURER_ID = '0x0131'
    PRODUCTS = ['0x0002:0x0002',]

    def setup(self):
        lamp = self.new_device("lamp.rgb")
        # attributes
        lamp.new_attribute("light")
        lamp.new_attribute("dimmer")
        # methods
        lamp.add_method('turn_on',self.turn_on)
        lamp.add_method('turn_off',self.turn_off)
        lamp.add_method('dim',self.dim)
        lamp.add_method('blink',self.blink)
        self.monitor_value('level',core.COMMAND_CLASS.SWITCH_MULTILEVEL)
        self.monitor_value('color',core.COMMAND_CLASS.ZIP_ADV_SERVER,1)
        self._blink_color = 0

    def set_level(self,value):
        self.set_value('level',value)
        self.gw.engine.add_timer(self.get_value('level').refresh,1,2)
        
    def turn_on(self):
        self.set_level(0x63)

    def turn_off(self):
        self.set_level(0)

    def dim(self,_value):
        val = int(_value)
        if (val > 0) and (val <100):
            self.set_level(val)

    def red(self):
        self.get_value('color').data = '#FF00000000'

    def white(self):
        self.get_value('color').data = '#000000FFFF'
        
    def _blink(self):
        # turn on, but avoid the timer..
        if self._blink_color == 0:
            self.red()
            self._blink_color = 1
        else:
            self.white()
            self._blink_color = 0
        
    def blink(self):
        eng = self.gw.engine
        state = self.devices[0].attributes["light"]
        #self.set_value('level',0x63)
        self.turn_on()
        eng.add_timer(self.white,19,1)        
        if state == False:
            eng.add_timer(self.turn_off,20,1)
        self.gw.engine.add_timer(self._blink,1,15)
        

    def handle_value_changed(self,value):
        if value == self.get_value('level'):
            dev = self.devices[0]
            dev.attributes["dimmer"] = value.data
            if value.data == 0:
                dev.attributes["light"] = False
            else:
                dev.attributes["light"] = True
                
