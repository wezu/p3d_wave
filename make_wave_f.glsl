//GLSL
#version 140
uniform sampler2D p3d_Texture0;
uniform sampler2D startmap;
in vec2 uv; 
uniform float size;
uniform float use_startmap;
//uniform float osg_DeltaFrameTime;

void main()
    {    
    float pixel =1.0/size;
    //float delta=osg_DeltaFrameTime*1000.0;
    vec4 final=texture(p3d_Texture0,uv);    
    //vec4 final=vec4(0.0,0.0,0.0,0.0); 
    final+=texture(p3d_Texture0, vec2(uv.x+pixel,uv.y));    
    final+=texture(p3d_Texture0, vec2(uv.x-pixel,uv.y));    
    final+=texture(p3d_Texture0, vec2(uv.x,uv.y+pixel)); 
    final+=texture(p3d_Texture0, vec2(uv.x,uv.y-pixel));       
    final*=0.4;    
    final.g+=final.r*0.01;    
    final.r-=0.01;
    final=mix(final,texture(startmap,uv), use_startmap);
    gl_FragData[0]=final;   
    }
    
