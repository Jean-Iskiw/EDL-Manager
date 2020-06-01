from PySide2 import QtCore

class QModel(QtCore.QAbstractTableModel):

    def __init__(self, application, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.application = application

    def rowCount(self, parent = None):
        return self.application.model_info().row_count

    def columnCount(self, parent = None):
        return self.application.model_info().col_count

    def data(self, index, role):
        cell = self.application.cell(index.row(), index.column())

        if role == QtCore.Qt.UserRole \
        or role == QtCore.Qt.DisplayRole:
            return cell

    def setData(self, index, value, role):
        # print  "\nQModel - Set Data :\nrow :{} col:{} value:{} role:{}".format( \
        #     index.row(),
        #     index.column(),
        #     value,
        #     role)
        self.application.update_cell(index.row(), index.column(), value)
        return False

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled \
               | QtCore.Qt.ItemIsEditable \
               | QtCore.Qt.ItemIsSelectable

    def setRowCount(self, count):
        return self.application.setRowCount(count)

    def headerData(self, section, orientation, role = QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return None

        list_headers = ["Clip",
                        "Rush TC In",
                        "Rush TC Out",
                        "Master TC In",
                        "Master TC Out"]
        if orientation == QtCore.Qt.Horizontal \
        and len(list_headers) > section:
            return list_headers[section]

        return None
