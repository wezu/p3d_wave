//GLSL
#version 140
uniform sampler2D p3d_Texture0;
uniform sampler2D startmap;
in vec2 uv; 
uniform float size;

void main()
    {    
    float pixel =1.0/size;  
    vec4 final=texture(startmap,uv);    
    final+=texture(p3d_Texture0,uv); 
    final+=texture(p3d_Texture0, vec2(uv.x+pixel,uv.y));    
    final+=texture(p3d_Texture0, vec2(uv.x-pixel,uv.y));    
    final+=texture(p3d_Texture0, vec2(uv.x,uv.y+pixel)); 
    final+=texture(p3d_Texture0, vec2(uv.x,uv.y-pixel));       
    final*=0.3; 
    if  (final.r>0.0)
        {
        final.g+=0.0009;
        //final.g+=0.02;
        final.r*=clamp((1.0-final.g),0.2, 1.0);   
        }  
    //remove the old data 
    //if (final.g>final.r)
    //    final=vec4(0.0, 0.0, 0.0, 0.0);
    final*=step(0.001, clamp(final.r-final.g, 0.0, 1.0));    
    
    gl_FragData[0]=final;       
    }
    
