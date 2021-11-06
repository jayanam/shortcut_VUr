import time

class SCV_Key_Input:

    def __init__(self):
        self._friendly_names = { 'LEFTMOUSE': 'Left', 'RIGHTMOUSE': 'Right', 'MIDDLEMOUSE': 'Middle',
                                 'WHEELUPMOUSE': "Mouse wheel up", "WHEELDOWNMOUSE": "Mouse wheel down",
                                 'ESC': 'Escape', 'RET': 'Enter', 'ONE' : '1', 'TWO': '2', 'THREE' : '3', 'FOUR': '4',
                                 'FIVE': '5', 'SIX':'6', 'SEVEN':'7', 'EIGHT' : '8', 'NINE': '9', 'ZERO' : '0',
                                 'COMMA' : 'Comma', 'PERIOD' : 'Period','OSKEY':'Command'}
        self.clear()

    def clear(self):
        self.is_ctrl  = False
        self.is_alt   = False
        self.is_shift = False
        self.key = ''
        self.detect_times = 0
        self.timestamp = time.time()

    def get_event_type(self, event):
        if event.type in self._friendly_names:
            return self._friendly_names[event.type]
        return event.type
      
    def input(self, event):    

        if self.is_same(event):
            self.detect_times += 1
        else:
            self.detect_times = 1

        self.is_ctrl = event.ctrl
        self.is_alt = event.alt
        self.is_shift = event.shift
        self.key = self.get_event_type(event)
        self.timestamp = time.time()

    def is_same(self, event):
        return (self.is_ctrl  == event.ctrl  and
                self.is_alt   == event.alt   and
                self.is_shift == event.shift and
                self.key == self.get_event_type(event))
          
    def __str__(self):
        result = []
        
        if(self.is_shift):
            result.append("Shift")
            
        if(self.is_ctrl):
            result.append("Ctrl")
            
        if(self.is_alt):
            result.append("Alt")
                    
        if(self.key != ''):
            result.append(self.key)

        if(len(result) > 0):
            if self.detect_times > 1:
                result.append("x " + str(self.detect_times))

            return " ".join(result)                  
        
        return ''
        
class SCV_Mouse_Input:

    def __init__(self):
        self.clear()
        self.set_mouse_pos(0,0)
    
    def clear(self):
        self.is_left   = False
        self.is_middle = False
        self.is_right  = False

    def set_mouse_pos(self, x, y):
        self.mouse_x = x
        self.mouse_y = y
        
    def input(self, event):
        
        self.clear()
        if(event.type == 'LEFTMOUSE'):
            self.is_left = event.value == 'PRESS'
        if(event.type == 'MIDDLEMOUSE'):
            self.is_middle = event.value == 'PRESS'  
        if(event.type == 'RIGHTMOUSE'):
            self.is_right = event.value == 'PRESS'            
        
    def __str__(self):
        result = ""
        result = result + "left: "  + str(self.is_left) + ", "
        result = result + "middle: "  + str(self.is_middle) + ", "
        result = result + "right: " + str(self.is_right)
        return result