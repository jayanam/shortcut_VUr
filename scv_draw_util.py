import gpu

from gpu_extras.batch import batch_for_shader

# bottom left, top left, top right, bottom right
vertices_left   = ((20, 20), (20, 50), (40, 50), (40, 20))
vertices_right  = ((70, 20), (70, 50), (90, 50), (90, 20))
vertices_middle = ((50, 30), (50, 50), (60, 50), (60, 30))

indices = ((0, 1, 2), (0, 2, 3))

# color tuples
grey  = (0.6, 0.6, 0.6, 0.1)
white = (1, 1, 1, 1)

shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')

batch_left_button = batch_for_shader(shader, 'TRIS', {"pos" : vertices_left}, indices=indices)

batch_right_button = batch_for_shader(shader, 'TRIS', {"pos" : vertices_right}, indices=indices)

batch_middle_button = batch_for_shader(shader, 'TRIS', {"pos" : vertices_middle}, indices=indices)

def __get_color(key_state):
    if key_state is True:
        return white
    else:
        return grey
    
def __set_color(key_state):
    shader.uniform_float("color", __get_color(key_state))
    
def draw_buttons(left, middle, right):
    
    shader.bind()
    
    __set_color(left)
    
    batch_left_button.draw(shader)
    
    __set_color(middle)
    batch_middle_button.draw(shader)
    
    __set_color(right)
    batch_right_button.draw(shader)