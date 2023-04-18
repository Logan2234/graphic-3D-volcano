#version 330 core
out vec4 out_color;

in vec3 out_normal;
in vec3 out_position;
in vec2 frag_tex_coords;

uniform vec3 w_camera_position;
uniform samplerCube skybox;
uniform sampler2D tex;

void main() {
    vec3 I = normalize(out_position - w_camera_position);
    vec3 R = reflect(I, normalize(out_normal));

    // Coloured version with reflection
    // out_color = mix(vec4(texture(skybox, R).rgb, 1), vec4(0.18, 0.49, 0.65, 1.0), 0.7);

    // Textured version with reflection
    // out_color = mix(texture(skybox, R), texture(tex, frag_tex_coords), 1);

    // Textured version with work on normal
    out_color = mix(texture(tex, frag_tex_coords), vec4(0.23, 0.54, 0.70, 1), out_normal.z * 0.8);

}