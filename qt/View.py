from PySide import QtCore, QtGui
from nexusgetUI import Ui_MainWindow
import nexusget
import os
import os.path

class MyMainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.password.setEchoMode(QtGui.QLineEdit.Password)
        self.ui.animal.addItems(nexusget.animals.keys())
        
    @QtCore.Slot()
    def on_pushButton_clicked(self):
        
        directory = QtGui.QFileDialog.getExistingDirectory(caption='Store data',
                        options=QtGui.QFileDialog.ShowDirsOnly)
        if len(directory):
            #get data
            os.chdir(directory)
            animal = self.ui.animal.currentText()
            username = self.ui.username.text()
            password = self.ui.password.text()
            getEvents = self.ui.checkBox.isChecked()
            filenumbers = self.ui.filenumbers.text()
            
            nxget = nexusget.NXGet(username, password, animal=animal)
            nxget.get_files(filenumbers, get_event_files=getEvents)
            nxget.t.close()
