#version 330 core

// global color
// uniform vec3 global_color;

// input attribute variable, given per vertex
in vec3 position;
in vec3 tex_coord;
in vec3 normal;

// global matrix variables
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

// Texture
out vec2 frag_tex_coords;
out float dirt_coef;
out float mix_coef;
// Light
out vec3 out_normal;
out vec3 frag_pos;
out vec4 view_space;

void main() {
    frag_tex_coords = tex_coord.xy;
    mix_coef = 1;
    // Compute mix_coef between basalte and grass
    if(position.z > 6) {
        mix_coef = normal.z;
    }

    // Compute dirt_coef
    if(position.z < 4) {
        dirt_coef = 1;
    } else if(position.z > 6) {
        dirt_coef = 0;
    } else {
        dirt_coef = -0.5 * position.z + 3;
    }

    out_normal = mat3(transpose(inverse(model))) * normal;
    frag_pos = vec3(model * vec4(position, 1.0));
    view_space = view * vec4(frag_pos, 1);
    gl_Position = projection * view_space;
}
