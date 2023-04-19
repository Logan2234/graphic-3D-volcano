#version 330 core

// global color
// uniform vec3 global_color;

// input attribute variable, given per vertex
in vec3 position;
// in vec3 tex_coord;
in vec3 normal;

// global matrix variables
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec2 frag_tex_coords;
out float dirt_coef;
out float mix_coef;

void main() {
    frag_tex_coords = position.xy;
    mix_coef = 1;
    // Compute mix_coef between basalte and grass
    if(position.z > 6) {
        mix_coef = normal.z;
    }

    // Compute dirt_coef
    if(position.z < 2) {
        dirt_coef = 1;
    } else if(position.z > 4) {
        dirt_coef = 0;
    } else {
        dirt_coef = -0.5 * position.z + 2;
    }
    gl_Position = projection * view * model * vec4(position, 1);
}
