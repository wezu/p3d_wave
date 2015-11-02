//GLSL
#version 140
uniform sampler2D p3d_Texture0;
uniform sampler2D startmap;
in vec2 uv; 
uniform float size;

void main()
    {    
    float pixel =1.0/size;    
    //vec4 final=texture(p3d_Texture0,uv); //not needed       
    vec4 final=vec4(0.0, 0.0, 0.0, 0.0);
    final+=texture(p3d_Texture0, vec2(uv.x+pixel,uv.y));    
    final+=texture(p3d_Texture0, vec2(uv.x-pixel,uv.y));    
    final+=texture(p3d_Texture0, vec2(uv.x,uv.y+pixel)); 
    final+=texture(p3d_Texture0, vec2(uv.x,uv.y-pixel));       
    final*=0.4;    
    final.g+=final.r*0.01;   //wave thickness, bigger number=thiner wave 
    final.r-=0.01;//range of the wave, bigger number=smaller range   
    //remove the old data 
    final*=step(0.001, clamp(final.r-final.g, 0.0, 1.0));
    //add new data
    final+=texture(startmap,uv);
    
    gl_FragData[0]=final;   
    }
    
