import bpy
from bpy.types import Panel

class SCV_PT_panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Shortcut VUr"
    bl_category = "Shortcut VUr"
    
    def draw(self, context):
        
        layout = self.layout
        scene = context.scene
                          
        row = layout.row()
        
        if(context.window_manager.SCV_started):
            row.operator('object.scv_ot_draw_operator', text="Stop Shortcut VUr", icon="CANCEL")
        else:
            row.operator('object.scv_ot_draw_operator', text="Start Shortcut VUr", icon="PLAY")

        row = layout.row()
        layout.prop(context.scene, "h_dock")
        
        # Offset only for left, right or dock to cursor, not when it is centered
        if (scene.h_dock != "2"):
            row = layout.row()
            layout.prop(context.scene, "cursor_offset_x")

            row = layout.row()
            layout.prop(context.scene, "cursor_offset_y")

        row = layout.row()
        layout.prop(context.scene, "font_color")

        row = layout.row()
        layout.prop(context.scene, "color_buttons")

        row = layout.row()
        layout.prop(context.scene, "color_buttons_active")

        row = layout.row()
        layout.prop(context.scene, "show_buttons")