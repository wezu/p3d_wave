//GLSL
#version 140
uniform sampler2D p3d_Texture0;
in vec2 uv; 
uniform float size;

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
    norm +=(((n.r-me.r)-(s.r-me.r))*perp1 - ((e.r-me.r)-(w.r-me.r))*perp2);
    //norm +=(((n.g-me.g)-(s.g-me.g))*perp1 - ((e.g-me.g)-(w.g-me.g))*perp2);
    norm = normalize(norm); 
    norm=norm*0.5+0.5;
    gl_FragData[0]=vec4(norm,1.0);  
    }
    
