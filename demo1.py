from panda3d.core import loadPrcFileData
loadPrcFileData("", "show-buffers 0")
loadPrcFileData("", "show-frame-rate-meter  1")
loadPrcFileData("", "sync-video 0")
from panda3d.core import *
from direct.showbase import ShowBase
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import *
import random

class Demo():
    def __init__(self):       
        #setup
        size=512 #size of the wave buffer
        self.update_speed=1.0/60.0 #the waves only look good when generated at this constant rate (1/60=60fps)
       
        
        base = ShowBase.ShowBase()        
        base.cam.setPos(128, -128, 80)
        base.cam.lookAt(128, 128, 0)
        
        #wave source buffer
        self.wave_source=self.makeBuffer(size=256, texFilter=Texture.FTNearest)
        self.wave_source['quad'].setColor(0,0,0, 0)
        self.wave_source['quad'].setZ(-10)
        
        #a normal, animated actor
        visible_panda=self.makeWalkingPanda(render)
        
        #a copy of the panda, but rendered offscreen
        phantom_panda=self.makeWalkingPanda(self.wave_source['root'])
        #the pahnatom panda needst to be clipped at the water level
        clip_plane = Plane(Vec3(0, 0, -1), Point3(0, 0, 1.0))
        plane_node = PlaneNode("clip")
        plane_node.setPlane(clip_plane)
        plane_path = render.attachNewNode(plane_node)
        phantom_panda.setClipPlane(plane_path)
        #we also remove the texture, and paint it red
        phantom_panda.setTextureOff(1)
        phantom_panda.setColor(1.0, 0.0, 0.0, 0.0) 
        #finaly draw it insideout
        phantom_panda.setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullCounterClockwise))
        
        #make the ping-pong buffer to draw the water waves
        #shader 2 makes no use of the wave_source texture, appart from that they are identical
        shader1=Shader.load(Shader.SL_GLSL,'v.glsl', 'make_wave_f.glsl')
        shader2=Shader.load(Shader.SL_GLSL,'v.glsl', 'make_wave2_f.glsl')
        
        self.ping=self.makeBuffer(shader1, size)
        self.pong=self.makeBuffer(shader2, size)        
        
        self.ping['quad'].setShaderInput("size",float(size))
        self.pong['quad'].setShaderInput("size",float(size))
        
        self.ping['quad'].setTexture(self.pong['tex'])
        self.pong['quad'].setTexture(self.ping['tex'])        

        self.ping['quad'].setShaderInput('startmap', self.wave_source['tex'])
        
        self.ping['buff'].setActive(True)
        self.pong['buff'].setActive(False)   
        
        #some vars to track the state of things
        self.time=0
        self.state=0
        
        #preview   
        cm = CardMaker("plane")
        cm.setFrame(0, 256, 0, 256)
        self.preview_plane=render.attachNewNode(cm.generate())
        self.preview_plane.setShader(Shader.load(Shader.SL_GLSL,'v.glsl','prev.glsl'))
        self.preview_plane.setShaderInput("size",float(size))
        self.preview_plane.setTexture(self.pong['tex'])
        self.preview_plane.setLightOff()
        self.preview_plane.lookAt(0, 0, -1)
        self.preview_plane.setPos(0,0,1.0)
        #self.preview_plane.hide()
     
        #update task
        taskMgr.add(self.update, 'update', sort=51) 
        
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
        
    def makeWalkingPanda(self, root, pos=(64,128, 0), axis_pos=(128, 128, 0),  scale=0.02, time=90.0):
        axis = root.attachNewNode('axis')
        axis.setPos(axis_pos)
        actor = Actor('panda-model', {'walk': 'panda-walk4'})
        actor.setPos(pos)
        actor.wrtReparentTo(axis)        
        actor.setScale(scale)
        walk = actor.actorInterval('walk', playRate=1.3)
        walk.loop()
        axis.hprInterval(time, LPoint3(360, 0, 0), startHpr=LPoint3(0, 0, 0)).loop()
        return actor
        
d=Demo()
base.run()


