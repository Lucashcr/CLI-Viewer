import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from .viewer_GUI import Ui_ViewerGUI


class AppController(QMainWindow, Ui_ViewerGUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        
    def keyPressEvent(self, KeyEvent):
        if KeyEvent.key() == Qt.Key.Key_Return:
            self.execute_command(self.commandLine.text().split(" "))
        elif KeyEvent.key() == Qt.Key.Key_Escape:
            self.commandLine.setText("")
        
    def execute_command(self, command):
        if command[0] == "exit":
            self.statusBar.showMessage("Bye! See you soon!")
            sys.exit()
        elif command[0] == "hello":
            self.statusBar.showMessage("Drawing hello triangle...")
            self.openGLWidget.add_element_to_scene("hello_triangle")
            self.statusBar.showMessage("Done!")
        else:
            self.statusBar.showMessage("Invalid command!")
