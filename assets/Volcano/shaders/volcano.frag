#version 330 core

uniform sampler2D tex;
uniform sampler2D tex2;
uniform sampler2D tex3;

// receiving interpolated color for fragment shader
in float mix_coef;
in vec2 frag_tex_coords;
in float dirt_coef;

// output fragment color for OpenGL
out vec4 out_color;

void main() {
    vec4 grass = texture(tex, frag_tex_coords);
    vec4 basalte = texture(tex2, frag_tex_coords);
    vec4 dirt = texture(tex3, frag_tex_coords);

    out_color = mix(basalte, mix(grass, dirt, dirt_coef), mix_coef);
}