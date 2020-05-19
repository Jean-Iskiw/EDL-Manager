# -*- coding: utf-8 -*-
import logging
from UniQt import QtWidgets, QtCore

class EdlTable(QtWidgets.QTableView):
    itemSelectionChanged = QtCore.Signal()

    def __init__(self, rows):
        super(EdlTable, self).__init__()
        self.model = QtWidgets.QStandardItemModel()
        self.setModel(self.model)

        self.model.setRowCount(rows)
        self.model.setColumnCount(6)
        self.model.setHorizontalHeaderLabels(["Clip",
                                        "Rush TC In",
                                        "Rush TC Out",
                                        "Master TC In",
                                        "Master TC Out"])

        self.setColumnHidden(5, True)
        self.setAlternatingRowColors(True)
        self.resizeColumnsToContents()
        self.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection
        )
        self.prev_selection = self.selectionModel().selectedRows()
        for r in range(self.model.rowCount()):
            self.model.setItem(r,5, QtWidgets.QStandardItem())
            # self.model.item(r,5).setText("")

    def mousePressEvent(self,event):
        super(EdlTable, self).mousePressEvent(event)
        if self.prev_selection != self.selectionModel().selectedRows():
            self.itemSelectionChanged.emit()


class MainWindow(QtWidgets.QMainWindow):
    saveEvent = QtCore.Signal()
    openedFile = QtCore.Signal(str)
    openedEdl = QtCore.Signal(str)

    def __init__(self, application, parent=None):

        QtWidgets.QMainWindow.__init__(self, parent)
        self.application = application
        self.elems_list=[]

        # Menus & Actions ---
        openAct =  QtWidgets.QAction("&Open...", self)
        openAct.setShortcuts(QtWidgets.QKeySequence.Open)
        openAct.setStatusTip("Open an existing file")
        openAct.triggered.connect(self.open_file)

        menubar = self.menuBar()
        self.fileMenu = menubar.addMenu('&File')
        self.fileMenu.addAction(openAct)
        # UI Elements ---
        self.table_edl = EdlTable(10)
        self.add_clip_field = QtWidgets.QTextEdit("")
        self.button_add = QtWidgets.QPushButton("Add")
        self.button_del = QtWidgets.QPushButton("Del")
        self.button_import = QtWidgets.QPushButton("Import EDL / AFF")
        self.comment = QtWidgets.QTextEdit("")

        self.layout_main = QtWidgets.QGridLayout()

        # UI Layout ---
        self.layout_main.addWidget(self.table_edl, 1, 0, 1, 4)
        self.layout_main.addWidget(self.add_clip_field, 2, 0, 1, 2)
        self.layout_main.addWidget(self.button_add, 2, 2, 1, 1)
        self.layout_main.addWidget(self.button_del, 2, 3, 1, 1)
        self.layout_main.addWidget(self.button_import, 2, 4, 1, 1)
        self.layout_main.addWidget(self.comment, 1, 4, 1, 1)

        self.add_clip_field.setFixedHeight(30)
        self.table_edl.setMinimumWidth(500)

        # Events and connections ---
        self.button_add.clicked.connect(self.add_item)
        self.button_del.clicked.connect(self.del_item)
        self.button_import.clicked.connect(self.open_edl)
        self.table_edl.itemSelectionChanged.connect(self.update_comment)
        self.comment.textChanged.connect(self.comment_changed)

        self.installEventFilter(self)

        self.centralWidget = QtWidgets.QWidget()
        self.centralWidget.setLayout(self.layout_main)
        self.setCentralWidget(self.centralWidget)

    def eventFilter(self,obj,event):
        if obj is self and event.type() == QtCore.QEvent.Close:
            self.saveEvent.emit()
            return True
        return super(
            type(self.application),
            self.application
        ).eventFilter(obj,event)

    def openAct(self):
        print("open file")

    def comment_changed(self):
        '''
        Notes are stored in hidden column (5) so each time we edit the text
        in elem_desc we update the column.
        '''
        for i in self.table_edl.selectionModel().selectedRows():
            selectedItem = self.table_edl.model.item(i.row(),5)
            break
        if not 'selectedItem' in locals():
            return
        if self.comment.toPlainText() != selectedItem.text():
            selectedItem.setText(self.comment.toPlainText())


    def update_comment(self):
        sel = self.table_edl.selectionModel().selectedRows()
        if len(sel) > 0:
            row = sel[0].row()
            self.comment.setText(
                self.table_edl.model.item(row,5).text()
            )
            return

    def add_item(self):
        pass

    def del_item(self):
        pass

    def open_file(self):
        browser = QtWidgets.QFileDialog()
        opened_file = browser.getOpenFileName(caption = "Open JSON File",
                                              filter = "JSON Files (*.json)")
        self.openedFile.emit(opened_file)

    def open_edl(self):
        browser = QtWidgets.QFileDialog()
        edl = browser.getOpenFileName(caption = "Open EDL / AFF File",
                                      filter = "EDL / AFF Files (*.edl *.aff)")
        self.openedEdl.emit(edl)
        # Use self.open_edl in main app to read EDL using python split.
        # Then set table according to data

    def export_table(self):
        return self.table_edl
