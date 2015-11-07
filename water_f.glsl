//GLSL
#version 140
uniform sampler2D p3d_Texture0;
uniform sampler2D normal_map;
uniform sampler2D reflection;
uniform mat3 p3d_NormalMatrix;
in vec2 uv; 
in vec2 time_uv1;
in vec2 time_uv2;
in vec4 reflect_uv;
in vec4 vpos;
uniform float size;

in vec4 pointLight [8];
uniform vec4 light_color[8];
uniform float num_lights;

void main()
    {    
    vec3 norm=vec3(0.0,0.0,1.0);    
    vec3 vLeft=vec3(1.0,0.0,0.0);     
    float pixel =1.0/size; 
    //normal vector...
    vec4 me=texture(p3d_Texture0,uv);
    vec4 n=texture(p3d_Texture0, vec2(uv.x,uv.y+pixel)); 
    vec4 s=texture(p3d_Texture0, vec2(uv.x,uv.y-pixel));   
    vec4 e=texture(p3d_Texture0, vec2(uv.x+pixel,uv.y));    
    vec4 w=texture(p3d_Texture0, vec2(uv.x-pixel,uv.y));
    //find perpendicular vector to norm:        
    vec3 temp = norm; //a temporary vector that is not parallel to norm    
    temp.x+=0.5;
    //form a basis with norm being one of the axes:
    vec3 perp1 = normalize(cross(norm,temp));
    vec3 perp2 = normalize(cross(norm,perp1));
    //use the basis to move the normal in its own space by the offset                       
    norm -=(((n.r-me.r)-(s.r-me.r))*perp1 - ((e.r-me.r)-(w.r-me.r))*perp2);
    //norm +=(((n.g-me.g)-(s.g-me.g))*perp1 - ((e.g-me.g)-(w.g-me.g))*perp2);
    //norm+=texture(normal_map,time_uv1).rgb*2.0-1.0;
    //norm+=texture(normal_map,time_uv2).rgb*2.0-1.0;
    //norm = normalize(p3d_NormalMatrix*norm); 
    //TBN
    vec3 N= p3d_NormalMatrix *  normalize(norm);
    vec3 T=  p3d_NormalMatrix * cross(N, vLeft);  
    vec3 B= p3d_NormalMatrix * cross(N, T);
    
    vec3 tsnormal =( texture(normal_map,time_uv1).rgb*2.0-1.0);    
    tsnormal += (texture(normal_map,time_uv2).rgb*2.0-1.0);    
    tsnormal=normalize(tsnormal);
    N*= tsnormal.z;
    N += T * tsnormal.x;
    N -= B * tsnormal.y;	
    N = normalize(N);
    
    //norm=norm*0.5+0.5;
    
   //lights   
    vec4 color =vec4(0.0, 0.0, 0.0, 0.0);    
    vec3 L;
    float NdotL;
    float spec=0.0;
    float att;
    float dist;
    int iNumLights = int(num_lights);
    for (int i=0; i<iNumLights; ++i)
        {  
        dist=distance(vpos.xyz, pointLight[i].xyz);
        dist*=dist;            
        att = clamp(1.0 - dist/(pointLight[i].w), 0.0, 1.0);            
        if (att>0.0)
            {      
            L = normalize(pointLight[i].xyz-vpos.xyz);
            NdotL = max(dot(N,L),0.0);
            if (NdotL > 0.0)
                {              
                spec+=pow( max(dot(reflect(-L.xyz, N.xyz),normalize(-vpos.xyz)), 0.0),200.0);
                color += light_color[i]* NdotL*0.3;
                }
            }
        }     
    //color+=spec;
    vec4 refl=textureProj(reflection, reflect_uv+vec4(N*2.0-1.0, 0.0));
    gl_FragData[0]=refl+refl*color+spec;  
    }
    
