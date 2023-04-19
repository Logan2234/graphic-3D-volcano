#version 330 core

uniform vec3 w_camera_position;

uniform sampler2D tex;
uniform sampler2D tex2;
uniform sampler2D tex3;

// In for texture calculations
in float mix_coef;
in vec2 frag_tex_coords;
in float dirt_coef;

// In for light calculations
in vec3 out_normal;
in vec3 frag_pos;
in vec4 view_space;

const vec3 lightColor = vec3(1, 1, 1);
const float K_a = 0.1;
const float K_s = 0;
const float K_d = 1 - K_s;

// Fog
const vec3 fogColor = vec3(.7, .7, .7);
const float FogDensity = .001;

out vec4 out_color;

void main() {
    vec4 grass = texture(tex, frag_tex_coords);
    vec4 basalte = texture(tex2, frag_tex_coords);
    vec4 dirt = texture(tex3, frag_tex_coords);

    vec4 tex_color = mix(basalte, mix(grass, dirt, dirt_coef), mix_coef);

    /**************** Light calculation *****************/

    // Ambient
    vec3 ambient = K_a * lightColor;

    // Diffuse
    vec3 norm = normalize(out_normal);
    vec3 lightDir = normalize(vec3(-0.5, -0.5, 1)); // Approx of sunlight pos

    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = K_d * diff * lightColor;

    // Specular
    vec3 viewDir = normalize(w_camera_position - frag_pos);
    vec3 reflectDir = reflect(-lightDir, norm);

    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
    vec3 specular = K_s * spec * lightColor;

    vec3 color = (ambient + diffuse + specular) * tex_color.rgb;

    // Fog
    float dist = length(view_space);
    float fogFactor = 1. / exp(pow(dist * FogDensity, 2));
    fogFactor = clamp(fogFactor, 0.1, 1);

    vec3 finalColor = mix(fogColor, color, fogFactor);
    out_color = vec4(finalColor, 1);
}