#version 330 core

uniform float time;
uniform vec2 resolution;
uniform sampler2D tex;

out vec4 out_color;

void main(void) {
vec2 cPos = -1.0 + 2.0 * gl_FragCoord.xy / resolution.xy;
float cLength = length(cPos);

vec2 uv = gl_FragCoord.xy/resolution.xy+(cPos/cLength)*cos(cLength*12.0-time*4.0)*0.03;
vec3 col = texture2D(tex,uv).xyz;

out_color = vec4(col,1.0);
}
