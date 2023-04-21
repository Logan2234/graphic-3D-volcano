#version 330 core

uniform samplerCube skybox;

in vec3 TexCoords;

out vec4 out_color;

const vec3 skyboxFogColor = vec3(0.4, 0.4, 0.4);
void main() {
    vec3 tex1 = texture(skybox, TexCoords).rgb;
    out_color = vec4(mix(tex1, skyboxFogColor, 0.3), 1);
}