import gpu

from gpu_extras.batch import batch_for_shader

class SCV_Draw_Util:

    def __init__(self, context):
        self.x_off = 14
        self.y_off = 50
        self.width_all = 70

        self.indices     = ((0, 1, 2), (0, 2, 3))

    def set_color_buttons(self, context):
        cb  = context.scene.color_buttons
        cba = context.scene.color_buttons_active

        self.color        = (cb.r, cb.g, cb.b, 1.0)
        self.color_active = (cba.r, cba.g, cba.b, 1.0)

    def create_batches(self, context, mouse_input):

        ox = context.scene.cursor_offset_x
        oy = context.scene.cursor_offset_y

        self.y_off = 50 + oy

        if context.scene.h_dock == "0":
            self.x_off = 14 + ox
        elif context.scene.h_dock == "1":
            self.x_off = context.region.width - 100 - ox

        # Follow cursor
        elif context.scene.h_dock == "3":
            self.x_off = mouse_input.mouse_x - 35 + ox
            self.y_off = mouse_input.mouse_y - 100 - oy
        else:
            self.x_off = ((context.region.width - self.width_all) / 2.0) - 1

        # bottom left, top left, top right, bottom right
        self.vertices_left   = ((self.x_off,      20 + self.y_off), (self.x_off,      50 + self.y_off), (self.x_off + 20, 50 + self.y_off), (self.x_off + 20, 20 + self.y_off))
        self.vertices_right  = ((self.x_off + 50, 20 + self.y_off), (self.x_off + 50, 50 + self.y_off), (self.x_off + 70, 50 + self.y_off), (self.x_off + 70, 20 + self.y_off))
        self.vertices_middle = ((self.x_off + 30, 30 + self.y_off), (self.x_off + 30, 50 + self.y_off), (self.x_off + 40, 50 + self.y_off), (self.x_off + 40, 30 + self.y_off))
        self.shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')

        self.batch_left_button   = batch_for_shader(self.shader, 'TRIS', {"pos" : self.vertices_left},   indices = self.indices)
        self.batch_right_button  = batch_for_shader(self.shader, 'TRIS', {"pos" : self.vertices_right},  indices = self.indices)
        self.batch_middle_button = batch_for_shader(self.shader, 'TRIS', {"pos" : self.vertices_middle}, indices = self.indices)

    def __get_color(self, key_state):
        if key_state is True:
            return self.color_active
        else:
            return self.color
    
    def __set_color(self, key_state):
        self.shader.uniform_float("color", self.__get_color(key_state))
    
    def draw_buttons(self, left, middle, right):
        
        self.shader.bind()
        
        self.__set_color(left)
        self.batch_left_button.draw(self.shader)
        
        self.__set_color(middle)
        self.batch_middle_button.draw(self.shader)
        
        self.__set_color(right)
        self.batch_right_button.draw(self.shader)