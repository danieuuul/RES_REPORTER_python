# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FormulasEditor_UI.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dialog_formulasEditor(object):
    def setupUi(self, dialog_formulasEditor):
        dialog_formulasEditor.setObjectName("dialog_formulasEditor")
        dialog_formulasEditor.resize(911, 725)
        self.gridLayout = QtWidgets.QGridLayout(dialog_formulasEditor)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea_2 = QtWidgets.QScrollArea(dialog_formulasEditor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea_2.sizePolicy().hasHeightForWidth())
        self.scrollArea_2.setSizePolicy(sizePolicy)
        self.scrollArea_2.setMinimumSize(QtCore.QSize(400, 320))
        self.scrollArea_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 685, 705))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_scrollFormulas = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_scrollFormulas.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_scrollFormulas.setObjectName("verticalLayout_scrollFormulas")
        self.verticalLayout_formulas = QtWidgets.QVBoxLayout()
        self.verticalLayout_formulas.setObjectName("verticalLayout_formulas")
        self.groupBox_newFormula = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_newFormula.sizePolicy().hasHeightForWidth())
        self.groupBox_newFormula.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_newFormula.setFont(font)
        self.groupBox_newFormula.setObjectName("groupBox_newFormula")
        self.gridLayout_newFormula = QtWidgets.QGridLayout(self.groupBox_newFormula)
        self.gridLayout_newFormula.setObjectName("gridLayout_newFormula")
        self.lineedit_formulaName = QtWidgets.QLineEdit(self.groupBox_newFormula)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.lineedit_formulaName.setFont(font)
        self.lineedit_formulaName.setObjectName("lineedit_formulaName")
        self.gridLayout_newFormula.addWidget(self.lineedit_formulaName, 1, 1, 1, 2)
        self.label = QtWidgets.QLabel(self.groupBox_newFormula)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_newFormula.addWidget(self.label, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox_newFormula)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_newFormula.addWidget(self.label_2, 2, 0, 1, 1)
        self.textedit_formulaExpression = TextEdit_DropFormulas(self.groupBox_newFormula)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textedit_formulaExpression.sizePolicy().hasHeightForWidth())
        self.textedit_formulaExpression.setSizePolicy(sizePolicy)
        self.textedit_formulaExpression.setMinimumSize(QtCore.QSize(0, 50))
        self.textedit_formulaExpression.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.textedit_formulaExpression.setFont(font)
        self.textedit_formulaExpression.setObjectName("textedit_formulaExpression")
        self.gridLayout_newFormula.addWidget(self.textedit_formulaExpression, 2, 1, 1, 2)
        self.button_NewFormula = QtWidgets.QPushButton(self.groupBox_newFormula)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_NewFormula.sizePolicy().hasHeightForWidth())
        self.button_NewFormula.setSizePolicy(sizePolicy)
        self.button_NewFormula.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Images/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_NewFormula.setIcon(icon)
        self.button_NewFormula.setIconSize(QtCore.QSize(20, 20))
        self.button_NewFormula.setObjectName("button_NewFormula")
        self.gridLayout_newFormula.addWidget(self.button_NewFormula, 4, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox_newFormula)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout_newFormula.addWidget(self.label_3, 4, 0, 1, 1)
        self.lbl_formula_type = QtWidgets.QLabel(self.groupBox_newFormula)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.lbl_formula_type.setFont(font)
        self.lbl_formula_type.setText("")
        self.lbl_formula_type.setObjectName("lbl_formula_type")
        self.gridLayout_newFormula.addWidget(self.lbl_formula_type, 4, 1, 1, 1)
        self.verticalLayout_formulas.addWidget(self.groupBox_newFormula)
        self.scrollArea = QtWidgets.QScrollArea(self.scrollAreaWidgetContents_2)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 663, 534))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_formulasAdded = QtWidgets.QGridLayout(self.groupBox)
        self.verticalLayout_formulasAdded.setObjectName("verticalLayout_formulasAdded")
        self.verticalLayout.addWidget(self.groupBox)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_formulas.addWidget(self.scrollArea)
        self.verticalLayout_scrollFormulas.addLayout(self.verticalLayout_formulas)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.gridLayout.addWidget(self.scrollArea_2, 1, 1, 5, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(dialog_formulasEditor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QtCore.QSize(200, 0))
        self.groupBox_2.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.combobox_formulas_type = QtWidgets.QComboBox(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combobox_formulas_type.sizePolicy().hasHeightForWidth())
        self.combobox_formulas_type.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.combobox_formulas_type.setFont(font)
        self.combobox_formulas_type.setObjectName("combobox_formulas_type")
        self.combobox_formulas_type.addItem("")
        self.combobox_formulas_type.addItem("")
        self.combobox_formulas_type.addItem("")
        self.verticalLayout_2.addWidget(self.combobox_formulas_type)
        self.listwidget_formulas_variables = QtWidgets.QListWidget(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listwidget_formulas_variables.sizePolicy().hasHeightForWidth())
        self.listwidget_formulas_variables.setSizePolicy(sizePolicy)
        self.listwidget_formulas_variables.setMinimumSize(QtCore.QSize(180, 300))
        self.listwidget_formulas_variables.setMaximumSize(QtCore.QSize(180, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.listwidget_formulas_variables.setFont(font)
        self.listwidget_formulas_variables.setObjectName("listwidget_formulas_variables")
        self.verticalLayout_2.addWidget(self.listwidget_formulas_variables)
        self.gridLayout.addWidget(self.groupBox_2, 1, 0, 4, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(dialog_formulasEditor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setMinimumSize(QtCore.QSize(200, 0))
        self.groupBox_3.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.listwidget_formulas_constants = QtWidgets.QListWidget(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listwidget_formulas_constants.sizePolicy().hasHeightForWidth())
        self.listwidget_formulas_constants.setSizePolicy(sizePolicy)
        self.listwidget_formulas_constants.setMinimumSize(QtCore.QSize(180, 0))
        self.listwidget_formulas_constants.setMaximumSize(QtCore.QSize(180, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.listwidget_formulas_constants.setFont(font)
        self.listwidget_formulas_constants.setObjectName("listwidget_formulas_constants")
        self.gridLayout_3.addWidget(self.listwidget_formulas_constants, 13, 0, 1, 2)
        self.label_4 = QtWidgets.QLabel(self.groupBox_3)
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 14, 0, 1, 1)
        self.button_SaveConstant = QtWidgets.QPushButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_SaveConstant.sizePolicy().hasHeightForWidth())
        self.button_SaveConstant.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.button_SaveConstant.setFont(font)
        self.button_SaveConstant.setObjectName("button_SaveConstant")
        self.gridLayout_3.addWidget(self.button_SaveConstant, 12, 0, 1, 2)
        self.label_5 = QtWidgets.QLabel(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QtCore.QSize(45, 0))
        self.label_5.setMaximumSize(QtCore.QSize(45, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 5, 0, 1, 1)
        self.combobox_constantType = QtWidgets.QComboBox(self.groupBox_3)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.combobox_constantType.setFont(font)
        self.combobox_constantType.setObjectName("combobox_constantType")
        self.combobox_constantType.addItem("")
        self.combobox_constantType.addItem("")
        self.gridLayout_3.addWidget(self.combobox_constantType, 2, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox_3)
        self.label_7.setMinimumSize(QtCore.QSize(45, 0))
        self.label_7.setMaximumSize(QtCore.QSize(45, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 2, 0, 1, 1)
        self.lineedit_constantName = QtWidgets.QLineEdit(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineedit_constantName.sizePolicy().hasHeightForWidth())
        self.lineedit_constantName.setSizePolicy(sizePolicy)
        self.lineedit_constantName.setMinimumSize(QtCore.QSize(100, 0))
        self.lineedit_constantName.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.lineedit_constantName.setFont(font)
        self.lineedit_constantName.setObjectName("lineedit_constantName")
        self.gridLayout_3.addWidget(self.lineedit_constantName, 5, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMinimumSize(QtCore.QSize(45, 0))
        self.label_6.setMaximumSize(QtCore.QSize(45, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 7, 0, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lineedit_constantValue = QtWidgets.QLineEdit(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineedit_constantValue.sizePolicy().hasHeightForWidth())
        self.lineedit_constantValue.setSizePolicy(sizePolicy)
        self.lineedit_constantValue.setMinimumSize(QtCore.QSize(100, 0))
        self.lineedit_constantValue.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.lineedit_constantValue.setFont(font)
        self.lineedit_constantValue.setObjectName("lineedit_constantValue")
        self.verticalLayout_3.addWidget(self.lineedit_constantValue)
        self.gridLayout_3.addLayout(self.verticalLayout_3, 7, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox_3, 5, 0, 1, 1)

        self.retranslateUi(dialog_formulasEditor)
        QtCore.QMetaObject.connectSlotsByName(dialog_formulasEditor)
        dialog_formulasEditor.setTabOrder(self.lineedit_formulaName, self.textedit_formulaExpression)
        dialog_formulasEditor.setTabOrder(self.textedit_formulaExpression, self.button_NewFormula)
        dialog_formulasEditor.setTabOrder(self.button_NewFormula, self.combobox_formulas_type)
        dialog_formulasEditor.setTabOrder(self.combobox_formulas_type, self.combobox_constantType)
        dialog_formulasEditor.setTabOrder(self.combobox_constantType, self.lineedit_constantName)
        dialog_formulasEditor.setTabOrder(self.lineedit_constantName, self.lineedit_constantValue)
        dialog_formulasEditor.setTabOrder(self.lineedit_constantValue, self.button_SaveConstant)
        dialog_formulasEditor.setTabOrder(self.button_SaveConstant, self.listwidget_formulas_constants)
        dialog_formulasEditor.setTabOrder(self.listwidget_formulas_constants, self.scrollArea)
        dialog_formulasEditor.setTabOrder(self.scrollArea, self.scrollArea_2)
        dialog_formulasEditor.setTabOrder(self.scrollArea_2, self.listwidget_formulas_variables)

    def retranslateUi(self, dialog_formulasEditor):
        _translate = QtCore.QCoreApplication.translate
        dialog_formulasEditor.setWindowTitle(_translate("dialog_formulasEditor", "Configuração de Fórmulas"))
        self.groupBox_newFormula.setTitle(_translate("dialog_formulasEditor", "Nova Fórmula"))
        self.label.setText(_translate("dialog_formulasEditor", "Nome"))
        self.label_2.setText(_translate("dialog_formulasEditor", "Fórmula"))
        self.label_3.setText(_translate("dialog_formulasEditor", "Tipo"))
        self.groupBox.setTitle(_translate("dialog_formulasEditor", "Fórmulas"))
        self.groupBox_2.setTitle(_translate("dialog_formulasEditor", "Variáveis"))
        self.combobox_formulas_type.setItemText(0, _translate("dialog_formulasEditor", "WELLS"))
        self.combobox_formulas_type.setItemText(1, _translate("dialog_formulasEditor", "GROUPS"))
        self.combobox_formulas_type.setItemText(2, _translate("dialog_formulasEditor", "SECTORS"))
        self.groupBox_3.setTitle(_translate("dialog_formulasEditor", "Constantes"))
        self.button_SaveConstant.setText(_translate("dialog_formulasEditor", "salvar"))
        self.label_5.setText(_translate("dialog_formulasEditor", "Nome"))
        self.combobox_constantType.setItemText(0, _translate("dialog_formulasEditor", "Número"))
        self.combobox_constantType.setItemText(1, _translate("dialog_formulasEditor", "Data"))
        self.label_7.setText(_translate("dialog_formulasEditor", "Tipo"))
        self.label_6.setText(_translate("dialog_formulasEditor", "Valor"))

from Interface.Extras.CustomWidgets import TextEdit_DropFormulas

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog_formulasEditor = QtWidgets.QDialog()
    ui = Ui_dialog_formulasEditor()
    ui.setupUi(dialog_formulasEditor)
    dialog_formulasEditor.show()
    sys.exit(app.exec_())

