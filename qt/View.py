from PySide import QtCore, QtGui
from nexusgetUI import Ui_MainWindow
import nexusget
import os
import os.path
import sys

class MyMainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.password.setEchoMode(QtGui.QLineEdit.Password)
        self.ui.animal.addItems(nexusget.animals.keys())
        console = EmittingStream()
        sys.stdout = console
        console.textWritten.connect(self.writeTextToConsole)

    def writeTextToConsole(self, text):
        self.ui.history.moveCursor(QtGui.QTextCursor.End)
        self.ui.history.insertPlainText(text)

    @QtCore.Slot()
    def on_setdirectory_clicked(self):

        directory = QtGui.QFileDialog.getExistingDirectory(caption='Store data',
                        options=QtGui.QFileDialog.ShowDirsOnly)
        if len(directory):
            os.chdir(directory)
            self.ui.directory.setText(directory)

    @QtCore.Slot()
    def on_getfiles_clicked(self):

        directory = self.ui.directory.text()

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

class EmittingStream(QtCore.QObject):
    # a class for rewriting stdout to a console window
    textWritten = QtCore.Signal(str)

    def write(self, text):
        self.textWritten.emit(str(text))