# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GraphEditor_UI.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_widget_graphEditor(object):
    def setupUi(self, widget_graphEditor):
        widget_graphEditor.setObjectName("widget_graphEditor")
        widget_graphEditor.resize(1103, 354)
        widget_graphEditor.setWindowTitle("")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(widget_graphEditor)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_21 = QtWidgets.QVBoxLayout()
        self.verticalLayout_21.setObjectName("verticalLayout_21")
        self.lbl_graphHeader = QtWidgets.QLabel(widget_graphEditor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_graphHeader.sizePolicy().hasHeightForWidth())
        self.lbl_graphHeader.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lbl_graphHeader.setFont(font)
        self.lbl_graphHeader.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.lbl_graphHeader.setObjectName("lbl_graphHeader")
        self.verticalLayout_21.addWidget(self.lbl_graphHeader)
        self.groupBox_5 = QtWidgets.QGroupBox(widget_graphEditor)
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
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 518, 193))
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
        self.listwidget_graph_ModelsAdded = QtWidgets.QListWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listwidget_graph_ModelsAdded.sizePolicy().hasHeightForWidth())
        self.listwidget_graph_ModelsAdded.setSizePolicy(sizePolicy)
        self.listwidget_graph_ModelsAdded.setMinimumSize(QtCore.QSize(500, 90))
        self.listwidget_graph_ModelsAdded.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.listwidget_graph_ModelsAdded.setObjectName("listwidget_graph_ModelsAdded")
        self.horizontalLayout.addWidget(self.listwidget_graph_ModelsAdded)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 4, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lbl_graphName = QtWidgets.QLabel(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_graphName.sizePolicy().hasHeightForWidth())
        self.lbl_graphName.setSizePolicy(sizePolicy)
        self.lbl_graphName.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lbl_graphName.setObjectName("lbl_graphName")
        self.horizontalLayout_2.addWidget(self.lbl_graphName)
        self.lineedit_graphName = QtWidgets.QLineEdit(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineedit_graphName.sizePolicy().hasHeightForWidth())
        self.lineedit_graphName.setSizePolicy(sizePolicy)
        self.lineedit_graphName.setMinimumSize(QtCore.QSize(125, 25))
        self.lineedit_graphName.setObjectName("lineedit_graphName")
        self.horizontalLayout_2.addWidget(self.lineedit_graphName)
        self.button_SaveGraph = QtWidgets.QPushButton(self.groupBox_5)
        self.button_SaveGraph.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Images/save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_SaveGraph.setIcon(icon)
        self.button_SaveGraph.setObjectName("button_SaveGraph")
        self.horizontalLayout_2.addWidget(self.button_SaveGraph)
        self.button_EditGraph = QtWidgets.QPushButton(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_EditGraph.sizePolicy().hasHeightForWidth())
        self.button_EditGraph.setSizePolicy(sizePolicy)
        self.button_EditGraph.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.button_EditGraph.setStyleSheet("")
        self.button_EditGraph.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Images/edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_EditGraph.setIcon(icon1)
        self.button_EditGraph.setObjectName("button_EditGraph")
        self.horizontalLayout_2.addWidget(self.button_EditGraph)
        self.button_DeleteGraph = QtWidgets.QPushButton(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_DeleteGraph.sizePolicy().hasHeightForWidth())
        self.button_DeleteGraph.setSizePolicy(sizePolicy)
        self.button_DeleteGraph.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.button_DeleteGraph.setStyleSheet("")
        self.button_DeleteGraph.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("Images/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_DeleteGraph.setIcon(icon2)
        self.button_DeleteGraph.setObjectName("button_DeleteGraph")
        self.horizontalLayout_2.addWidget(self.button_DeleteGraph)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.verticalLayout_21.addWidget(self.groupBox_5)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_21.addItem(spacerItem1)
        self.horizontalLayout_5.addLayout(self.verticalLayout_21)
        self.verticalLayout_20 = QtWidgets.QVBoxLayout()
        self.verticalLayout_20.setObjectName("verticalLayout_20")
        self.lbl_graph_typeHeader = QtWidgets.QLabel(widget_graphEditor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_graph_typeHeader.sizePolicy().hasHeightForWidth())
        self.lbl_graph_typeHeader.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lbl_graph_typeHeader.setFont(font)
        self.lbl_graph_typeHeader.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.lbl_graph_typeHeader.setObjectName("lbl_graph_typeHeader")
        self.verticalLayout_20.addWidget(self.lbl_graph_typeHeader)
        self.groupBox_6 = QtWidgets.QGroupBox(widget_graphEditor)
        self.groupBox_6.setTitle("")
        self.groupBox_6.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBox_6.setObjectName("groupBox_6")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_6)
        self.gridLayout.setObjectName("gridLayout")
        self.combobox_graph_type = QtWidgets.QComboBox(self.groupBox_6)
        self.combobox_graph_type.setObjectName("combobox_graph_type")
        self.combobox_graph_type.addItem("")
        self.combobox_graph_type.addItem("")
        self.combobox_graph_type.addItem("")
        self.gridLayout.addWidget(self.combobox_graph_type, 1, 0, 1, 1)
        self.verticalLayout_20.addWidget(self.groupBox_6)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_20.addItem(spacerItem2)
        self.horizontalLayout_5.addLayout(self.verticalLayout_20)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_5)
        self.verticalLayout_24 = QtWidgets.QVBoxLayout()
        self.verticalLayout_24.setObjectName("verticalLayout_24")
        self.lbl_graph_originsHeader = QtWidgets.QLabel(widget_graphEditor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_graph_originsHeader.sizePolicy().hasHeightForWidth())
        self.lbl_graph_originsHeader.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lbl_graph_originsHeader.setFont(font)
        self.lbl_graph_originsHeader.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.lbl_graph_originsHeader.setObjectName("lbl_graph_originsHeader")
        self.verticalLayout_24.addWidget(self.lbl_graph_originsHeader)
        self.checkbox_graph_selectAll_Origins = QtWidgets.QCheckBox(widget_graphEditor)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.checkbox_graph_selectAll_Origins.setFont(font)
        self.checkbox_graph_selectAll_Origins.setObjectName("checkbox_graph_selectAll_Origins")
        self.verticalLayout_24.addWidget(self.checkbox_graph_selectAll_Origins)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_graph_originGroup = QtWidgets.QLabel(widget_graphEditor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_graph_originGroup.sizePolicy().hasHeightForWidth())
        self.label_graph_originGroup.setSizePolicy(sizePolicy)
        self.label_graph_originGroup.setObjectName("label_graph_originGroup")
        self.horizontalLayout_3.addWidget(self.label_graph_originGroup)
        self.combobox_graph_originGroup = QtWidgets.QComboBox(widget_graphEditor)
        self.combobox_graph_originGroup.setObjectName("combobox_graph_originGroup")
        self.horizontalLayout_3.addWidget(self.combobox_graph_originGroup)
        self.button_graph_CheckOrigins_byGroup = QtWidgets.QPushButton(widget_graphEditor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_graph_CheckOrigins_byGroup.sizePolicy().hasHeightForWidth())
        self.button_graph_CheckOrigins_byGroup.setSizePolicy(sizePolicy)
        self.button_graph_CheckOrigins_byGroup.setMaximumSize(QtCore.QSize(20, 16777215))
        self.button_graph_CheckOrigins_byGroup.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("Images/check.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_graph_CheckOrigins_byGroup.setIcon(icon3)
        self.button_graph_CheckOrigins_byGroup.setObjectName("button_graph_CheckOrigins_byGroup")
        self.horizontalLayout_3.addWidget(self.button_graph_CheckOrigins_byGroup)
        self.verticalLayout_24.addLayout(self.horizontalLayout_3)
        self.listwidget_graph_origins = QtWidgets.QListWidget(widget_graphEditor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(50)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listwidget_graph_origins.sizePolicy().hasHeightForWidth())
        self.listwidget_graph_origins.setSizePolicy(sizePolicy)
        self.listwidget_graph_origins.setMinimumSize(QtCore.QSize(100, 0))
        self.listwidget_graph_origins.setObjectName("listwidget_graph_origins")
        self.verticalLayout_24.addWidget(self.listwidget_graph_origins)
        self.horizontalLayout_6.addLayout(self.verticalLayout_24)
        self.verticalLayout_25 = QtWidgets.QVBoxLayout()
        self.verticalLayout_25.setObjectName("verticalLayout_25")
        self.lbl_graph_variablesHeader = QtWidgets.QLabel(widget_graphEditor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_graph_variablesHeader.sizePolicy().hasHeightForWidth())
        self.lbl_graph_variablesHeader.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lbl_graph_variablesHeader.setFont(font)
        self.lbl_graph_variablesHeader.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.lbl_graph_variablesHeader.setObjectName("lbl_graph_variablesHeader")
        self.verticalLayout_25.addWidget(self.lbl_graph_variablesHeader)
        self.checkbox_graph_selectAll_VariablesFormulas = QtWidgets.QCheckBox(widget_graphEditor)
        self.checkbox_graph_selectAll_VariablesFormulas.setObjectName("checkbox_graph_selectAll_VariablesFormulas")
        self.verticalLayout_25.addWidget(self.checkbox_graph_selectAll_VariablesFormulas)
        self.listwidget_graph_variables = QtWidgets.QListWidget(widget_graphEditor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listwidget_graph_variables.sizePolicy().hasHeightForWidth())
        self.listwidget_graph_variables.setSizePolicy(sizePolicy)
        self.listwidget_graph_variables.setMinimumSize(QtCore.QSize(0, 120))
        self.listwidget_graph_variables.setObjectName("listwidget_graph_variables")
        self.verticalLayout_25.addWidget(self.listwidget_graph_variables)
        self.listwidget_graph_formulas = QtWidgets.QListWidget(widget_graphEditor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listwidget_graph_formulas.sizePolicy().hasHeightForWidth())
        self.listwidget_graph_formulas.setSizePolicy(sizePolicy)
        self.listwidget_graph_formulas.setMinimumSize(QtCore.QSize(0, 90))
        self.listwidget_graph_formulas.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.listwidget_graph_formulas.setObjectName("listwidget_graph_formulas")
        self.verticalLayout_25.addWidget(self.listwidget_graph_formulas)
        self.horizontalLayout_6.addLayout(self.verticalLayout_25)
        self.verticalLayout_23 = QtWidgets.QVBoxLayout()
        self.verticalLayout_23.setObjectName("verticalLayout_23")
        self.groupbox_cathegory = QtWidgets.QGroupBox(widget_graphEditor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupbox_cathegory.sizePolicy().hasHeightForWidth())
        self.groupbox_cathegory.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupbox_cathegory.setFont(font)
        self.groupbox_cathegory.setObjectName("groupbox_cathegory")
        self.verticalLayout_27 = QtWidgets.QVBoxLayout(self.groupbox_cathegory)
        self.verticalLayout_27.setObjectName("verticalLayout_27")
        self.radiobutton_graph_cathegoryModel = QtWidgets.QRadioButton(self.groupbox_cathegory)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.radiobutton_graph_cathegoryModel.setFont(font)
        self.radiobutton_graph_cathegoryModel.setChecked(True)
        self.radiobutton_graph_cathegoryModel.setObjectName("radiobutton_graph_cathegoryModel")
        self.verticalLayout_27.addWidget(self.radiobutton_graph_cathegoryModel)
        self.radiobutton_graph_cathegoryOrigin = QtWidgets.QRadioButton(self.groupbox_cathegory)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.radiobutton_graph_cathegoryOrigin.setFont(font)
        self.radiobutton_graph_cathegoryOrigin.setObjectName("radiobutton_graph_cathegoryOrigin")
        self.verticalLayout_27.addWidget(self.radiobutton_graph_cathegoryOrigin)
        self.verticalLayout_23.addWidget(self.groupbox_cathegory)
        self.groupbox_column = QtWidgets.QGroupBox(widget_graphEditor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupbox_column.sizePolicy().hasHeightForWidth())
        self.groupbox_column.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupbox_column.setFont(font)
        self.groupbox_column.setObjectName("groupbox_column")
        self.verticalLayout_28 = QtWidgets.QVBoxLayout(self.groupbox_column)
        self.verticalLayout_28.setObjectName("verticalLayout_28")
        self.radiobutton_graph_columnModel = QtWidgets.QRadioButton(self.groupbox_column)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.radiobutton_graph_columnModel.setFont(font)
        self.radiobutton_graph_columnModel.setObjectName("radiobutton_graph_columnModel")
        self.verticalLayout_28.addWidget(self.radiobutton_graph_columnModel)
        self.radiobutton_graph_columnOrigin = QtWidgets.QRadioButton(self.groupbox_column)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.radiobutton_graph_columnOrigin.setFont(font)
        self.radiobutton_graph_columnOrigin.setChecked(True)
        self.radiobutton_graph_columnOrigin.setObjectName("radiobutton_graph_columnOrigin")
        self.verticalLayout_28.addWidget(self.radiobutton_graph_columnOrigin)
        self.verticalLayout_23.addWidget(self.groupbox_column)
        self.horizontalLayout_6.addLayout(self.verticalLayout_23)

        self.retranslateUi(widget_graphEditor)
        QtCore.QMetaObject.connectSlotsByName(widget_graphEditor)

    def retranslateUi(self, widget_graphEditor):
        _translate = QtCore.QCoreApplication.translate
        self.lbl_graphHeader.setText(_translate("widget_graphEditor", "GRÁFICO"))
        self.lbl_graphName.setText(_translate("widget_graphEditor", "GRÁFICO X"))
        self.button_SaveGraph.setToolTip(_translate("widget_graphEditor", "Salvar nome do gráfico"))
        self.button_EditGraph.setToolTip(_translate("widget_graphEditor", "Editar nome do gráfico"))
        self.button_DeleteGraph.setToolTip(_translate("widget_graphEditor", "Excluir gráfico"))
        self.lbl_graph_typeHeader.setText(_translate("widget_graphEditor", "TIPO"))
        self.combobox_graph_type.setItemText(0, _translate("widget_graphEditor", "WELLS"))
        self.combobox_graph_type.setItemText(1, _translate("widget_graphEditor", "GROUPS"))
        self.combobox_graph_type.setItemText(2, _translate("widget_graphEditor", "SECTORS"))
        self.lbl_graph_originsHeader.setText(_translate("widget_graphEditor", "ORIGENS"))
        self.checkbox_graph_selectAll_Origins.setText(_translate("widget_graphEditor", "TODOS"))
        self.label_graph_originGroup.setText(_translate("widget_graphEditor", "GRUPO"))
        self.lbl_graph_variablesHeader.setText(_translate("widget_graphEditor", "VARIÁVEIS"))
        self.checkbox_graph_selectAll_VariablesFormulas.setText(_translate("widget_graphEditor", "TODOS"))
        self.groupbox_cathegory.setTitle(_translate("widget_graphEditor", "CATEGORIA"))
        self.radiobutton_graph_cathegoryModel.setText(_translate("widget_graphEditor", "Modelo"))
        self.radiobutton_graph_cathegoryOrigin.setText(_translate("widget_graphEditor", "Origem"))
        self.groupbox_column.setTitle(_translate("widget_graphEditor", "COLUNA"))
        self.radiobutton_graph_columnModel.setText(_translate("widget_graphEditor", "Modelo"))
        self.radiobutton_graph_columnOrigin.setText(_translate("widget_graphEditor", "Origem"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget_graphEditor = QtWidgets.QWidget()
    ui = Ui_widget_graphEditor()
    ui.setupUi(widget_graphEditor)
    widget_graphEditor.show()
    sys.exit(app.exec_())
