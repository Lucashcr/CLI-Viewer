import logging
import OpenGL.GL as gl

MINIMAL_VERTEX_SHADER = "./ui/shaders/minimal_vertex_shader.glsl"

MINIMAL_FRAGMENT_SHADER = "./ui/shaders/minimal_fragment_shader.glsl"

def LoadShaders(vertex_shader_file, fragment_shader_file):
    logger = logging.getLogger(__name__)

    vertex_code = open(vertex_shader_file).readlines()
    assert vertex_code
    fragment_code = open(fragment_shader_file).readlines()
    assert fragment_code

    program = gl.glCreateProgram()
    vertex = gl.glCreateShader(gl.GL_VERTEX_SHADER)
    fragment = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)

    # Set shaders source
    gl.glShaderSource(vertex, vertex_code)
    gl.glShaderSource(fragment, fragment_code)

    # Compile shaders
    gl.glCompileShader(vertex)
    if not gl.glGetShaderiv(vertex, gl.GL_COMPILE_STATUS):
        error = gl.glGetShaderInfoLog(vertex).decode()
        logger.error("Vertex shader compilation error: %s", error)

    gl.glCompileShader(fragment)
    if not gl.glGetShaderiv(fragment, gl.GL_COMPILE_STATUS):
        error = gl.glGetShaderInfoLog(fragment).decode()
        print(error)
        raise RuntimeError("Fragment shader compilation error")

    gl.glAttachShader(program, vertex)
    gl.glAttachShader(program, fragment)
    gl.glLinkProgram(program)

    if not gl.glGetProgramiv(program, gl.GL_LINK_STATUS):
        print(gl.glGetProgramInfoLog(program))
        raise RuntimeError('Linking error')

    gl.glDetachShader(program, vertex)
    gl.glDetachShader(program, fragment)

    gl.glDeleteShader(vertex)
    gl.glDeleteShader(fragment)

    return program

# import ctypes
# import sys
# import glm

# def Load_to_buffer(obj, current_program, camera):
#     VBO, EBO, vSize, nSize, iSize = Load_object(obj)
    
#     gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBO)
#     gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, EBO)

#     gl.glEnableVertexAttribArray(0)
#     gl.glEnableVertexAttribArray(1)
#     gl.glEnableVertexAttribArray(2)

#     gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(0))
#     gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_TRUE, 0, ctypes.c_void_p(vSize))
#     gl.glVertexAttribPointer(2, 3, gl.GL_FLOAT, gl.GL_TRUE, 0, ctypes.c_void_p(vSize + nSize))
    
#     MVP = camera.GetMVP()
#     ModelViewProjectionLoc = gl.glGetUniformLocation(current_program, "ModelViewProjection")
#     gl.glUniformMatrix4fv(ModelViewProjectionLoc, 1, gl.GL_FALSE, glm.value_ptr(MVP))

#     NormalMatrix = camera.GetNormalMatrix()
#     NormalMatrixLoc = gl.glGetUniformLocation(current_program, "NormalMatrix")
#     gl.glUniformMatrix4fv(NormalMatrixLoc, 1, gl.GL_FALSE, glm.value_ptr(NormalMatrix))
    
#     gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
#     gl.glDrawElements(gl.GL_TRIANGLES, iSize*3, gl.GL_UNSIGNED_INT, ctypes.c_void_p(0))
    
#     gl.glDisableVertexAttribArray(0)
#     gl.glDisableVertexAttribArray(1)
#     gl.glDisableVertexAttribArray(2)
    
    
# def Load_object(obj):
#     # Construindo dados
#     vertices = glm.array([vert.position for vert in obj.vertices])
#     indices = glm.array([glm.ivec3(face) for face in obj.faces])
#     colors = glm.array([vert.color for vert in obj.vertices])
#     normals = glm.array([vert.normal for vert in obj.vertices])

#     # Gerando os buffers e obtendo os identificadores
#     VertexBuffer = gl.glGenBuffers(1)
#     ElementBuffer = gl.glGenBuffers(1)

#     # Ativando os buffers como corrente para receber os pontos
#     # e copiando os dados para a memória de vídeo
#     gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VertexBuffer)
#     buffer_size = vertices.nbytes + normals.nbytes + colors.nbytes
#     gl.glBufferData(gl.GL_ARRAY_BUFFER, buffer_size, None, gl.GL_STATIC_DRAW)
#     gl.glBufferSubData(gl.GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices.ptr)
#     gl.glBufferSubData(gl.GL_ARRAY_BUFFER, vertices.nbytes, colors.nbytes, colors.ptr)
#     gl.glBufferSubData(gl.GL_ARRAY_BUFFER, vertices.nbytes + colors.nbytes, normals.nbytes, normals.ptr)
#     gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

#     gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, ElementBuffer)
#     gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices.ptr, gl.GL_STATIC_DRAW)
#     gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, 0)

#     return VertexBuffer, ElementBuffer, vertices.nbytes, normals.nbytes, len(indices)
