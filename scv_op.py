import bpy

import time

from bpy.types import Operator
 
# Blender utils and fonts module
import blf 

from . scv_draw_util import *

def create_font(id, size):
    blf.size(id, size, 72)
      
def draw_text(text, x, y, font_id):

    blf.position(font_id, x, y , 0)
    
    blf.draw(font_id, text)
    
ignored_keys = ['LEFT_SHIFT', 'RIGHT_SHIFT', 'LEFT_ALT',
         'RIGHT_ALT', 'LEFT_CTRL', 'RIGHT_CTRL', 'TIMER',
         'MOUSEMOVE', 'INBETWEEN_MOUSEMOVE', 'TIMER_REPORT', 'TIMER1', 
         'TIMERREGION', 'WINDOW_DEACTIVATE', 'NONE']

allowed_mouse_types = ['LEFTMOUSE','MIDDLEMOUSE','RIGHTMOUSE']
    
class SCV_Key_Input:

    def __init__(self):
        self.is_ctrl  = False
        self.is_alt   = False
        self.is_shift = False
        self.key = ''
        self.timestamp = time.time()
        
    def input(self, event):    
        self.is_ctrl = event.ctrl
        self.is_alt = event.alt
        self.is_shift = event.shift
        self.key = event.type
        self.timestamp = time.time()
                
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
            return ' + '.join(result)                  
        
        return ''
        
class SCV_Mouse_Input:

    def __init__(self):
        self.init()
    
    def init(self):
        self.is_left   = False
        self.is_middle = False
        self.is_right  = False         
        
    def input(self, event):
        
        self.init()
        if(event.type == 'LEFTMOUSE'):
            self.is_left = event.value == 'PRESS'
        if(event.type == 'MIDDLEMOUSE'):
            self.is_middle = event.value == 'PRESS'  
        if(event.type == 'RIGHTMOUSE'):
            self.is_right = event.value == 'PRESS'            
        
    def __str__(self):
        result = ""
        result = result + "left: "  + str(self.is_left) + ", "
        result = result + "middle: "   + str(self.is_middle) + ", "
        result = result + "right: " + str(self.is_right)
        return result
	
class SCV_OT_draw_operator(Operator):
    bl_idname = "object.scv_ot_draw_operator"
    bl_label = "Shortcut VUr"
    bl_description = "Shortcut display operator" 
    bl_options = {'REGISTER'}
    
    duration = bpy.props.IntProperty()
	
    @classmethod
    def poll(cls, context):
        return True
    
    def __init(self):
        self.draw_handle = None
        self.draw_event  = None

    def invoke(self, context, event):
        args = (self, context)
        
        self.key_input = SCV_Key_Input()
        self.mouse_input = SCV_Mouse_Input()

        
        if(context.window_manager.SCV_started is False):
            context.window_manager.SCV_started = True
                
            # Register draw callback
            self.register_handlers(args, context)
                       
            context.window_manager.modal_handler_add(self)
            return {"RUNNING_MODAL"}
        else:
            context.window_manager.SCV_started = False
            return {'CANCELLED'}
    
    def register_handlers(self, args, context):
        self.draw_handle = bpy.types.SpaceView3D.draw_handler_add(self.draw_callback_px, (self, context), "WINDOW", "POST_PIXEL")
        self.draw_event = context.window_manager.event_timer_add(0.1, window=context.window)
        
    def unregister_handlers(self, context):
        
        context.window_manager.event_timer_remove(self.draw_event)
        
        bpy.types.SpaceView3D.draw_handler_remove(self.draw_handle, "WINDOW")
        
        self.draw_handle = None
        self.draw_event  = None
     
           
    def modal(self, context, event):
        if context.area:
            context.area.tag_redraw()
    
        self.detect_keyboard(event)   
        
        self.detect_mouse(event)  
        
        if not context.window_manager.SCV_started:

            self.unregister_handlers(context)
            
            return {'CANCELLED'}
               
        return {"PASS_THROUGH"}
    
    def detect_keyboard(self, event):
        if event.type not in ignored_keys:
            self.key_input.input(event)
                        
    def detect_mouse(self, event):

        if(event.type in allowed_mouse_types):
            self.mouse_input.input(event)
            
    def cancel(self, context):
        if context.window_manager.SCV_started:
            self.unregister_handlers(context)
        return {'CANCELLED'}        
        
    def finish(self):
        self.unregister_handlers(context)
        return {"FINISHED"}
		
	    # Draw handler to paint onto the screen
    def draw_callback_px(self, context, args):
            
        draw_buttons(
        self.mouse_input.is_left,
        self.mouse_input.is_middle, 
        self.mouse_input.is_right)
        
        current_time = time.time()
        
        time_diff_keys = current_time - self.key_input.timestamp
                            
        if(time_diff_keys < 4.0):
                                                 
            font_id = 0
            create_font(font_id, 28)
            
            text = str(self.key_input)
                                    
            draw_text(text, 12, 30, font_id)