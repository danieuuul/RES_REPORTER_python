# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TableEditor_UI.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_widget_setEditor(object):
    def setupUi(self, widget_setEditor):
        widget_setEditor.setObjectName("widget_setEditor")
        widget_setEditor.resize(1095, 325)
        widget_setEditor.setWindowTitle("")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(widget_setEditor)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_21 = QtWidgets.QVBoxLayout()
        self.verticalLayout_21.setObjectName("verticalLayout_21")
        self.lbl_setHeader = QtWidgets.QLabel(widget_setEditor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_setHeader.sizePolicy().hasHeightForWidth())
        self.lbl_setHeader.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lbl_setHeader.setFont(font)
        self.lbl_setHeader.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.lbl_setHeader.setObjectName("lbl_setHeader")
        self.verticalLayout_21.addWidget(self.lbl_setHeader)
        self.groupBox_5 = QtWidgets.QGroupBox(widget_setEditor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy)
        self.groupBox_5.setTitle("")
        self.groupBox_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_5)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QtCore.QSize(515, 100))
        self.scrollArea.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 518, 179))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listwidget_set_ModelsAdded = QtWidgets.QListWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listwidget_set_ModelsAdded.sizePolicy().hasHeightForWidth())
        self.listwidget_set_ModelsAdded.setSizePolicy(sizePolicy)
        self.listwidget_set_ModelsAdded.setMinimumSize(QtCore.QSize(500, 90))
        self.listwidget_set_ModelsAdded.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.listwidget_set_ModelsAdded.setObjectName("listwidget_set_ModelsAdded")
        self.horizontalLayout.addWidget(self.listwidget_set_ModelsAdded)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 4, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lbl_setName = QtWidgets.QLabel(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_setName.sizePolicy().hasHeightForWidth())
        self.lbl_setName.setSizePolicy(sizePolicy)
        self.lbl_setName.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lbl_setName.setObjectName("lbl_setName")
        self.horizontalLayout_2.addWidget(self.lbl_setName)
        self.lineedit_setName = QtWidgets.QLineEdit(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineedit_setName.sizePolicy().hasHeightForWidth())
        self.lineedit_setName.setSizePolicy(sizePolicy)
        self.lineedit_setName.setMinimumSize(QtCore.QSize(125, 25))
        self.lineedit_setName.setObjectName("lineedit_setName")
        self.horizontalLayout_2.addWidget(self.lineedit_setName)
        self.button_SaveSet = QtWidgets.QPushButton(self.groupBox_5)
        self.button_SaveSet.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Images/save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_SaveSet.setIcon(icon)
        self.button_SaveSet.setObjectName("button_SaveSet")
        self.horizontalLayout_2.addWidget(self.button_SaveSet)
        self.button_EditSet = QtWidgets.QPushButton(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_EditSet.sizePolicy().hasHeightForWidth())
        self.button_EditSet.setSizePolicy(sizePolicy)
        self.button_EditSet.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.button_EditSet.setStyleSheet("")
        self.button_EditSet.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Images/edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_EditSet.setIcon(icon1)
        self.button_EditSet.setObjectName("button_EditSet")
        self.horizontalLayout_2.addWidget(self.button_EditSet)
        self.button_DeleteSet = QtWidgets.QPushButton(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_DeleteSet.sizePolicy().hasHeightForWidth())
        self.button_DeleteSet.setSizePolicy(sizePolicy)
        self.button_DeleteSet.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.button_DeleteSet.setStyleSheet("")
        self.button_DeleteSet.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("Images/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_DeleteSet.setIcon(icon2)
        self.button_DeleteSet.setObjectName("button_DeleteSet")
        self.horizontalLayout_2.addWidget(self.button_DeleteSet)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.verticalLayout_21.addWidget(self.groupBox_5)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_21.addItem(spacerItem1)
        self.horizontalLayout_5.addLayout(self.verticalLayout_21)
        self.verticalLayout_20 = QtWidgets.QVBoxLayout()
        self.verticalLayout_20.setObjectName("verticalLayout_20")
        self.lbl_set_typeHeader = QtWidgets.QLabel(widget_setEditor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_set_typeHeader.sizePolicy().hasHeightForWidth())
        self.lbl_set_typeHeader.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lbl_set_typeHeader.setFont(font)
        self.lbl_set_typeHeader.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.lbl_set_typeHeader.setObjectName("lbl_set_typeHeader")
        self.verticalLayout_20.addWidget(self.lbl_set_typeHeader)
        self.groupBox_6 = QtWidgets.QGroupBox(widget_setEditor)
        self.groupBox_6.setTitle("")
        self.groupBox_6.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBox_6.setObjectName("groupBox_6")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_6)
        self.gridLayout.setObjectName("gridLayout")
        self.combobox_set_type = QtWidgets.QComboBox(self.groupBox_6)
        self.combobox_set_type.setObjectName("combobox_set_type")
        self.combobox_set_type.addItem("")
        self.combobox_set_type.addItem("")
        self.combobox_set_type.addItem("")
        self.gridLayout.addWidget(self.combobox_set_type, 1, 0, 1, 1)
        self.verticalLayout_20.addWidget(self.groupBox_6)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_20.addItem(spacerItem2)
        self.horizontalLayout_5.addLayout(self.verticalLayout_20)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_5)
        self.verticalLayout_24 = QtWidgets.QVBoxLayout()
        self.verticalLayout_24.setObjectName("verticalLayout_24")
        self.lbl_set_originsHeader = QtWidgets.QLabel(widget_setEditor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_set_originsHeader.sizePolicy().hasHeightForWidth())
        self.lbl_set_originsHeader.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lbl_set_originsHeader.setFont(font)
        self.lbl_set_originsHeader.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.lbl_set_originsHeader.setObjectName("lbl_set_originsHeader")
        self.verticalLayout_24.addWidget(self.lbl_set_originsHeader)
        self.checkbox_set_selectAll_Origins = QtWidgets.QCheckBox(widget_setEditor)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.checkbox_set_selectAll_Origins.setFont(font)
        self.checkbox_set_selectAll_Origins.setObjectName("checkbox_set_selectAll_Origins")
        self.verticalLayout_24.addWidget(self.checkbox_set_selectAll_Origins)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_set_originGroup = QtWidgets.QLabel(widget_setEditor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_set_originGroup.sizePolicy().hasHeightForWidth())
        self.label_set_originGroup.setSizePolicy(sizePolicy)
        self.label_set_originGroup.setObjectName("label_set_originGroup")
        self.horizontalLayout_3.addWidget(self.label_set_originGroup)
        self.combobox_set_originGroup = QtWidgets.QComboBox(widget_setEditor)
        self.combobox_set_originGroup.setObjectName("combobox_set_originGroup")
        self.horizontalLayout_3.addWidget(self.combobox_set_originGroup)
        self.button_set_CheckOrigins_byGroup = QtWidgets.QPushButton(widget_setEditor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_set_CheckOrigins_byGroup.sizePolicy().hasHeightForWidth())
        self.button_set_CheckOrigins_byGroup.setSizePolicy(sizePolicy)
        self.button_set_CheckOrigins_byGroup.setMaximumSize(QtCore.QSize(20, 16777215))
        self.button_set_CheckOrigins_byGroup.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("Images/check.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_set_CheckOrigins_byGroup.setIcon(icon3)
        self.button_set_CheckOrigins_byGroup.setObjectName("button_set_CheckOrigins_byGroup")
        self.horizontalLayout_3.addWidget(self.button_set_CheckOrigins_byGroup)
        self.verticalLayout_24.addLayout(self.horizontalLayout_3)
        self.listwidget_set_origins = QtWidgets.QListWidget(widget_setEditor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(50)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listwidget_set_origins.sizePolicy().hasHeightForWidth())
        self.listwidget_set_origins.setSizePolicy(sizePolicy)
        self.listwidget_set_origins.setMinimumSize(QtCore.QSize(100, 0))
        self.listwidget_set_origins.setObjectName("listwidget_set_origins")
        self.verticalLayout_24.addWidget(self.listwidget_set_origins)
        self.horizontalLayout_6.addLayout(self.verticalLayout_24)
        self.verticalLayout_25 = QtWidgets.QVBoxLayout()
        self.verticalLayout_25.setObjectName("verticalLayout_25")
        self.lbl_set_variablesHeader = QtWidgets.QLabel(widget_setEditor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_set_variablesHeader.sizePolicy().hasHeightForWidth())
        self.lbl_set_variablesHeader.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lbl_set_variablesHeader.setFont(font)
        self.lbl_set_variablesHeader.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.lbl_set_variablesHeader.setObjectName("lbl_set_variablesHeader")
        self.verticalLayout_25.addWidget(self.lbl_set_variablesHeader)
        self.checkbox_set_selectAll_VariablesFormulas = QtWidgets.QCheckBox(widget_setEditor)
        self.checkbox_set_selectAll_VariablesFormulas.setObjectName("checkbox_set_selectAll_VariablesFormulas")
        self.verticalLayout_25.addWidget(self.checkbox_set_selectAll_VariablesFormulas)
        self.listwidget_set_variables = QtWidgets.QListWidget(widget_setEditor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listwidget_set_variables.sizePolicy().hasHeightForWidth())
        self.listwidget_set_variables.setSizePolicy(sizePolicy)
        self.listwidget_set_variables.setMinimumSize(QtCore.QSize(0, 120))
        self.listwidget_set_variables.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.listwidget_set_variables.setObjectName("listwidget_set_variables")
        self.verticalLayout_25.addWidget(self.listwidget_set_variables)
        self.listwidget_set_formulas = QtWidgets.QListWidget(widget_setEditor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listwidget_set_formulas.sizePolicy().hasHeightForWidth())
        self.listwidget_set_formulas.setSizePolicy(sizePolicy)
        self.listwidget_set_formulas.setMinimumSize(QtCore.QSize(0, 90))
        self.listwidget_set_formulas.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.listwidget_set_formulas.setSizeIncrement(QtCore.QSize(0, 100))
        self.listwidget_set_formulas.setObjectName("listwidget_set_formulas")
        self.verticalLayout_25.addWidget(self.listwidget_set_formulas)
        self.horizontalLayout_6.addLayout(self.verticalLayout_25)

        self.retranslateUi(widget_setEditor)
        QtCore.QMetaObject.connectSlotsByName(widget_setEditor)

    def retranslateUi(self, widget_setEditor):
        _translate = QtCore.QCoreApplication.translate
        self.lbl_setHeader.setText(_translate("widget_setEditor", "CONJUNTO DE DADOS"))
        self.lbl_setName.setText(_translate("widget_setEditor", "CONJUNTO X"))
        self.button_SaveSet.setToolTip(_translate("widget_setEditor", "Salvar nome do gráfico"))
        self.button_EditSet.setToolTip(_translate("widget_setEditor", "Editar nome do gráfico"))
        self.button_DeleteSet.setToolTip(_translate("widget_setEditor", "Excluir gráfico"))
        self.lbl_set_typeHeader.setText(_translate("widget_setEditor", "TIPO"))
        self.combobox_set_type.setItemText(0, _translate("widget_setEditor", "WELLS"))
        self.combobox_set_type.setItemText(1, _translate("widget_setEditor", "GROUPS"))
        self.combobox_set_type.setItemText(2, _translate("widget_setEditor", "SECTORS"))
        self.lbl_set_originsHeader.setText(_translate("widget_setEditor", "ORIGENS"))
        self.checkbox_set_selectAll_Origins.setText(_translate("widget_setEditor", "TODOS"))
        self.label_set_originGroup.setText(_translate("widget_setEditor", "GRUPO"))
        self.lbl_set_variablesHeader.setText(_translate("widget_setEditor", "VARIÁVEIS"))
        self.checkbox_set_selectAll_VariablesFormulas.setText(_translate("widget_setEditor", "TODOS"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget_setEditor = QtWidgets.QWidget()
    ui = Ui_widget_setEditor()
    ui.setupUi(widget_setEditor)
    widget_setEditor.show()
    sys.exit(app.exec_())

