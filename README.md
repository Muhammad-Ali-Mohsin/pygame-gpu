
# Pygame GPU

A small module which seamlessly interfaces the popular pygame library with the GPU, allowing for better performance and shader support.


## Installation

Download all files and extract them into your project. Use pip to install the necessary requirements.

```bash
pip install moderngl pygame
```
    
## How to use

To use, download all files and extract them into your project. Then, include the following at the top of your file.

```py
from pygame_gpu import create_window
```

The create window function can then be used to return a custom window class which will run the shaders for you. Use this instead of `pygame.display.set_mode`. Usage:

```py
window = create_window(output_resolution, input_resolution=None, vert_shader=None, frag_shader=None)
```

If you do not provide an input resolution, the window will use your output resolution and if you do not provide specific shader paths, it will use the default shaders.

Finally, use Pygame as normal but instead of using `pygame.display.update` or `pygame.display.flip` when updating the screen, call the update method on the window.

```py
window.update(uniforms={})
```

Any uniforms you specify will be passed into the shader. You can also pass Pygame surfaces as a uniform and they will be automatically converted into a ModernGL texture by the window for use with the shader.

If at any point, you need to reference the window surface, such as when using Pygame methods like `pygame.draw.rect`, use `window.screen` instead of `window`. This will ensure the function will receive the Pygame Surface.


## Additional Information

This module allows for shader support with Pygame. These shaders are written using the OpenGL Shading Language (GLSL). 

The module supports two types of shaders, a vertex shader and a fragment shader. The vertex shader is responsible for mapping the corners of the pygame surface onto the window. You can modify this if you want to transform the shape of your output.

The fragment shader is responsible for running calculations on each individual pixel on your window. This has the most applications with Pygame and will allow you to create filters and effects within your projects.

The shaders take in uniforms. This refers to data which remains constant across all instances of the shader. Common examples may include Pygame surfaces such as the screen or a time variable.
