//fog fragment shader
//................!!!.......................
//if you decided how to compute fog distance
//and you want to use only one fog equation
//you don't have to use those if statements
//Here is a tutorial and I want to show
//different possibilities
//.........................................
#version 330
out vec4 out_color;

// uniform vec3 light_position;
uniform vec3 w_camera_position;

uniform sampler2D tex;
uniform sampler2D tex2;

//0 linear; 1 exponential; 2 exponential square
// uniform int fogSelector;
//0 plane based; 1 range based
// uniform int depthFog;

//can pass them as uniforms
const vec3 light_position=vec3(0, -1, 0);
const vec3 DiffuseLight=vec3(.15,.05,0.);
const vec3 RimColor=vec3(.2,.2,.2);

//from vertex shader
in vec3 frag_pos;
in vec3 out_normal;
in vec4 viewSpace;
in vec2 frag_tex_coords;

//0 linear; 1 exponential; 2 exponential square
const int fogSelector = 1;
//0 plane based; 1 range based
const int depthFog = 0;
const vec3 fogColor=vec3(.7,.7,.7);
const float FogDensity=.005;

void main(){

    vec4 tex1 = texture(tex, frag_tex_coords);
    vec4 tex2 = texture(tex2, frag_tex_coords);

    //get light an view directions
    vec3 L = normalize(light_position - frag_pos);
    vec3 V = normalize(w_camera_position - frag_pos);

    //diffuse lighting
    vec3 diffuse = DiffuseLight * max(0, dot(L, out_normal));

    //rim lighting
    float rim = 1 - max(dot(V, out_normal), 0.);
    rim=smoothstep(.6,1.,rim);
    vec3 finalRim=RimColor*vec3(rim,rim,rim);
    //get all lights and texture
    vec3 mix_tex = mix(tex1.rgb, tex2.rgb, tex2.a).rgb;
    vec3 lightColor=finalRim+diffuse+mix_tex;

    vec3 finalColor=vec3(0,0,0);

    //distance
    float dist=0;
    float fogFactor=0;

    //compute distance used in fog equations
    if(depthFog==0)//select plane based vs range based
    {
        //plane based
        dist=abs(viewSpace.z);
        //dist = (gl_FragCoord.z / gl_FragCoord.w);
    }
    else
    {
        //range based
        dist=length(viewSpace);
    }

    if(fogSelector==0)//linear fog
    {
        // 20 - fog starts; 80 - fog ends
        fogFactor=(80-dist)/(80-20);
        fogFactor=clamp(fogFactor,0.,1.);

        //if you inverse color in glsl mix function you have to
        //put 1.0 - fogFactor
        finalColor=mix(fogColor,lightColor,fogFactor);
    }
    else if(fogSelector==1)// exponential fog
    {
        fogFactor=1./exp(dist*FogDensity);
        fogFactor=clamp(fogFactor,0.,1.);

        // mix function fogColor⋅(1−fogFactor) + lightColor⋅fogFactor
        finalColor=mix(fogColor,lightColor,fogFactor);
    }
    else if(fogSelector==2)
    {
        fogFactor=1./exp((dist*FogDensity)*(dist*FogDensity));
        fogFactor=clamp(fogFactor,0.,1.);

        finalColor=mix(fogColor,lightColor,fogFactor);
    }

    // show fogFactor depth(gray levels)
    // fogFactor = 1 - fogFactor;
    // out_color = vec4(fogFactor, fogFactor, fogFactor, 1.0);
    out_color = vec4(finalColor, 1);
}