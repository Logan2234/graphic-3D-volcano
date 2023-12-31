#version 330 core

uniform mat4 projection;
uniform mat4 view;

in vec3 position;

out vec3 TexCoords;

void main() {
    TexCoords = position;
    gl_Position = projection * mat4(mat3(view)) * vec4(position, 1.0);
}