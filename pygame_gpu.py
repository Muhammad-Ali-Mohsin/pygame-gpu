import moderngl

import pygame

from array import array

FRAG_SHADER_PATH = "shaders/shader.frag"
VERT_SHADER_PATH = "shaders/shader.vert"

class MGLWindow:
    def __init__(self, vert_path, frag_path, input_resolution, output_resolution):
        self.window = pygame.display.set_mode(output_resolution, pygame.OPENGL | pygame.DOUBLEBUF)
        self.ctx = moderngl.create_context()
        self.uniforms = {}
        self.memory_locations = {}

        # Vertex Buffer Object mapping each vertice on the pygame surface to the one on the opengl texture. Each line is (mgl x, mgl y, py x, py y)
        vbo = self.ctx.buffer(data=array('f', [
            -1.0, 1.0, 0.0, 0.0,
            1.0, 1.0, 1.0, 0.0,
            -1.0, -1.0, 0.0, 1.0,
            1.0, -1.0, 1.0, 1.0,
        ]))

        # Loads in the shaders
        with open(vert_path, "r") as f:
            vert_shader = f.read()

        with open(frag_path, "r") as f:
            frag_shader = f.read()

        # Program which packages the shaders together
        self.program = self.ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)

        # Vertex Array Object
        self.vao = self.ctx.vertex_array(self.program, [(vbo, '2f 2f', 'vert', 'texcoord')])

        # Pygame Surface
        self.screen = pygame.Surface(input_resolution).convert_alpha()

    def pass_uniforms(self, uniforms={}):
        """
        Turns all the surface uniforms into textures and passes them into the vao
        """
        if 'screen_texture' not in uniforms: uniforms['screen_texture'] = self.screen

        for uniform in uniforms:
            # Checks whether the uniform is a pygame Surface
            if isinstance(uniforms[uniform], pygame.Surface):
                # Converts the uniform to a moderngl Texture
                self.uniforms[uniform] = self.surf_to_texture(uniforms[uniform])
                # Checks whether it has an assigned memory location and if not, assigns it to the next available location
                if uniform not in self.memory_locations:
                    if len(self.memory_locations) == 0:
                       self.memory_locations[uniform] = 0
                    else: 
                        self.memory_locations[uniform] = max(self.memory_locations.values()) + 1
                    # Tells the program which memory location the uniform is at
                    self.program[uniform] = self.memory_locations[uniform]
                # Tells the uniform which memory location to go to
                self.uniforms[uniform].use(self.memory_locations[uniform])
            else:
                self.program[uniform].value = uniforms[uniform]

    def release(self, uniforms={}):
        """
        Releases all the uniforms to free the space in memory
        """
        for uniform in uniforms:
            # Checks if the uniform is a moderngl Texture and releases it if so
            if uniform in self.uniforms and isinstance(self.uniforms[uniform], moderngl.Texture):
                    self.uniforms[uniform].release()

    def surf_to_texture(self, surf):
        """
        Converts a pygame surface to an OpenGL texture
        """
        # Creates a texture the same size as the surface
        tex = self.ctx.texture(surf.get_size(), 4)
        # Tells the texture to use the nearest colour when resizing instead of interpolating colours
        tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        # Tells te texture to use the BGRA format that pygame uses instead of the conventional RGBA
        tex.swizzle = 'BGRA'
        # Fills the texture with the pixel data from the pygame surface
        tex.write(surf.get_view('1'))
        return tex

    def update(self, uniforms={}):
        """
        Updates the display when provided with the uniforms
        """
        # Passes the uniforms to te program and then runs the shaders to render the frame before releasing the uniforms and updating the screen
        self.pass_uniforms(uniforms)
        self.vao.render(mode=moderngl.TRIANGLE_STRIP)
        self.release(uniforms)
        pygame.display.flip()

    def __getattribute__(self, name):
        try:
            return super().__getattribute__(name)
        except AttributeError:
            return getattr(self.screen, name)


def create_window(output_resolution, input_resolution=None, vert_shader=None, frag_shader=None):
    """
    Creates a window
    """
    if input_resolution == None: input_resolution = output_resolution
    if vert_shader == None: vert_shader = VERT_SHADER_PATH
    if frag_shader == None: frag_shader = FRAG_SHADER_PATH
    pygame.display.init()
    window = MGLWindow(vert_shader, frag_shader, input_resolution, output_resolution)
    return window
