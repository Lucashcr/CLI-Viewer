import sys
from PyQt5.QtWidgets import QApplication
from ui.app_controller import AppController
                
                    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = AppController()
    controller.show()
    app.exec_()
