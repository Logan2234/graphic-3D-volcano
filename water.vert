#version 330 core

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform float time;

in vec3 normal;
in vec3 position;

out vec3 out_normal;
out vec3 out_position;
out vec2 frag_tex_coords;

// void main() {
//     vec3 temp = position;
//     temp.y = - temp.y;
//     gl_Position = projection * view * model * vec4(temp, 1);
//     pos = position.xy;
// }

void main() {
    vec3 new_pos = position;
    new_pos.z = cos(new_pos.x + time) * 0.3;
    new_pos.x += sin(time);
    out_position = vec3(model * vec4(new_pos, 1.0));
    out_normal = mat3(transpose(inverse(model))) * normal;
    out_normal.x = cos(new_pos.x + time) * 0.3;
    out_normal = normalize(out_normal);
    gl_Position = projection * view * model * vec4(new_pos, 1.0);
}