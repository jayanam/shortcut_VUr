bl_info = {
    "name": "Shortcut VUr",
    "description": "Shortcut display addon",
    "author": "Jayanam",
    "version": (0, 9, 2, 0),
    "blender": (2, 80, 0),
    "location": "View3D",
    "category": "Object"}

# Blender imports
import bpy

from bpy.props import *

from . scv_op    import SCV_OT_draw_operator
from . scv_panel import SCV_PT_panel

addon_keymaps = []

wm = bpy.types.WindowManager
wm.SCV_started = bpy.props.BoolProperty(default=False)
wm.do_redraw = bpy.props.BoolProperty(default=False)

def do_redraw(self, context):
    context.window_manager.do_redraw = True

bpy.types.Scene.show_buttons = bpy.props.BoolProperty(
    name="Show Buttons", 
    description="Show or hide the mouse buttons", 
    default=True)

h_dock = [ ("0",  "Left",  "Dock to the left side"),
           ("1",  "Right", "Dock to the right side"),
           ("2",  "Center", "Dock to the center"),
           ("3",  "Cursor", "Attach to mouse cursor")
         ]

bpy.types.Scene.h_dock = bpy.props.EnumProperty(
    items = h_dock, name="Dock", 
    description="Dock to left, center, right or to the cursor", 
    default="1",
    update=do_redraw)

bpy.types.Scene.cursor_offset_x = IntProperty(
                                      name="Offset X", 
                                      description="Offset X to cursor",
                                      default = 0,
                                      update=do_redraw)

bpy.types.Scene.cursor_offset_y = IntProperty(
                                      name="Offset Y", 
                                      description="Offset Y to cursor",
                                      default = 0,
                                      update=do_redraw)

bpy.types.Scene.font_color = bpy.props.FloatVectorProperty(  
   name="Text Color",
   subtype='COLOR',
   default=(1.0, 1.0, 1.0),
   min=0.0, max=1.0,
   description="Color for the text"
   )

bpy.types.Scene.color_buttons = bpy.props.FloatVectorProperty(  
   name="Color Buttons",
   subtype='COLOR',
   default=(0.1, 0.1, 0.1),
   min=0.0, max=1.0,
   description="Color for mouse buttons"
   )

bpy.types.Scene.color_buttons_active = bpy.props.FloatVectorProperty(  
   name="Color Buttons active",
   subtype='COLOR',
   default=(1.0, 1.0, 1.0),
   min=0.0, max=1.0,
   description="Color for mouse active buttons"
   )

classes = ( SCV_OT_draw_operator, SCV_PT_panel )

register, unregister = bpy.utils.register_classes_factory(classes)
    
if __name__ == "__main__":
    register()