from PySide2 import QtWidgets, QtCore
from view import MainWindow
from qmodel import QModel
from table_model import TableModel

class EDLManagerApp(QtCore.QObject):
    def __init__(self, args, parent = None, rows = 10):
        super(EDLManagerApp, self).__init__(parent)

        self.pyside_app = QtWidgets.QApplication(['EDL Manager'])
        self.table_model = TableModel(rows)
        self.qmodel = QModel(self)

        self.main_window = MainWindow(application = self,
                                      model = self.qmodel)

        self.main_window.saveEvent.connect(self.save_edl)
        self.main_window.openedFile.connect(self.read_edl)

    def model_info(self):
        return self.table_model.info()

    def run(self):
        self.main_window.show()
        return(self.pyside_app.exec_())

    def read_edl(self, edl):
        pass
        #parse raw EDL into function to split it into rows / columns

    def save_edl(self):
        table_to_save = self.main_window.export_table()
        # Save commented EDL ---

    def setRowCount(self, count):
        return self.table_model.setRowCount(count)

    def cell(self, row, column):
        return self.table_model.data[row][column]

    def update_cell(self, row, col, val):
        self.table_model.update_cell(row, col, val)
