// #version 330 core

// uniform float time;
// uniform vec2 resolution;
// uniform sampler2D tex;

// in vec2 pos;

// out vec4 out_color;

// void main(void) {
//     // vec2 cPos = - 1 + 30.0 * pos.xy / resolution.xy;
//     // float cLength = length(cPos);

//     // vec2 uv = 10*pos.xy/resolution.xy+(cPos/cLength)*cos(cLength*12.0-time*2.0)*0.03 ;
//     // vec3 col = texture2D(tex,uv).xyz;

//     out_color = vec4(189.0/255.0, 171.0/255.0, 218.0/255.0,1.0);
// }

#version 330 core
out vec4 out_color;

in vec3 out_normal;
in vec3 out_position;

uniform vec3 w_camera_position;
uniform samplerCube skybox;

void main()
{             
    vec3 I = normalize(out_position - w_camera_position);
    vec3 R = reflect(I, normalize(out_normal));
    out_color = mix(vec4(texture(skybox, R).rgb, 1.0), vec4(122.0/255, 144.0/255, 252.0/255, 1), 0.3);
}