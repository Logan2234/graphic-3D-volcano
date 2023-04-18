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

    float distance = sqrt(pow(new_pos.x, 2) + pow(new_pos.y, 2));
    float offset = distance * 0.05;
    float amplitude = 10;

    new_pos.z += amplitude * cos(offset + time);

    out_position = vec3(model * vec4(new_pos, 1.0));

    out_normal = mat3(transpose(inverse(model))) * normal;
    out_normal.xy = vec2(sin(offset / 2 + time / 2));
    out_normal = normalize(out_normal);

    frag_tex_coords = tex_coord.xy;
    gl_Position = projection * view * model * vec4(new_pos, 1.0);
}