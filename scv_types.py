import time

class SCV_Key_Input:

    def __init__(self):
        self.clear()

    def clear(self):
        self.is_ctrl  = False
        self.is_alt   = False
        self.is_shift = False
        self.key = ''
        self.detect_times = 0
        self.timestamp = time.time()
        
    def input(self, event):    

        if self.is_same(event):
            self.detect_times += 1
        else:
            self.detect_times = 1

        self.is_ctrl = event.ctrl
        self.is_alt = event.alt
        self.is_shift = event.shift
        self.key = event.type
        self.timestamp = time.time()

    def is_same(self, event):
        return (self.is_ctrl  == event.ctrl  and
                self.is_alt   == event.alt   and
                self.is_shift == event.shift and
                self.key == event.type)
          
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
    
    def clear(self):
        self.is_left   = False
        self.is_middle = False
        self.is_right  = False
        
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