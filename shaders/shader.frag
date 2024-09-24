#version 330 core

uniform sampler2D screen_texture;  // The input texture

in vec2 uv;
out vec4 f_color;

void main()
{
    // Gets the initial color from the texture
    vec4 screen_color = texture(screen_texture, uv);
    f_color = screen_color;
}
