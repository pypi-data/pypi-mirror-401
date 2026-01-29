from direct.showbase.ShowBase import ShowBase
from panda3d.core import LPoint3, LVector3, BitMask32, NodePath
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import WindowProperties
from panda3d.core import LineSegs

import math
import os

try:
    # Python 3.9+
    from importlib import resources
except ImportError:
    # 兼容旧版本
    import pkg_resources
    resources = None

# 尝试导入gltf模块用于加载glb文件
try:
    from gltf import load_model
    GLTF_AVAILABLE = True
except ImportError:
    GLTF_AVAILABLE = False

class Color():
    red=(1,0,0,1)
    green=(0,1,0,1)
    blue=(0,0,1,1)
    yellow=(1,1,0,1)
    cyan=(0,1,1,1)
    pink=(255/255, 102/255, 255/255, 1)
    brown=(102/255, 51/255, 255/255, 1)
    purple=(150/255, 102/255, 255/255, 1)
    orange=(255/255, 102/255, 0/255, 1)
    tan=(221/255, 201/255, 168/255, 1)
    gray=(80/255, 80/255, 80/255, 1)
    white=(1,1,1,1)
    black=(0,0,0,1)
    
class CameraController:
    """摄像机控制工具类，实现围绕目标旋转等功能"""
    
    def __init__(self, base, target_pos=LPoint3(0, 0, 0), radius=10):
        self.base = base
        self.target_pos = target_pos  # 注视目标位置
        self.radius = radius          # 旋转半径
        self.theta = 45                # 水平旋转角度(绕Y轴)
        self.phi = 45                 # 垂直旋转角度(绕X轴)，初始稍微向上
        
        # 禁用默认的鼠标控制
        self.base.disableMouse()
        
        # 设置初始摄像机位置
        self.update_camera_position()
        
        # 鼠标状态变量
        self.mouse_down = False
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        
        # 绑定鼠标事件
        self.base.accept("mouse1", self.on_mouse_down)
        self.base.accept("mouse1-up", self.on_mouse_up)
        self.base.taskMgr.add(self.update_mouse, "UpdateMouseTask")
        
        # 绑定键盘事件用于调整半径
        self.base.accept("wheel_up", self.decrease_radius)
        self.base.accept("wheel_down", self.increase_radius)
    
    def on_mouse_down(self):
        """鼠标按下事件处理"""
        self.mouse_down = True
        self.last_mouse_x = self.base.mouseWatcherNode.getMouseX()
        self.last_mouse_y = self.base.mouseWatcherNode.getMouseY()
    
    def on_mouse_up(self):
        """鼠标释放事件处理"""
        self.mouse_down = False
    
    def update_mouse(self, task):
        """鼠标移动更新任务"""
        if self.mouse_down and self.base.mouseWatcherNode.hasMouse():
            # 获取当前鼠标位置
            x = self.base.mouseWatcherNode.getMouseX()
            y = self.base.mouseWatcherNode.getMouseY()
            
            # 计算鼠标移动差值
            dx = x - self.last_mouse_x
            dy = y - self.last_mouse_y
            
            # 更新旋转角度 (敏感度控制)
            self.theta += dx * 100  # 水平旋转
            self.phi += dy * 100    # 垂直旋转
            
            # 限制垂直旋转角度，避免过度翻转
            self.phi = max(5, min(85, self.phi))
            
            # 更新摄像机位置
            self.update_camera_position()
            
            # 保存当前鼠标位置
            self.last_mouse_x = x
            self.last_mouse_y = y
        
        return task.cont
    
    def update_camera_position(self):
        """根据角度和半径更新摄像机位置"""
        # 将角度转换为弧度
        theta_rad = math.radians(self.theta)
        phi_rad = math.radians(self.phi)
        
        # 计算摄像机在球坐标系中的位置
        x = self.target_pos.x + self.radius * math.sin(phi_rad) * math.sin(theta_rad)
        y = self.target_pos.y + self.radius * math.sin(phi_rad) * math.cos(theta_rad)
        z = self.target_pos.z + self.radius * math.cos(phi_rad)
        
        # 设置摄像机位置
        self.base.camera.setPos(x, y, z)
        
        # 让摄像机看向目标点
        self.base.camera.lookAt(self.target_pos)
    
    def set_target(self, new_target):
        """设置新的注视目标"""
        self.target_pos = LPoint3(new_target)
        self.update_camera_position()
    
    def set_radius(self, new_radius):
        """设置新的旋转半径"""
        if new_radius > 0:  # 确保半径为正数
            self.radius = new_radius
            self.update_camera_position()
    
    def increase_radius(self):
        """增加旋转半径"""
        self.set_radius(self.radius + 0.5)
    
    def decrease_radius(self):
        """减小旋转半径"""
        self.set_radius(max(1, self.radius - 0.5))  # 最小半径为1


