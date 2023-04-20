#version 330 core

uniform sampler2D tex; // Rock
uniform sampler2D tex2; // Dirt
uniform sampler2D tex3; // Grass
uniform vec3 w_camera_position;

// In for light calculations
in vec3 out_normal;
in vec3 frag_pos;
in vec4 view_space;
in vec2 frag_tex_coords;

vec3 lightColor = vec3(1, 1, 1);
const float K_a = 0.3;
const float K_s = 0.1;
const float K_d = 1 - K_s;

// Fog
const vec3 fogColor = vec3(.7, .7, .7);
const float FogDensity = .001;

out vec4 out_color;

void main() {
    vec4 color1 = texture(tex, frag_tex_coords);
    vec4 color2 = texture(tex2, frag_tex_coords);
    vec4 color3 = texture(tex3, frag_tex_coords);

    vec4 texture_color = vec4(0, 0, 0, 0);
    if (frag_pos.z >= 1) {
        texture_color = color3;
    } else if (frag_pos.z >= 0){
        texture_color = color2;
    } else {
        texture_color = color1;
    }

    /**************** Light calculation *****************/

    // Ambient
    float ambient = K_a;

    // Diffuse
    vec3 norm = normalize(out_normal);
    vec3 lightDir = normalize(vec3(-0.5, -0.5, 1)); // Approx of sunlight pos

    float diff = max(dot(norm, lightDir), 0.0);
    if (frag_pos.z >= 0){
        diff = dot(vec3(0, 0, 1), lightDir);
    }
    float diffuse = K_d * diff;

    // Specular
    vec3 viewDir = normalize(w_camera_position - frag_pos);
    vec3 reflectDir = reflect(-lightDir, norm);

    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 4);
    float specular = K_s * spec;

    vec3 colorWithDirLight = (ambient + diffuse + specular) * lightColor * texture_color.rgb;

    // Fog
    float dist = length(view_space);
    float fogFactor = 1. / exp(pow(dist * FogDensity, 2));
    fogFactor = clamp(fogFactor, 0.05, 1);

    vec3 finalColor = mix(fogColor, colorWithDirLight, fogFactor);
    out_color = vec4(finalColor, 1);
}
