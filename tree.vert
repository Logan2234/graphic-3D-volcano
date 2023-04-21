#version 330 core

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

in vec3 tex_coord;
in vec3 position;
in vec3 normal;

out vec3 out_normal;
out vec3 frag_pos;
out vec4 view_space;
out vec2 frag_tex_coords;

void main() {
    out_normal = mat3(transpose(inverse(model))) * normal;
    frag_pos = vec3(model * vec4(position, 1.0));
    view_space = view * vec4(frag_pos, 1);
    frag_tex_coords = tex_coord.xy;
    gl_Position = projection * view_space;
}