class XKD(ShowBase):
    def __init__(self,showAxis=True):
        ShowBase.__init__(self)
        print("嗨,星空吾星3D编程欢迎您!促进儿童编程发展意见请mailTo:airfly000@163.com")
        properties = WindowProperties()
        properties.setTitle("星空吾星3D编程")#set window title
        properties.setSize(1000, 750)
        self.win.requestProperties(properties)

        # 设置背景色，RGB值范围0-1
        self.setBackgroundColor(51/255, 153/255, 204/255)  #天空蓝
        
        # 创建场景内容
        self.setup_scene(showAxis)
        
        # 创建摄像机控制器
        self.camera_controller = CameraController(self, LPoint3(0, 0, 0), 40)

        self.update=None

        self.taskMgr.add(self.updateScene, "updateSceneTask")
        
    def _get_resource_path(self, filename):
        """获取包内资源的完整路径"""
        try:
            if resources is not None:
                # Python 3.9+
                with resources.as_file(resources.files("xkd").joinpath(filename)) as path:
                    return str(path)
            else:
                # 兼容旧版本
                return pkg_resources.resource_filename("xkd", filename)
        except Exception as e:
            # 如果获取包内资源失败，尝试从当前目录加载
            return filename
    
    def setup_scene(self,showAxis=True):
        """设置演示场景"""
        if not showAxis: #不显示坐标轴
            return
        axis=self.loader.loadModel("zup-axis")
        axis.setScale(1,1,1)
        axis.reparentTo(self.render)
        
        
    def addBall(self,pos,color=(1,1,1,0),scale=(1,1,1)):
        obj=self.loader.loadModel("smiley")
        obj.setPos(pos)
        obj.setColor(color)
        obj.setScale(scale[0],scale[1],scale[2])
        obj.reparentTo(self.render)
        return obj

    def addBox(self,pos,color=(1,1,1,0),scale=(1,1,1)):
        obj=self.loader.loadModel("box")
        obj.setPos(pos)
        obj.setColor(color)
        obj.setScale(scale[0],scale[1],scale[2])
        obj.reparentTo(self.render)
        return obj

    #从程序当前目录或panda3d/models加载模型,如obj,glb,返回模型对应的模型
    def cm(self,fn,nc=True):#fn是带扩展名的文件名
        b=self.loader.loadModel(fn,noCache=nc)
        b.reparentTo(self.render)
        return b

    #加载obj文件返回模型,比getObj要简化
    def om(self,fileName,nc=True):
        if not(".obj" in fileName):#自动加上.obj文件名
            fileName=fileName+".obj"
        obj_path = self._get_resource_path(fileName)
        b=self.loader.loadModel(obj_path,noCache=nc)
        b.reparentTo(self.render)
        return b
    
    #加载glb文件返回模型Node
    def gm(self,fileName,nc=True):
        if not(".glb" in fileName):#自动加上.glb文件名
            fileName=fileName+".glb"
        obj_path = self._get_resource_path(fileName)
        
        if GLTF_AVAILABLE and obj_path.endswith(".glb"):
            # 使用gltf模块加载glb文件
            try:
                model_root = load_model(obj_path)
                b = NodePath(model_root)
            except Exception as e:
                print(f"使用gltf模块加载{fileName}失败，尝试使用默认加载器: {e}")
                b = self.loader.loadModel(obj_path,noCache=nc)
        else:
            # 使用默认加载器
            b = self.loader.loadModel(obj_path,noCache=nc)
            
        b.reparentTo(self.render)
        return b
    
    # 重写loader.loadModel方法，自动支持包内资源加载
    def loadModel(self, modelPath, noCache=False):
        fullPath = self._get_resource_path(modelPath)
        
        if GLTF_AVAILABLE and fullPath.endswith(".glb"):
            # 使用gltf模块加载glb文件
            try:
                model_root = load_model(fullPath)
                return NodePath(model_root)
            except Exception as e:
                print(f"使用gltf模块加载{modelPath}失败，尝试使用默认加载器: {e}")
                # 回退到默认加载器
        
        # 使用默认加载器
        return self.loader.loadModel(fullPath, noCache=noCache)

    #更新场景
    def updateScene(self, task):
        if self.update !=None:
            self.update()
        return task.cont

#Pen类，绘制线条
class Pen(LineSegs):
    
    def __init__(self,app):
        super().__init__()
        self.np=app.render.attachNewNode("linesCtn")#线条容器
        self.lineNode=None #线条结点

    def lineTo(self,x,y,z):
        self.drawTo(x,y,z)

    def color(self,c):
        self.setColor(c)

    def size(self,n):
        self.setThickness(n)

    def clear(self):
        self.reset()#Removes any lines in progress and resets to the initial empty state.
        self.np.get_children().detach()#np清空

    def update(self):
        self.lineNode=self.np.attachNewNode(self.create())#重新添加线条结点

    



        
