#version 330 core

uniform samplerCube skybox;
uniform vec3 w_camera_position;

//from vertex shader
in vec3 world_pos;
in vec3 world_normal;
in vec3 TexCoords;

const vec3 RimColor = vec3(.2, .2, .2);

out vec4 out_color;

void main() {

    vec3 tex1 = texture(skybox, TexCoords).rgb;

    //get light an view directions
    vec3 V = normalize(w_camera_position - world_pos);

    //diffuse lighting

    //rim lighting
    float rim = 1 - max(dot(V, world_normal), 0.);
    rim = smoothstep(.6, 1., rim);
    vec3 finalRim = RimColor * vec3(rim, rim, rim);

    //get all lights and texture
    vec3 lightColor = finalRim + tex1;

    out_color = vec4(lightColor, 1);
}