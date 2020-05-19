# -*- coding: utf-8 -*-
import sys
import logging
from UniQt import QtWidgets, QtCore
from __ui__ import MainWindow

class EDLManagerApp(QtCore.QObject):
    def __init__(self, args, parent = None):
        QtCore.QObject.__init__(self,parent)
        self.pyside_app = QtWidgets.QApplication(['EDL Manager'])
        self.main_window = MainWindow(application = self)

        self.main_window.saveEvent.connect(self.save_edl)
        self.main_window.openedFile.connect(self.read_edl)

    def run(self):
        self.main_window.show()
        return(self.pyside_app.exec_())

    def read_edl(self, edl):
        pass
        #parse raw EDL into function to split it into rows / columns

    def save_edl(self):
        table_to_save = self.main_window.export_table()
        # Save commented EDL ---
if __name__ == '__main__':
    #logging.basicConfig(level=logging.INFO)

    application = EDLManagerApp(sys.argv)
    sys.exit(application.run())
