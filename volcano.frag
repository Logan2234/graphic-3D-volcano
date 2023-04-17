#version 330 core

uniform sampler2D tex;
uniform sampler2D tex2;

// receiving interpolated color for fragment shader
in float mix_coef;
in vec2 frag_tex_coords;

// output fragment color for OpenGL
out vec4 out_color;

void main() {
    vec4 color1 = texture(tex, frag_tex_coords);
    vec4 color2 = texture(tex2, frag_tex_coords);
    out_color = mix(color1, color2, (1 - mix_coef) * 0.75);
}
