bl_info = {
    "name": "Shortcut VUr",
    "description": "Shortcut display addon",
    "author": "Jayanam",
    "version": (0, 5, 0, 1),
    "blender": (2, 80, 0),
    "location": "VIEW_3D",
    "category": "Object"}

# Blender imports
import bpy

from bpy.props import *

from . scv_op    import SCV_Operator
from . scv_panel import SCV_Panel

addon_keymaps = []

wm = bpy.types.WindowManager
wm.SCV_started = bpy.props.BoolProperty(default=False)

def register():
   bpy.utils.register_class(SCV_Operator)
   bpy.utils.register_class(SCV_Panel)
     
def unregister():
   bpy.utils.unregister_class(SCV_Operator)
   bpy.utils.unregister_class(SCV_Panel)
  
   
   # remove keymap entry
   for km, kmi in addon_keymaps:
       km.keymap_items.remove(kmi)
   addon_keymaps.clear()

    
if __name__ == "__main__":
    register()
