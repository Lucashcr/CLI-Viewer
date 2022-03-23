import glm

class Camera():
    def __init__(self, ContextWidth, ContextHeight):
        self.Target = glm.vec3(0,0,0)
        self.Location = glm.vec3(0,0,3)
        self.Up = glm.vec3(0,1,0)

        self.FoV = glm.radians(45.)
        self.AspRatio = ContextWidth / ContextHeight
        self.Near = 0.01
        self.Far = 100.
        
        self.ModelMatrix = glm.identity(glm.mat4)
    
    def GetViewMatrix(self):
        return glm.lookAt(self.Location, self.Target, self.Up)

    def GetNormalMatrix(self):
        return glm.transpose(glm.inverse(self.GetViewMatrix() * self.ModelMatrix))

    def GetMVP(self):
        self.ViewMatrix = self.GetViewMatrix()
        self.ProjectionMatrix = glm.perspective(self.FoV, self.AspRatio, self.Near, self.Far)
        return self.ProjectionMatrix * self.ViewMatrix * self.ModelMatrix

    def MoveHAxis(self, amount):
        right = glm.cross((self.Target - self.Location), self.Up) 
        self.Location -= right * amount * 0.001
        self.Target -= right * amount * 0.001
    
    def MoveVAxis(self, amount):
        up = glm.cross(glm.cross((self.Target - self.Location), self.Up), self.Location - self.Target)
        self.Location -= up * amount * 0.001
        self.Target -= up * amount * 0.001

    def RotHAxis(self, amount):
        self.Location = glm.rotateZ(self.Location, -glm.radians(amount)*0.1)

    def RotVAxis(self, amount):
        self.Location.z -= self.Z/2
        self.Location = glm.rotate(self.Location, glm.radians(amount)*0.1, glm.cross(self.Up, (self.Target-self.Location)))
        self.Location.z += self.Z/2

    def Zoom(self, amount):
        self.Location -= self.Location * amount / 1200
        self.Target -= self.Target * amount / 1200
        
    def Resize(self, ContextWidth, ContextHeight):
        self.AspRatio = ContextWidth / ContextHeight
        self.ProjectionMatrix = glm.perspective(self.FoV, self.AspRatio, self.Near, self.Far)
