import bpy
from bpy.types import Panel

from . scv_op import SCV_Operator

class SCV_Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_label = "Shortcut VUr"
    bl_category = "Shortcut VUr"
    
    def draw(self, context):
        
        layout = self.layout
        scene = context.scene
                          
        row = layout.row()
        
        if(context.window_manager.SCV_started):
            row.operator('object.scv_op', text="Stop Shortcut VUr", icon="CANCEL")
        else:
            row.operator('object.scv_op', text="Start Shortcut VUr", icon="PLAY")
 
