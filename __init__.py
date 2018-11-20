bl_info = {
    "name": "Shortcut VUr",
    "description": "Shortcut display addon",
    "author": "Jayanam",
    "version": (0, 6, 0, 0),
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

classes = ( SCV_OT_draw_operator, SCV_PT_panel )

register, unregister = bpy.utils.register_classes_factory(classes)
    
if __name__ == "__main__":
    register()