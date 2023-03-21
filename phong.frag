#version 330 core

// fragment position and normal of the fragment, in WORLD coordinates
// (you can also compute in VIEW coordinates, your choice! rename variables)
in vec3 w_position, w_normal;   // in world coodinates

// light dir, in world coordinates
uniform vec3 light_dir;

// material properties
uniform vec3 k_d;
uniform vec3 k_s;
uniform vec3 k_a;
uniform float s;

// world camera position
uniform vec3 w_camera_position;

// output fragment color for OpenGL
out vec4 out_color;

void main() {
    vec3 w_normal_normalized = normalize(w_normal);

    vec3 ambiant = k_d * max(0, dot(light_dir, w_normal_normalized));
    
    vec3 r = reflect(-light_dir, w_normal_normalized);
    vec3 v = normalize(w_camera_position - w_position);
    vec3 specular = k_s * pow(max(0, dot(r, v)), s);

    out_color = vec4(k_a + specular + ambiant, 1);
    
}
