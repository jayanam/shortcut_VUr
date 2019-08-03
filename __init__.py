bl_info = {
    "name": "Shortcut VUr",
    "description": "Shortcut display addon",
    "author": "Jayanam",
    "version": (0, 7, 2, 0),
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

h_dock = [ ("0",  "Left",  "Dock to the left side"),
           ("1",  "Right", "Dock to the right side"),
           ("2",  "Center", "Dock to the center")
         ]

bpy.types.Scene.h_dock = bpy.props.EnumProperty(
    items = h_dock, name="Dock", 
    description="Dock to left or right side", 
    default="1")

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