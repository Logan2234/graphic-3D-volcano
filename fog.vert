//********************
// fog vertex shader
//*******************
#version 330

in vec3 position;
in vec3 normal;
in vec2 texcoord;

uniform mat4 model, view, projection;

out vec3 world_pos;
out vec3 world_normal;
out vec2 out_texcoord;
out vec4 viewSpace;

void main(){

    //used for lighting models
    world_pos = (model * vec4(position, 1)).xyz;
    world_normal = normalize(mat3(model) * normal);
    out_texcoord = texcoord;

    //send it to fragment shader
    viewSpace = view * model * vec4(position, 1);
    gl_Position=projection*viewSpace;

}