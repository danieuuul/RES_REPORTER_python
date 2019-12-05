# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FormulasView_UI.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_widget_formulas(object):
    def setupUi(self, widget_formulas):
        widget_formulas.setObjectName("widget_formulas")
        widget_formulas.resize(474, 67)
        widget_formulas.setWindowTitle("")
        self.gridLayout = QtWidgets.QGridLayout(widget_formulas)
        self.gridLayout.setObjectName("gridLayout")
        self.lbl_formulaExpression = QtWidgets.QLabel(widget_formulas)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.lbl_formulaExpression.setFont(font)
        self.lbl_formulaExpression.setText("")
        self.lbl_formulaExpression.setObjectName("lbl_formulaExpression")
        self.gridLayout.addWidget(self.lbl_formulaExpression, 0, 1, 1, 1)
        self.lbl_formulaType = QtWidgets.QLabel(widget_formulas)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_formulaType.sizePolicy().hasHeightForWidth())
        self.lbl_formulaType.setSizePolicy(sizePolicy)
        self.lbl_formulaType.setMinimumSize(QtCore.QSize(75, 0))
        self.lbl_formulaType.setSizeIncrement(QtCore.QSize(75, 0))
        self.lbl_formulaType.setText("")
        self.lbl_formulaType.setObjectName("lbl_formulaType")
        self.gridLayout.addWidget(self.lbl_formulaType, 0, 2, 1, 1)
        self.button_DeleteFormula = QtWidgets.QPushButton(widget_formulas)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_DeleteFormula.sizePolicy().hasHeightForWidth())
        self.button_DeleteFormula.setSizePolicy(sizePolicy)
        self.button_DeleteFormula.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Images/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_DeleteFormula.setIcon(icon)
        self.button_DeleteFormula.setObjectName("button_DeleteFormula")
        self.gridLayout.addWidget(self.button_DeleteFormula, 0, 3, 1, 1)
        self.lbl_formulaName = QtWidgets.QLabel(widget_formulas)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_formulaName.sizePolicy().hasHeightForWidth())
        self.lbl_formulaName.setSizePolicy(sizePolicy)
        self.lbl_formulaName.setMinimumSize(QtCore.QSize(150, 0))
        self.lbl_formulaName.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.lbl_formulaName.setFont(font)
        self.lbl_formulaName.setText("")
        self.lbl_formulaName.setObjectName("lbl_formulaName")
        self.gridLayout.addWidget(self.lbl_formulaName, 0, 0, 1, 1)

        self.retranslateUi(widget_formulas)
        QtCore.QMetaObject.connectSlotsByName(widget_formulas)

    def retranslateUi(self, widget_formulas):
        pass


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget_formulas = QtWidgets.QWidget()
    ui = Ui_widget_formulas()
    ui.setupUi(widget_formulas)
    widget_formulas.show()
    sys.exit(app.exec_())

