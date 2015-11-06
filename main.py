from panda3d.core import loadPrcFileData
loadPrcFileData("", "show-buffers 0")
loadPrcFileData("", "show-frame-rate-meter  1")
loadPrcFileData("", "sync-video 0")
from panda3d.core import *
from direct.showbase import ShowBase
import random

class Demo():
    def __init__(self):       
        #config here:
        size=512 #size of the buffer, bigger number=smaller waves
        self.update_speed=1.0/60.0 #how often the buffors get fliped, set to 0.01 for 60fps, 0.04 for ~500fps
        #reset_time=0.02 #how often the buffers are reset to the default state (re-run the wave generation)
        
        base = ShowBase.ShowBase()             
               
        wave_shader=Shader.load(Shader.SL_GLSL,'v.glsl', 'make_wave_f.glsl')
        wave_shader2=Shader.load(Shader.SL_GLSL,'v.glsl', 'make_wave2_f.glsl')
        
        self.ping=self.makeBuffer(wave_shader, size)
        self.pong=self.makeBuffer(wave_shader2, size)
        self.birth=self.makeBuffer(size=256, texFilter=Texture.FTNearest)
        self.birth['quad'].setColor(0,0,0, 0)
        
        self.ping['quad'].setShaderInput("size",float(size))
        self.pong['quad'].setShaderInput("size",float(size))
        
        self.ping['quad'].setTexture(self.pong['tex'])
        self.pong['quad'].setTexture(self.ping['tex'])        

        self.ping['quad'].setShaderInput('startmap', self.birth['tex'])
        
        self.ping['buff'].setActive(True)
        self.pong['buff'].setActive(False)        

        #preview   
        cm = CardMaker("plane")
        cm.setFrame(-10, 10, -10, 10)
        self.preview_plane=render.attachNewNode(cm.generate())
        self.preview_plane.setShader(Shader.load(Shader.SL_GLSL,'v.glsl','prev.glsl'))
        self.preview_plane.setShaderInput("size",float(size))
        self.preview_plane.setTexture(self.pong['tex'])
        self.preview_plane.setLightOff()
        self.preview_plane.setPos(0,30,0)

        self.state=0
        self.map_state=0
        self.time=0.0
        self.spawns=[]
        self.doHide=False
        cm.setFrame(-0.5, 0.5, -0.5, 0.5)
        for i in range(10):
            self.spawns.append(self.birth['root'].attachNewNode(cm.generate()))    
            self.spawns[-1].setColor(0.2, 0.1, 0.0, 0.0)            
            self.spawns[-1].lookAt(0, 0, -1)
            self.spawns[-1].setZ(10)
            #self.spawns[-1].hide()
            
        self.mouse_spawn=self.birth['root'].attachNewNode(cm.generate())    
        self.mouse_spawn.setColor(1.0, 0.0, 0.0, 0.0)            
        self.mouse_spawn.lookAt(0, 0, -1)  
        self.mouse_spawn.setZ(10)
        self.plane = Plane(Point3(10, 30, 10), Point3(-10, 30, 10), Point3(-10, 30, -10))     
            
       
        taskMgr.add(self.update, 'update', sort=51)
        taskMgr.add(self.mouseUpdate, "mouseUpdate")
        taskMgr.doMethodLater(0.01, self.updateMap, "updateMap")
        
    def updateMap(self, task):                  
        for spawn in self.spawns:        
            spawn.setPos(random.randrange(0, 255),random.randrange(0, 255), 1.0)
            spawn.setColor(random.uniform(0.5, 0.1), 0.05, 0.0, 0.0)
        return task.again  
            
    def mouseUpdate(self, task):
        if base.mouseWatcherNode.hasMouse():
            mpos = base.mouseWatcherNode.getMouse()
            pos3d = Point3()
            nearPoint = Point3()
            farPoint = Point3()
            base.camLens.extrude(mpos, nearPoint, farPoint)
            if self.plane.intersectsLine(pos3d, render.getRelativePoint(camera, nearPoint),render.getRelativePoint(camera, farPoint)):
                #print pos3d
                self.mouse_spawn.setX(int((pos3d[0]+10.0)*12.8))
                self.mouse_spawn.setY(int((pos3d[2]+10.0)*12.8))
            #self.spawns[0].setZ(10)            
        return task.again
            
    def makeBuffer(self, shader=None, size=256, texFilter=Texture.FTLinearMipmapLinear):
        root=NodePath("bufferRoot")
        tex=Texture()
        tex.setWrapU(Texture.WMClamp)
        tex.setWrapV(Texture.WMClamp)
        tex.setMagfilter(texFilter)
        tex.setMinfilter(texFilter)
        props = FrameBufferProperties()
        props.setRgbaBits(16, 16, 0, 0)
        props.setSrgbColor(False)        
        buff=base.win.makeTextureBuffer("buff", size, size, tex, fbp=props)
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
        if shader:
            ShaderAttrib.make(shader)  
            quad.setAttrib(ShaderAttrib.make(shader))
        #return all the data in a dict
        return{'root':root, 'tex':tex, 'buff':buff, "cam":cam, 'quad':quad}        
            
    def update(self, task):   
        dt=globalClock.getDt()
        self.time+=dt
        if self.time>=self.update_speed:
            self.time=0            
            if self.state==0:            
                self.state=1            
                self.ping['buff'].setActive(False)
                self.pong['buff'].setActive(True)    
                self.preview_plane.setTexture(self.pong['tex']) 
            else:
                self.state=0
                self.ping['buff'].setActive(True)
                self.pong['buff'].setActive(False)             
                self.preview_plane.setTexture(self.ping['tex'])           
        else:
            self.ping['buff'].setActive(False)
            self.pong['buff'].setActive(False) 
        return task.again

d=Demo()
base.run()


