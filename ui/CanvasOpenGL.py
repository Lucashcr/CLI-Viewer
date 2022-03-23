from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QOpenGLWidget

import glm
import OpenGL.GL as gl
from classes.camera import Camera

from classes.meshes import Triangle
from classes.vertex import Vertex


class CanvasOpenGL(QOpenGLWidget):
    
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent, flags)
        self.__scene__ = list()
        self.camera = Camera(self.width(), self.height())
        
    def add_element_to_scene(self, element):
        if element == "hello_triangle":
            t = Triangle([Vertex([ 1.0, -1.0, 0.0], [1.0, 0.0, 0.0]),
                          Vertex([ 0.0,  1.0, 0.0], [0.0, 1.0, 0.0]),
                          Vertex([-1.0, -1.0, 0.0], [0.0, 0.0, 1.0])], [(0, 1, 2)])
        self.__scene__.append(t)
        self.repaint()
        
    def remove_element_from_scene(self, element):
        self.__scene__.remove(element)
        
    def clear_scene(self):
        self.__scene__ = []
        
    def initializeGL(self):
        pass
    
    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        self.camera.Resize(self.width(), self.height())
        
        for element in self.__scene__:
            element.draw(self.camera.GetMVP(), self.camera.GetNormalMatrix())

    def mousePressEvent(self, MouseEvent):
        self.x = MouseEvent.x()
        self.y = MouseEvent.y()

    def mouseMoveEvent(self, MouseEvent):
        deltax = MouseEvent.x() - self.x; self.x += deltax
        deltay = MouseEvent.y() - self.y; self.y += deltay

        self.camera.MoveHAxis(deltax)
        self.camera.MoveVAxis(deltay)

        self.repaint()

    def wheelEvent(self, WheelEvent):
        zoomAmount = WheelEvent.angleDelta().y() 
        self.camera.Zoom(zoomAmount)
        self.repaint()