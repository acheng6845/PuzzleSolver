__author__ = 'Aaron'

# import necessary files
from PyQt5 import PyQt5
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QHBoxLayout,
                             QFrame, QSplitter, QStyleFactory,
                             QMainWindow, QStackedWidget)
from PyQt5.QtCore import Qt

from PADScreen import PADScreen

class GUIMainWindow(QMainWindow):

  def __init__(self):
    super().__init__()
    widget = PADScreen(self)
    self.setCentralWidget(widget)
    self.setGeometry(300, 300, 300, 200)
    self.setWindowTitle('PAD Damage Calculator')
    self.show()


class PADGUI(QStackedWidget):

  def __init__(self, main_window):
    super().__init__()

    self.init_UI(main_window)

  def init_UI(self, main_window):
    #The initial screen that we'll be working on
    screen = PADScreen(self, main_window)
    screen_widget = QWidget(main_window)

    #Make the main screen our layout
    screen_widget.setLayout(screen)

    self.addWidget(screen_widget)

    #Add simulation screen here:

    #Set the window dimensions, title and show it off!
    self.setGeometry(300, 300, 300, 200)
    self.setWindowTitle('PAD Damage Calculator')
    self.show()

if __name__ == '__main__':

  app = QApplication(sys.argv)

  gui = GUIMainWindow()

  sys.exit(app.exec_())