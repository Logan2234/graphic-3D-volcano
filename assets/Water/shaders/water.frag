#version 330 core

uniform vec3 w_camera_position;
uniform samplerCube skybox;
uniform sampler2D tex;

// In for light calculations
in vec3 out_normal;
in vec3 out_position;
in vec2 frag_tex_coords;
in vec4 view_space;

const vec3 lightColor = vec3(1, 1, 1);
const float K_a = 0.8;
const float K_s = 0.8;
const float K_d = 1 - K_s;

// Fog
const vec3 fogColor = vec3(.7, .7, .7);
const float FogDensity = .0005;

out vec4 out_color;

void main() {
    vec3 I = normalize(out_position - w_camera_position);
    vec3 R = reflect(I, normalize(out_normal));

    // Coloured version with reflecton
    // vec4 tex_color = mix(vec4(texture(skybox, R).rgb, 1), vec4(0.18, 0.49, 0.65, 1.0), 0.7);

    // Textured version with reflection
    vec4 tex_color = mix(texture(skybox, R), texture(tex, frag_tex_coords), 0.5);

    // Textured version with work on normal
    // vec4 tex_color = mix(texture(tex, frag_tex_coords), vec4(0.23, 0.54, 0.70, 1), out_normal.z * 0.8);

    /**************** Light calculation *****************/

    // Ambient
    vec3 ambient = K_a * lightColor;

    // Diffuse
    vec3 norm = normalize(out_normal);
    vec3 lightDir = normalize(vec3(0.5, 0.5, 1)); // Approx of sunlight pos

    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = K_d * diff * lightColor;

    // Specular
    vec3 viewDir = normalize(w_camera_position - out_position);
    vec3 reflectDir = normalize(reflect(-lightDir, norm));

    float spec = pow(max(dot(viewDir, reflectDir), 0), 128);
    vec3 specular = K_s * spec * lightColor;

    vec3 color = (specular + diffuse + ambient) * tex_color.rgb;

    // Fog
    float dist = length(view_space);
    float fogFactor = 1. / exp(pow(dist * FogDensity, 2));
    fogFactor = clamp(fogFactor, 0.05, 1.);

    vec3 finalColor = mix(fogColor, color, fogFactor);
    out_color = vec4(finalColor, 1);
}
