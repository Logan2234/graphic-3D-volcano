//********************
// fog vertex shader
//*******************
#version 330

in vec3 in_position;
in vec3 in_normal;
in vec2 in_texcoord;

uniform mat4 model, view, projection;

out vec3 world_pos;
out vec3 world_normal;
out vec2 texcoord;
out vec4 viewSpace;

void main(){
    
    //used for lighting models
    world_pos=(model*vec4(in_position,1)).xyz;
    world_normal=normalize(mat3(model)*in_normal);
    texcoord=in_texcoord;
    
    //send it to fragment shader
    viewSpace=view*model*vec4(in_position,1);
    gl_Position=projection*viewSpace;
    
}