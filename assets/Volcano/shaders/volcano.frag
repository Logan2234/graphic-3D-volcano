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

vec3 lightColor = vec3(1, 1, 1);
vec3 lavaColor = vec3(0.811, 0.06, 0.125);
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
    float ambient = K_a;

    // Diffuse
    vec3 norm = normalize(out_normal);
    vec3 lightDir = normalize(vec3(-0.5, -0.5, 1)); // Approx of sunlight pos

    float diff = max(dot(norm, lightDir), 0.0);
    float diffuse = K_d * diff;

    // Specular
    vec3 viewDir = normalize(w_camera_position - frag_pos);
    vec3 reflectDir = reflect(-lightDir, norm);

    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
    float specular = K_s * spec;

    vec3 colorWithDirLight = (ambient + diffuse + specular) * lightColor * tex_color.rgb;

    // Computation of light emitted by lava
    vec3 lavaPos = vec3(0, 0, 150);
    vec3 lightDirLava = normalize(lavaPos - frag_pos);
    float diffLava = max(dot(norm, lightDirLava), 0.0);
    float diffuseLava = K_d * diffLava;

    // Attenuation of point light
    float distance = length(lightDirLava - frag_pos);
    float attenuation = 1.0 / (1.0 + 0.005 * distance + 0.00008 * (distance * distance));

    vec3 color = colorWithDirLight;

    if(length(frag_pos.xy) < 30)
        color += diffuseLava * attenuation * lavaColor;

    // Fog
    float dist = length(view_space);
    float fogFactor = 1. / exp(pow(dist * FogDensity, 2));
    fogFactor = clamp(fogFactor, 0.05, 1);

    vec3 finalColor = mix(fogColor, color, fogFactor);
    out_color = vec4(finalColor, 1);
}