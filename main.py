from panda3d.core import loadPrcFileData
#loadPrcFileData("", "show-buffers 1")
loadPrcFileData("", "show-frame-rate-meter  1")
loadPrcFileData("", "sync-video 1")
from panda3d.core import *
from direct.showbase import ShowBase

class Demo():
    def __init__(self):       
        #config here:
        size=512 #size of the buffer, bigger number=smaller waves
        update_speed=0.01 #how often the buffors get fliped, set to 0.01 for 60fps, 0.04 for ~500fps
        reset_time=1.5 #how often the buffers are reset to the default state (re-run the wave generation)
        
        base = ShowBase.ShowBase()
               
        wave_shader=Shader.load(Shader.SL_GLSL,'v.glsl', 'make_wave_f.glsl')
        
        self.ping=self.makeBuffer(wave_shader, size)
        self.pong=self.makeBuffer(wave_shader, size)
        
        self.ping['quad'].setShaderInput("size",float(size))
        self.pong['quad'].setShaderInput("size",float(size))
        
        self.ping['quad'].setTexture(self.pong['tex'])
        self.pong['quad'].setTexture(self.ping['tex'])
        
        self.ping['quad'].setShaderInput('startmap', loader.loadTexture('startmap256.png'))
        self.pong['quad'].setShaderInput('startmap', loader.loadTexture('startmap256.png'))
        
        self.ping['quad'].setShaderInput('use_startmap', 1.0)
        self.pong['quad'].setShaderInput('use_startmap', 0.0)
        
        self.ping['buff'].setActive(True)
        self.pong['buff'].setActive(False)        

        #preview   
        cm = CardMaker("plane")
        cm.setFrame(-10, 10, -10, 10)
        self.preview_plane=render.attachNewNode(cm.generate())
        self.preview_plane.setShader(Shader.load(Shader.SL_GLSL,'v.glsl','prev.glsl'))
        self.preview_plane.setTexture(self.pong['tex'])
        self.preview_plane.setLightOff()
        self.preview_plane.setPos(0,30,0)

        self.state=0
        #taskMgr.add(self.update, 'update', sort=51)
        taskMgr.doMethodLater(update_speed, self.update, 'update', sort=51)
        taskMgr.doMethodLater(reset_time, self.updateMap, 'update_map')
        
    def makeBuffer(self, shader, size=256):
        root=NodePath("bufferRoot")
        tex=Texture()
        tex.setWrapU(Texture.WMClamp)
        tex.setWrapV(Texture.WMClamp)
        buff=base.win.makeTextureBuffer("buff", size, size, tex)
        #the camera for the buffer
        cam=base.makeCamera(win=buff)
        cam.reparentTo(root)          
        cam.setPos(size/2,size/2,100)                
        cam.setP(-90)                   
        lens = OrthographicLens()
        lens.setFilmSize(size, size)  
        cam.node().setLens(lens)          
        #plane with the texture
        cm = CardMaker("plane")
        cm.setFrame(0, size, 0, size)        
        quad=root.attachNewNode(cm.generate())
        quad.lookAt(0, 0, -1)      
        ShaderAttrib.make(shader)  
        quad.setAttrib(ShaderAttrib.make(shader))
        #return all the data in a dict
        return{'root':root, 'tex':tex, 'buff':buff, "cam":cam, 'quad':quad}
        
    def updateMap(self, task):
        self.ping['quad'].setShaderInput('use_startmap', 1.0)
        return task.again   
         
    def update(self, task): 
        if self.state==0:
            self.state=1            
            self.ping['buff'].setActive(False)
            self.pong['buff'].setActive(True)             
            #self.ping['quad'].setTexture(self.pong['tex']) #?
            self.ping['quad'].setShaderInput('use_startmap', 0.0)
            self.preview_plane.setTexture(self.pong['tex'])
        else:
            self.state=0
            self.ping['buff'].setActive(True)
            self.pong['buff'].setActive(False)             
            self.preview_plane.setTexture(self.ping['tex'])           
        return task.again

d=Demo()
base.run()


