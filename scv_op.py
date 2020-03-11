import bpy

from bpy.types import Operator
 
# Blender utils and fonts module
import blf 

from . scv_types import *
from . scv_draw_util import *

def create_font(id, size, color):
    blf.color(id, color.r, color.g, color.b, 1.0 )
    blf.size(id, size, 72)
      
def draw_text(text, x, y, font_id):
    blf.position(font_id, x, y , 0) 
    blf.draw(font_id, text)
   
ignored_keys = {'LEFT_SHIFT', 'RIGHT_SHIFT', 'LEFT_ALT',
         'RIGHT_ALT', 'LEFT_CTRL', 'RIGHT_CTRL', 'TIMER',
         'MOUSEMOVE', 'EVT_TWEAK_L', 'INBETWEEN_MOUSEMOVE', 'TIMER_REPORT', 'TIMER1', 
         'TIMERREGION', 'WINDOW_DEACTIVATE', 'NONE'}

clear_events = {'WINDOW_DEACTIVATE', 'TIMER1', 'TIMER_REPORT'}

allowed_mouse_types = {'LEFTMOUSE','MIDDLEMOUSE','RIGHTMOUSE'}
    
	
class SCV_OT_draw_operator(Operator):
    bl_idname = "object.scv_ot_draw_operator"
    bl_label = "Shortcut VUr"
    bl_description = "Shortcut display operator" 
    bl_options = {'REGISTER'}
    
    duration : bpy.props.IntProperty()
	
    def __init(self):
        self.draw_handle = None
        self.draw_event  = None

    def check_create_batches(self, context):
        if context.window_manager.do_redraw:
            self.draw_util.create_batches(context, self.mouse_input)
            context.window_manager.do_redraw = False

    def invoke(self, context, event):
        args = (self, context)

        self.draw_util = SCV_Draw_Util(context)        
        self.key_input = SCV_Key_Input()
        self.mouse_input = SCV_Mouse_Input()
        self.width_region = context.region.width

        self.draw_util.create_batches(context, self.mouse_input)
                
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
        self.draw_event  = None
     
           
    def modal(self, context, event):
        if context.area:
            context.area.tag_redraw()

        self.handle_mouse_move(context, event)
    
        self.detect_keyboard(event)   
        
        self.detect_mouse(event)

        self.check_create_batches(context)
        
        if not context.window_manager.SCV_started:

            self.unregister_handlers(context)
            
            return {'CANCELLED'}
               
        return {"PASS_THROUGH"}

    def handle_mouse_move(self, context, event):
        if event.type == "MOUSEMOVE" and context.scene.h_dock == "3":
            self.mouse_input.set_mouse_pos(event.mouse_region_x, event.mouse_region_y)
            self.draw_util.create_batches(context, self.mouse_input)
    
    def detect_keyboard(self, event):
        if event.value == "PRESS" and event.type not in ignored_keys:
            self.key_input.input(event)
            self.mouse_input.clear()
                        
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
    def draw_callback_px(self, op, context):

        if context.region.width != self.width_region:
            self.width_region = context.region.width
            self.draw_util.create_batches(context, self.mouse_input)
            
        refresh_after_sec = 3.0
        font_color = context.scene.font_color
        font_size = 28

        if context.scene.show_buttons:

            # set color for buttons
            self.draw_util.set_color_buttons(context)

            # Draw the mouse buttons
            self.draw_util.draw_buttons(
            self.mouse_input.is_left,
            self.mouse_input.is_middle, 
            self.mouse_input.is_right)
        
        # draw the text for events
        current_time = time.time()
        
        time_diff_keys = current_time - self.key_input.timestamp
                            
        if(time_diff_keys < refresh_after_sec):
                                                 
            self.draw_text(font_size, font_color, context)

        else:
            self.key_input.clear()
            self.mouse_input.clear()

    def draw_text(self, font_size, font_color, context):
        font_id = 0
        create_font(font_id, font_size, font_color)

        text = str(self.key_input)

        ox = context.scene.cursor_offset_x
        oy = context.scene.cursor_offset_y

        # default left dock
        xpos_text = 12 + ox
        ypos_text = 30 + oy

        if context.scene.h_dock == "1":

            # right dock
            text_extent = blf.dimensions(font_id, text)
            xpos_text = context.region.width - text_extent[0] - 28 - ox 

        elif context.scene.h_dock == "2":

            # center dock
            ypos_text = 30
            text_extent = blf.dimensions(font_id, text)
            xpos_text = (context.region.width - text_extent[0]) / 2.0

        elif context.scene.h_dock == "3":

            offset_buttons = 120
            if context.scene.show_buttons == False:
                offset_buttons = 70

            oy = context.scene.cursor_offset_y + offset_buttons

            text_extent = blf.dimensions(font_id, text)
            xpos_text = self.mouse_input.mouse_x - (text_extent[0] / 2.0) + ox
            ypos_text = self.mouse_input.mouse_y - oy

        draw_text(text, xpos_text, ypos_text, font_id)

