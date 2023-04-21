//********************
// fog vertex shader
//*******************
#version 330

in vec3 position;
in vec3 normal;
in vec2 texcoord;

uniform mat4 model, view, projection;

out vec3 frag_pos;
out vec3 out_normal;
out vec2 frag_tex_coords;
out vec4 viewSpace;

void main(){

    //used for lighting models
    frag_pos = (model * vec4(position, 1)).xyz;
    out_normal = normalize(mat3(model) * normal);
    frag_tex_coords = texcoord;

    //send it to fragment shader
    viewSpace = view * model * vec4(position, 1);
    gl_Position=projection*viewSpace;

}