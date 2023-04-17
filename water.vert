#version 330 core

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform float time;

in vec3 normal;
in vec3 position;
in vec3 tex_coord;

out vec3 out_normal;
out vec3 out_position;
out vec2 frag_tex_coords;

void main() {
    vec3 new_pos = position;

    new_pos.z = cos(new_pos.x * 0.6 + time);
    new_pos.x += 2 * sin(time);

    out_position = vec3(model * vec4(new_pos, 1.0));

    out_normal = mat3(transpose(inverse(model))) * normal;
    out_normal.x = sin(new_pos.x * 0.6 + time) * 0.5;
    out_normal = normalize(out_normal);

    frag_tex_coords = tex_coord.xy;
    gl_Position = projection * view * model * vec4(new_pos, 1.0);
}