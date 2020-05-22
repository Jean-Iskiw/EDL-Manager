# -*- coding: utf-8 -*-
import logging
from Pyside2 import QtWidgets, QtCore


class EdlTable(QtWidgets.QTableView):
    itemSelectionChanged = QtCore.Signal()

    def __init__(self, rows, model):
        super(EdlTable, self).__init__()
        self.model = model
        self.setModel(self.model)

        self.model.setRowCount(rows)

        self.setColumnHidden(5, True)
        self.setAlternatingRowColors(True)
        self.resizeColumnsToContents()
        self.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection
        )
        self.prev_selection = self.selectionModel().selectedRows()

        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.resize(1280, 720)

    def mousePressEvent(self,event):
        super(EdlTable, self).mousePressEvent(event)
        if self.prev_selection != self.selectionModel().selectedRows():
            self.prev_selection = self.selectionModel().selectedRows()
            self.itemSelectionChanged.emit()


class MainWindow(QtWidgets.QMainWindow):
    saveEvent = QtCore.Signal()
    openedFile = QtCore.Signal(str)
    openedEdl = QtCore.Signal(str)

    def __init__(self, application, model, parent = None):

        QtWidgets.QMainWindow.__init__(self, parent)
        self.application = application

        # Menus & Actions ---
        open_act =  QtWidgets.QAction("&Open...", self)
        open_act.setShortcuts(QtWidgets.QKeySequence.Open)
        open_act.setStatusTip("Open an existing file")
        open_act.triggered.connect(self.open_file)

        menubar = self.menuBar()
        self.fileMenu = menubar.addMenu('&File')
        self.fileMenu.addAction(open_act)

        # UI Elements ---
        self.table_edl = EdlTable(10, model)
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

    def open_act(self):
        print("open file")

    def comment_changed(self):
        '''
        Notes are stored in hidden column (5) so each time we edit the text
        in elem_desc we update the column.
        '''
        for index in self.table_edl.selectionModel().selectedRows():
            selectedItem = self.table_edl.model.data(CellIndex(index.row(),
                                                               5),
                                                     QtCore.Qt.UserRole)
            break
        if not 'selectedItem' in locals():
            return

        # print "\nComment_changed :\nCell : {} Comment : {}".format( \
        #     selectedItem, self.comment.toPlainText())
        if self.comment.toPlainText() != selectedItem:
            self.table_edl.model.setData(CellIndex(index.row(), 5),
                                         self.comment.toPlainText(),
                                         2)


    def update_comment(self):
        sel = self.table_edl.selectionModel().selectedRows()
        if len(sel) > 0:
            # print "\nview - update comment\nselected row : {} value : {}".format( \
            #     sel[0],
            #     self.table_edl.model.data(CellIndex(sel[0].row(),
            #                                         5),
            #                               QtCore.Qt.UserRole))
            self.comment.blockSignals(True)
            self.comment.setText(
                self.table_edl.model.data(CellIndex(sel[0].row(),
                                                    5),
                                          QtCore.Qt.UserRole)
            )
            self.comment.blockSignals(False)
            return

    def add_item(self):
        item = self.add_clip_field.toPlainText().split(" ")
        row = compare_master_TC_in(item[3])
        for i in item:
            pass

    def compare_master_TC_in(self, timecode):
        # used to know on which row we should add item X
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


class CellIndex:
    def __init__(self,row,column):
        self._row = row
        self._column = column

    def row(self):
        return self._row
    def column(self):
        return self._column
