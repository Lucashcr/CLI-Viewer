import glm 

class Vertex:
    
    def __init__(self, position, color):
        self.position = glm.vec3(position)
        self.color = glm.vec3(color)
        
    def __str__(self):
        vertex_str  = "[\n  VERTEX OBJECT: \n"
        vertex_str += "    postion...: " + str(self.position) + "\n"
        vertex_str += "    color.....: " + str(self.color) + "\n"
        return vertex_str
        
if __name__ == '__main__':
    vertex = Vertex([1.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0])
    print(vertex)