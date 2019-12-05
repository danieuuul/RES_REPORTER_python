# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GraphViewer_UI.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dialog_graphViewer(object):
    def setupUi(self, dialog_graphViewer):
        dialog_graphViewer.setObjectName("dialog_graphViewer")
        dialog_graphViewer.resize(780, 585)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(dialog_graphViewer)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.button_Previous = QtWidgets.QPushButton(dialog_graphViewer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_Previous.sizePolicy().hasHeightForWidth())
        self.button_Previous.setSizePolicy(sizePolicy)
        self.button_Previous.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Images/previous.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_Previous.setIcon(icon)
        self.button_Previous.setIconSize(QtCore.QSize(60, 60))
        self.button_Previous.setObjectName("button_Previous")
        self.gridLayout.addWidget(self.button_Previous, 1, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 3)
        self.button_Next = QtWidgets.QPushButton(dialog_graphViewer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_Next.sizePolicy().hasHeightForWidth())
        self.button_Next.setSizePolicy(sizePolicy)
        self.button_Next.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Images/next.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_Next.setIcon(icon1)
        self.button_Next.setIconSize(QtCore.QSize(60, 60))
        self.button_Next.setObjectName("button_Next")
        self.gridLayout.addWidget(self.button_Next, 1, 2, 1, 1)
        self.button_showIterativeGraph = QtWidgets.QPushButton(dialog_graphViewer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_showIterativeGraph.sizePolicy().hasHeightForWidth())
        self.button_showIterativeGraph.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.button_showIterativeGraph.setFont(font)
        self.button_showIterativeGraph.setIconSize(QtCore.QSize(45, 45))
        self.button_showIterativeGraph.setObjectName("button_showIterativeGraph")
        self.gridLayout.addWidget(self.button_showIterativeGraph, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)

        self.retranslateUi(dialog_graphViewer)
        QtCore.QMetaObject.connectSlotsByName(dialog_graphViewer)

    def retranslateUi(self, dialog_graphViewer):
        _translate = QtCore.QCoreApplication.translate
        dialog_graphViewer.setWindowTitle(_translate("dialog_graphViewer", "Dialog"))
        self.button_showIterativeGraph.setText(_translate("dialog_graphViewer", "GRÁFICO ITERATIVO"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog_graphViewer = QtWidgets.QDialog()
    ui = Ui_dialog_graphViewer()
    ui.setupUi(dialog_graphViewer)
    dialog_graphViewer.show()
    sys.exit(app.exec_())

