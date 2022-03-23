import glm, ctypes
import OpenGL.GL as gl

from classes.OpenGLutils import *

class Mesh:
    normals = list()
    def __init__(self, vertices, faces):
        self.vertices = glm.array([v.position for v in vertices])
        self.colors = glm.array([v.color for v in vertices])
        self.faces = glm.array([glm.ivec3(f) for f in faces])
        for i, j, k in self.faces:
            self.normals.append(
                glm.normalize(
                    glm.cross(vertices[j].position-vertices[i].position, 
                              vertices[k].position-vertices[j].position
                    )
                )
            )
        self.normals = glm.array(self.normals)
        self.center = sum(self.vertices)/len(self.vertices)
    
        
    def __str__(self):
        mesh_str = "=================================== MESH OBJECT ====================================\n"
        mesh_str+= "------------------------------------- Vertices -------------------------------------\n"
        for i, (v, c) in enumerate(zip(self.vertices, self.colors)):
            mesh_str+= "Indice {}:\n".format(i)
            mesh_str+= "Position...: {}\n".format(v)
            mesh_str+= "Color......: {}\n\n".format(c)
        mesh_str+= "\n------------------------------------- Faces --------------------------------------\n"
        for f, n in zip(self.faces, self.normals):
            mesh_str+= "Face.......: {}\n".format(f)
            mesh_str+= "Normal.....:  {}\n\n".format(n)
        return mesh_str
    
        
    def draw(self, MVPMatrix, NormalMatrix,
             vertex_shader   = MINIMAL_VERTEX_SHADER, 
             fragment_shader = MINIMAL_FRAGMENT_SHADER):
        # Gerando os buffers e obtendo os identificadores
        VertexBuffer = gl.glGenBuffers(1)
        ElementBuffer = gl.glGenBuffers(1)

        # Ativando os buffers como corrente para receber os pontos
        # e copiando os dados para a memória de vídeo
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VertexBuffer)
        buffer_size = self.vertices.nbytes + self.normals.nbytes + self.colors.nbytes
        gl.glBufferData(gl.GL_ARRAY_BUFFER, buffer_size, None, gl.GL_STATIC_DRAW)
        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, 0, self.vertices.nbytes, self.vertices.ptr)
        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, self.vertices.nbytes, self.colors.nbytes, self.colors.ptr)
        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, self.vertices.nbytes + self.colors.nbytes, self.normals.nbytes, self.normals.ptr)

        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, ElementBuffer)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, self.faces.nbytes, self.faces.ptr, gl.GL_STATIC_DRAW)

        gl.glEnableVertexAttribArray(0)
        gl.glEnableVertexAttribArray(1)
        gl.glEnableVertexAttribArray(2)
        
        vSize, nSize, iSize = self.vertices.nbytes, self.normals.nbytes, self.faces.nbytes

        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(0))
        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_TRUE, 0, ctypes.c_void_p(vSize))
        gl.glVertexAttribPointer(2, 3, gl.GL_FLOAT, gl.GL_TRUE, 0, ctypes.c_void_p(vSize + nSize))
        
        current_program = LoadShaders(vertex_shader, fragment_shader)
        gl.glUseProgram(current_program)
        
        ModelViewProjectionLoc = gl.glGetUniformLocation(current_program, "ModelViewProjection")
        gl.glUniformMatrix4fv(ModelViewProjectionLoc, 1, gl.GL_FALSE, glm.value_ptr(MVPMatrix))

        NormalMatrixLoc = gl.glGetUniformLocation(current_program, "NormalMatrix")
        gl.glUniformMatrix4fv(NormalMatrixLoc, 1, gl.GL_FALSE, glm.value_ptr(NormalMatrix))
        
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
        gl.glDrawElements(gl.GL_TRIANGLES, iSize*3, gl.GL_UNSIGNED_INT, ctypes.c_void_p(0))
        
        gl.glDisableVertexAttribArray(0)
        gl.glDisableVertexAttribArray(1)
        gl.glDisableVertexAttribArray(2)
        gl.glUseProgram(0)
    

class Triangle(Mesh):
    def __init__(self, vertices, faces):
        if len(vertices) != 3 or len(faces) != 1:
            raise ValueError("Triangle must have 3 vertices and 1 face!")
        else:
            super().__init__(vertices, faces)
    
    
class Quad(Mesh):
    def __init__(self, vertices, faces):
        if len(vertices) != 4 or len(faces) != 2:
            raise ValueError("Quad must have 4 vertices and 1 face!")
        else:
            super().__init__(vertices, faces)