__author__ = 'Aaron'
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5 import QtWidgets, QtCore, QtGui

class PADCompleter(QCompleter):
    def __init__(self):
        super().__init__()
        self.prefix = ''
        self.model = None

    def _set_model_(self, model):
        self.model = model
        super().setModel(self.model)

    def _update_model_(self):
        prefix = self.prefix

        class InnerProxyModel(QSortFilterProxyModel):
            def filterAcceptsRow(self, row, parent):
                index = self.sourceModel().index(row, 0, parent)
                search_string = prefix.lower()
                model_string = self.sourceModel().data(index, Qt.DisplayRole).lower()
                #print(search_string, 'in', model_string, search_string in model_string)
                return search_string in model_string

        proxy_model = InnerProxyModel()
        proxy_model.setSourceModel(self.model)
        self.setModel(proxy_model)
        #print('match :', proxy_model.rowCount())

    def splitPath(self, path):
        self.prefix = str(path)
        self._update_model_()
        return self.sourceModel().data()