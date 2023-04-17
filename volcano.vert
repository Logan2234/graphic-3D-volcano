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

out vec2 frag_tex_coords;

// interpolated color for fragment shader, intialized at vertices
out float mix_coef;

void main() {
    // initialize interpolated colors at vertices
    frag_tex_coords = position.xy;
    mix_coef = normal.z;
    // tell OpenGL how to transform the vertex to clip coordinates
    gl_Position = projection * view * model * vec4(position, 1);
}
