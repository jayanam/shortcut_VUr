import bpy

import time

from bpy.types import Operator
 
# Blender utils and fonts module
import blf 

# Blender wrapper for opengl
import bgl

def draw_bg(region):
    
    # Enable Opengl alpha
    bgl.glEnable(bgl.GL_BLEND)
    
    # set color: red, green, blue, alpha
    # bgl.glColor4f(1.0, 0.0, 0.0, 0.1)
    
    # draw rectangle
    # x0, y0, x1, y1
    # bgl.glRecti(1, 100, region.width, 0)

def create_font(id, size):
    blf.size(id, size, 72)
      
def draw_text(text, x, y, font_id):

    blf.position(font_id, x, y , 0)
    
    # We have to wait for Draw API of Blender 2.8
    # bgl.glColor4f(1.0, 1.0, 1.0, 1.0)
    
    blf.draw(font_id, text)
    
allowed_key_types = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

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
        self.is_left   = False
        self.is_middle = False
        self.is_right  = False
        
    def input(self, event):
        
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
	
class SCV_Operator(Operator):
    bl_idname = "object.scv_op"
    bl_label = "Shortcut VUr"
    bl_description = "Shortcut display addon" 
    bl_options = {'REGISTER'} 
	
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
        self.draw_handle = bpy.types.SpaceView3D.draw_handler_add(self.draw_callback_px, args, "WINDOW", "POST_PIXEL")
        self.draw_event = context.window_manager.event_timer_add(0.1, window=context.window)
        
    def unregister_handlers(self, context):
        
        context.window_manager.event_timer_remove(self.draw_event)
        
        bpy.types.SpaceView3D.draw_handler_remove(self.draw_handle, "WINDOW")
        
        self.draw_handle = None
        self.draw_event = None
     
           
    def modal(self, context, event):
        context.area.tag_redraw()
    
        self.detect_keyboard(event)   
        
        # TODO: Implement when 2.8 draw API is available
        # self.detect_mouse(event)  
        
        if not context.window_manager.SCV_started:

            self.unregister_handlers(context)
            
            return {'CANCELLED'}
               
        return {"PASS_THROUGH"}
    
    def detect_keyboard(self, event):
        if(event.value == 'PRESS' and event.type in allowed_key_types):
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
    def draw_callback_px(tmp, self, context):
        
        region = context.region
        
        current_time = time.time()
        
        time_diff_keys = current_time - self.key_input.timestamp
        
        if(time_diff_keys < 4.0):
                        
            xt = int(region.width / 2.0)
                             
            # Big font
            font_id = 0
            create_font(font_id, 30)
            
            text = str(self.key_input)
            
            #draw_text(text, xt- blf.dimensions(font_id, text)[0] / 2, 30, font_id)
            draw_text(text, 40, 30, font_id)
