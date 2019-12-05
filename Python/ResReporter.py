#External Imports
import tempfile
import webbrowser
import sys
import time
import sip
import pandas as pd
import numpy as np
from datetime import datetime
import pickle
import seaborn as sns
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from _plotly_future_ import v4_subplots
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import plotly.offline as po

#import cufflinks
#cufflinks.go_offline(connected = True)

# PyQT5 Imports
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import  Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog



#Local Imports
from Util import General
import Model
from Business import Business
from Interface.Extras.QtWaitingSpinner import QtWaitingSpinner
from Interface.Extras.CustomWidgets import LineEdit_DateMask, TextEdit_DropFormulas, ListWidget_DropVariables


# Ui imports
from Interface.ResReporter_UI import Ui_QMain_ResReporter
from Interface.GraphEditor_UI import Ui_widget_graphEditor
from Interface.TableEditor_UI import Ui_widget_setEditor
from Interface.DatesEditor_UI import Ui_dialog_datesEditor
from Interface.FormulasEditor_UI import Ui_dialog_formulasEditor
from Interface.FormulasView_UI import Ui_widget_formulas
from Interface.UnitsEditor_UI import Ui_dialog_unitsEditor
from Interface.ColumnsEditor_UI import Ui_dialog_columnsEditor
from Interface.GraphViewer_UI import Ui_dialog_graphViewer


class ResReport_Thread(QtCore.QThread):
    signal = QtCore.pyqtSignal(str)

    def __init__(self, resReport, action):
        QtCore.QThread.__init__(self)
        self.resReport = resReport
        self.action = action
            
    def run(self):
        if self.action == "ReportGraphs":            
            self.signal.emit(self.resReport.ReportGraphs())
        if self.action == "PrepareTable":            
            self.signal.emit(self.resReport.PrepareTable())
        if self.action == "Export_toExcel":            
            self.signal.emit(self.resReport.Export_toExcel())
        if self.action == "ImportModels":            
            self.signal.emit(self.resReport.ImportModels())            

class ResReporter(QMainWindow, Ui_QMain_ResReporter):    
    send_fig = QtCore.pyqtSignal(str)
    
    def __init__(self):             
        self.service = Business()
        
        QMainWindow.__init__(self)
        self.setupUi(self)    
        
        # INICIALIZAÇÕES PRIMÁRIAS
        self.spinner = QtWaitingSpinner(self)
        
        
                           
        
        # INICIALIZANDO A TELA PRINCIPAL - CONFIGURAÇÕES DOS MODELOS   
        self.files = []        
        self.models = []
        self.modelsVariables = {}
        self.modelsVariables['GROUPS'] = []
        self.modelsVariables['WELLS'] = []
        self.modelsVariables['SECTORS'] = []
        
        self.modelsOrigins = {}
        self.modelsOrigins['GROUPS'] = []
        self.modelsOrigins['WELLS'] = []
        self.modelsOrigins['SECTORS'] = []
        
        self.thread_ImportModels = ResReport_Thread(self, "ImportModels")
        self.thread_ImportModels.signal.connect(self.ImportModels_Finished) 

        # INICIALIZANDO A TELA PRINCIPAL - CONFIGURAÇÕES DA ABA DE GRÁFICOS             
        self.configGraph_list = []
        self.widget_graph_list = []    
        
        self.thread_ReportGraphs = ResReport_Thread(self, "ReportGraphs")
        self.thread_ReportGraphs.signal.connect(self.ReportGraphs_Finished) 
        
        self.init_GraphViewer()

        
        # INICIALIZANDO A TELA PRINCIPAL - CONFIGURAÇÕES DA ABA DE CONJUNTOS DE DADOS        
        self.configSet_list = []
        self.widget_set_list = []
        
        self.button_ReportSets.setVisible(False)         
        self.listwidget_tableHeaders.setVisible(False)
        self.scrollarea_TableHeaders.setVisible(False)
        
        self.thread_PrepareTable = ResReport_Thread(self, "PrepareTable")
        self.thread_PrepareTable.signal.connect(self.PrepareTable_Finished)
        self.thread_Export_toExcel = ResReport_Thread(self, "Export_toExcel")
        self.thread_Export_toExcel.signal.connect(self.Export_toExcel_Finished)
        

        #INICIALIZANDO A TELA DE CONFIGURAÇÃO DE DATAS
        self.configTimestepsParams_graphs = "ALL"
        self.configTimestepsParams_sets = "ALL"
        self.init_ConfigDates()
        
        #INICIALIZANDO A TELA DE CONFIGURAÇÃO DE UNIDADES
        self.configUnits = {}
        self.configUnits['WELLS'] = {}
        self.configUnits['GROUPS'] = {}
        self.configUnits['SECTORS'] = {}
        self.init_ConfigUnits()
        
        
        #INICIALIZANDO A TELA DE CONFIGURAÇÃO DE FORMULAS
        self.configConstants = []
        self.configConstants = self.service.addConstant(self.configConstants, 'TMA', 0.095, "Número")
        self.configConstants = self.service.addConstant(self.configConstants, 'DATA_BASE', datetime(year = 2020, month = 4, day = 13), "Data")
        
        self.configFormulas = []   
        self.init_ConfigFormulas()
        
        
        # INICIALIZANDO A TELA DE CONFIGURAÇÃO DE EDITOR DAS COLUNAS (ORDEM E APELIDOS)
        self.init_ConfigColumns()
        self.configColumnsOrder = {}
                
                            

# -------------------------------------------------------- JANELA PRINCIPAL / PARTE: GERAL
    
    @QtCore.pyqtSlot()
    def on_action_SaveTemplate_triggered(self):  
        if self.models != []:                 
            templateOutput = QFileDialog.getSaveFileName(None, 'Salvar arquivo', 'Config.rtp', 'ResReporter(*.rtp)')[0]
            if templateOutput:             
                with open(templateOutput, 'wb') as configFile:
                    self.SaveGraphs()
                    pickle.dump(self.configGraph_list, configFile)
                    self.SaveSets()
                    pickle.dump(self.configSet_list, configFile)
                    pickle.dump(self.configFormulas, configFile)
                    pickle.dump(self.configConstants, configFile)
                    pickle.dump(self.configUnits, configFile)
                    pickle.dump(self.configTimestepsParams_graphs, configFile)
                    pickle.dump(self.configTimestepsParams_sets, configFile)        
                    pickle.dump(self.configColumnsOrder, configFile)
                value = QMessageBox.information(None, "Concluído", "Arquivo " + str(templateOutput.split("/")[-1]) + " salvo com sucesso.")                
        else:
            value = QMessageBox.warning(None, "Atenção", "Você não adicionou nenhum modelo.")
    
    @QtCore.pyqtSlot()
    def on_action_ImportTemplate_triggered(self):
        if self.models != []:     
            templateInput = QFileDialog.getOpenFileName(None, 'Selecionar arquivo', '.', 'ResReporter(*.rtp)')[0]               
            if templateInput:
                with open(templateInput, 'rb') as configFile:            
                    self.configGraph_list = pickle.load(configFile)
                    self.configSet_list = pickle.load(configFile)                    
                    self.configFormulas = self.configFormulas + pickle.load(configFile)               
                    self.configConstants = self.configConstants + pickle.load(configFile)    
                    self.configUnits = pickle.load(configFile)
                    self.configTimestepsParams_graphs = pickle.load(configFile)
                    self.configTimestepsParams_sets = pickle.load(configFile)        
                    self.configColumnsOrder = pickle.load(configFile)
                    
                    self.init_WidgetGraphs()
                    self.init_WidgetSets()
                    self.loadFormulas()
                    value = QMessageBox.information(None, "Concluído", "Template carregado com sucesso.")   
        else:
            value = QMessageBox.warning(None, "Atenção", "Você não adicionou nenhum modelo.")
            
    @QtCore.pyqtSlot()
    def on_action_AddModels_triggered(self):               
        self.verticalLayout.addWidget(self.spinner)               
        self.new_files = QFileDialog.getOpenFileNames(None, 'Selecionar modelos', '.', '(*.sr3)')[0]
              
#        arquivos = ['Z://AI_FEL3.cmpd//PESSIMISTA_FEL3.cmsd//PESSIMISTA_FEL3_00025_P90_FVMFEL3_v2.sr3', 
#                    'Z://AI_FEL3.cmpd//BASE_FEL3.cmsd//BASE_FEL3_00009_P50_FVMFEL3_v2.sr3']
#        self.new_files = arquivos
        
        if self.new_files != []:
            self.thread_ImportModels.start()              
            self.spinner.start()
            self.centralwidget.setEnabled(False)                 
            
    def ImportModels(self):
        start_time = time.time()
        try:
            for file in self.new_files:                            
                if file not in [modelo.fileSR3 for modelo in self.models]:
    #                General.copyFile(file, file.split("/")[-1])
                    model = self.service.importModel(file)                       
                    self.models.append(model)   
            self.import_Models_Variables_Origins()
            self.loadGraphs()
            self.loadSets()
            print("IMPORTAR MODELO: %s seconds ---" % (time.time() - start_time))
            return "success"
        except Exception as e:
            return str(e.args[-1])
    

    def import_Models_Variables_Origins(self): 
        self.listwidget_ModelsAdded.clear()
        count = 0
        for model in self.models:
            item = QtWidgets.QListWidgetItem(model.name, self.listwidget_ModelsAdded, self.models.index(model))      
            item.setData(QtCore.Qt.UserRole, model)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            self.listwidget_ModelsAdded.addItem(item)

        self.listwidget_ModelsAdded.itemChanged.connect(self.listwidget_ModelsAdded_itemChanged)                

        self.load_Origins(self.models)
        self.load_Variables_OPTIMIZED(self.models[self.listwidget_ModelsAdded.currentRow()])
        
                
        
    def listwidget_ModelsAdded_itemChanged(self, item):
        model = item.data(QtCore.Qt.UserRole)
        model.name = item.text()
        self.loadGraphs()
        self.loadSets()
    
    
    def load_Variables_OPTIMIZED(self, model):
    #JEITO OTIMIZADO = considerando que as variáveis são iguais para todos os modelos
        variables = []
        variables_temp = self.service.importVariables(model, "GROUPS")
        for var in variables_temp:
            if var not in variables:
                variables.append(var)
                if var.outputUnit != None:
                    unit = var.outputUnit
                    mult = str(1)
                else:
                    unit = "-"
                    mult = "-"
            self.configUnits['GROUPS'].update({var.keyword: [unit, mult]})        
        self.modelsVariables['GROUPS'] = variables
        
        variables = []
        variables_temp = self.service.importVariables(model, "WELLS")
        for var in variables_temp:
            if var not in variables:
                variables.append(var)
                if var.outputUnit != None:
                    unit = var.outputUnit
                    mult = str(1)
                else:
                    unit = "-"
                    mult = "-"
                self.configUnits["WELLS"].update({var.keyword: [unit, mult]})
               
        self.modelsVariables['WELLS'] = variables

        variables = []
        variables_temp = self.service.importVariables(model, "SECTORS")
        for var in variables_temp:
            if var not in variables:
                variables.append(var)
                if var.outputUnit != None:
                    unit = var.outputUnit
                    mult = str(1)
                else:
                    unit = "-"
                    mult = "-"
                self.configUnits['SECTORS'].update({var.keyword: [unit, mult]})

        self.modelsVariables['SECTORS'] = variables
    
    def load_Origins(self, models): 
        for model in models:
            origins = []
            origins_temp = self.service.importOrigins(model, "GROUPS")
            for o in origins_temp:
                if o not in origins:
                    origins.append(o)
        
            self.modelsOrigins['GROUPS'] = origins
            
            origins = []
            origins_temp = self.service.importOrigins(model, "WELLS")
            for o in origins_temp:
                if o not in origins:
                    origins.append(o)
        
            self.modelsOrigins['WELLS'] = origins
            
            origins = []
            origins_temp = self.service.importOrigins(model, "SECTORS")
            for o in origins_temp:
                if o not in origins:
                    origins.append(o)
        
            self.modelsOrigins['SECTORS'] = origins
    
    def ImportModels_Finished(self, signal):
        self.centralwidget.setEnabled(True)
        self.spinner.stop()
        if signal != "success":
            value = QMessageBox.warning(None, "Atenção", "Erro ao carregar dados para gerar o gráfico. " + signal)   
        
    @QtCore.pyqtSlot()        
    def on_button_DeleteModel_clicked(self):
        if self.listwidget_ModelsAdded.currentRow() > -1:
            del self.models[self.listwidget_ModelsAdded.currentRow()]
            self.listwidget_ModelsAdded.takeItem(self.listwidget_ModelsAdded.currentRow())   
            self.loadGraphs()
            self.loadSets()
        if len(self.listwidget_ModelsAdded) == 0:
            for widget_graphic in self.widget_graph_list:
                self.verticalLayout_graphListWidget.removeWidget(widget_graphic)
                sip.delete(widget_graphic)
                widget_graphic = None
            self.widget_graph_list = []                
            for widget_set in self.widget_set_list:
                self.verticalLayout_setListWidget.removeWidget(widget_set)
                sip.delete(widget_set)
                widget_set = None
            self.widget_set_list = []                     
  



# ------------------------------------------------- JANELA DO EDITOR DE DATAS ---------------------------
        
   
    def init_ConfigDates(self):
        self.dialog_datesEditor = QtWidgets.QDialog()
        datesEditor_ui = Ui_dialog_datesEditor()
        datesEditor_ui.setupUi(self.dialog_datesEditor)
        
        self.dialog_datesEditor.button_addDayofMonth = self.dialog_datesEditor.findChild(QtWidgets.QPushButton, "button_addDayofMonth")
        self.dialog_datesEditor.button_addDayofMonth.clicked.connect(self.on_button_addDayofMonth_clicked)
        
        self.dialog_datesEditor.button_deleteDayofMonth = self.dialog_datesEditor.findChild(QtWidgets.QPushButton, "button_deleteDayofMonth")
        self.dialog_datesEditor.button_deleteDayofMonth.setStyleSheet("background-color: rgba(255, 255, 255, 0)")
        self.dialog_datesEditor.button_deleteDayofMonth.clicked.connect(self.on_button_deleteDayofMonth_clicked)
        
        self.dialog_datesEditor.lineedit_dayofMonth = self.dialog_datesEditor.findChild(QtWidgets.QLineEdit, "lineedit_dayofMonth")
        validador = QtCore.QRegExp("\d\d")
        self.dialog_datesEditor.lineedit_dayofMonth.setValidator(QtGui.QRegExpValidator(validador, self))
        
        self.dialog_datesEditor.lineedit_startDate = self.dialog_datesEditor.findChild(LineEdit_DateMask, "lineedit_startDate")
        self.dialog_datesEditor.lineedit_endDate = self.dialog_datesEditor.findChild(LineEdit_DateMask, "lineedit_endDate")
        
        self.dialog_datesEditor.listwidget_daysofMonth = self.dialog_datesEditor.findChild(QtWidgets.QListWidget, "listwidget_daysofMonth")
                    
        validador = QtCore.QRegExp("[0-9]{2}/[0-9]{2}/[0-9]{4}")
        self.dialog_datesEditor.lineedit_startDate.setValidator(QtGui.QRegExpValidator(validador, self))
        self.dialog_datesEditor.lineedit_startDate.setInputMask("99/99/9999")
        self.dialog_datesEditor.lineedit_endDate.setValidator(QtGui.QRegExpValidator(validador, self))
        self.dialog_datesEditor.lineedit_endDate.setInputMask("99/99/9999")          

        self.dialog_datesEditor.lineedit_startDate.textChanged.connect(self.lineedit_startDate_textChanged)             
        self.dialog_datesEditor.lineedit_endDate.textChanged.connect(self.lineedit_endDate_textChanged)             
                    
        self.dialog_datesEditor.radiobutton_DatesEditor_Graph = self.dialog_datesEditor.findChild(QtWidgets.QRadioButton, "radiobutton_DatesEditor_Graph")
        self.dialog_datesEditor.radiobutton_DatesEditor_Table = self.dialog_datesEditor.findChild(QtWidgets.QRadioButton, "radiobutton_DatesEditor_Table")
        self.dialog_datesEditor.radiobutton_DatesEditor_Table.setChecked(True)
        
        self.dialog_datesEditor.radiobutton_DatesEditor_Graph.clicked.connect(self.radiobutton_DatesEditor_changed)
        self.dialog_datesEditor.radiobutton_DatesEditor_Table.clicked.connect(self.radiobutton_DatesEditor_changed)
        
        self.dialog_datesEditor.button_saveDates = self.dialog_datesEditor.findChild(QtWidgets.QPushButton, "button_saveDates")
        self.dialog_datesEditor.button_saveDates.clicked.connect(self.on_button_saveDates_clicked)
        
        self.dialog_datesEditor.checkbox_alldates = self.dialog_datesEditor.findChild(QtWidgets.QCheckBox, "checkbox_alldates")
        self.dialog_datesEditor.checkbox_alldates.clicked.connect(self.loadDatesWidgets)
        
    @QtCore.pyqtSlot() 
    def on_action_ConfigDates_triggered(self):
        if self.models != []:     
            self.loadDates()
            self.dialog_datesEditor.exec()                          
        else:
            value = QMessageBox.warning(None, "Atenção", "Você não adicionou nenhum modelo.")
    

    def loadDates(self):                    
        if self.dialog_datesEditor.radiobutton_DatesEditor_Table.isChecked():
            params = self.configTimestepsParams_sets            
        else:
            params = self.configTimestepsParams_graphs
            
        self.dialog_datesEditor.lineedit_startDate.setText("")
        self.dialog_datesEditor.lineedit_endDate.setText("")
        self.dialog_datesEditor.listwidget_daysofMonth.clear()

        if params == "ALL":
            self.dialog_datesEditor.checkbox_alldates.setChecked(True)            
        else:
            self.dialog_datesEditor.checkbox_alldates.setChecked(False)            
            startDate_string = params[0].strftime("%d/%m/%Y")
            self.dialog_datesEditor.lineedit_startDate.setText(startDate_string)
            
            endDate_string = params[1].strftime("%d/%m/%Y")
            self.dialog_datesEditor.lineedit_endDate.setText(endDate_string)
            
            daysofMonth_list = params[2]            
            for day in daysofMonth_list:
                item = QtWidgets.QListWidgetItem(str(day), self.dialog_datesEditor.listwidget_daysofMonth, 0)         
                self.dialog_datesEditor.listwidget_daysofMonth.addItem(item)
        
        self.loadDatesWidgets()        


    def lineedit_startDate_textChanged(self):
        if self.dialog_datesEditor.lineedit_startDate.hasAcceptableInput() == False:
            QtWidgets.QToolTip.showText(self.dialog_datesEditor.lineedit_startDate.mapToGlobal(QtCore.QPoint()), "A data deve ser no formado dd/mm/yyyy")
        else:
            QtWidgets.QToolTip.hideText()
    
    def lineedit_endDate_textChanged(self):
        self.dialog_datesEditor.lineedit_endDate = self.dialog_datesEditor.findChild(LineEdit_DateMask, "lineedit_endDate")
        if self.dialog_datesEditor.lineedit_endDate.hasAcceptableInput() == False:
            QtWidgets.QToolTip.showText(self.dialog_datesEditor.lineedit_endDate.mapToGlobal(QtCore.QPoint()), "A data deve ser no formado dd/mm/yyyy")
        else:
            QtWidgets.QToolTip.hideText()                        
                
    def on_button_addDayofMonth_clicked(self):
        if self.dialog_datesEditor.lineedit_dayofMonth.text() != "":
            day = self.dialog_datesEditor.lineedit_dayofMonth.text()
            if not self.dialog_datesEditor.listwidget_daysofMonth.findItems(day, QtCore.Qt.MatchExactly):
                item = QtWidgets.QListWidgetItem(day, self.dialog_datesEditor.listwidget_daysofMonth, 0)         
                self.dialog_datesEditor.listwidget_daysofMonth.addItem(item)
            self.dialog_datesEditor.lineedit_dayofMonth.setText("")
    
    def on_button_deleteDayofMonth_clicked(self):
        if self.dialog_datesEditor.listwidget_daysofMonth.currentRow() > -1:
            self.dialog_datesEditor.listwidget_daysofMonth.takeItem(self.dialog_datesEditor.listwidget_daysofMonth.currentRow())   
                        
    def loadDatesWidgets(self):
        showWidgets_StartEndDates = True
        showWidgets_DaysofMonth = True
        
        if self.dialog_datesEditor.radiobutton_DatesEditor_Graph.isChecked():      
            showWidgets_DaysofMonth = False
        
        if self.dialog_datesEditor.checkbox_alldates.isChecked():
            showWidgets_StartEndDates = False
            showWidgets_DaysofMonth = False
                
        self.dialog_datesEditor.button_addDayofMonth.setEnabled(showWidgets_DaysofMonth)
        self.dialog_datesEditor.button_deleteDayofMonth.setEnabled(showWidgets_DaysofMonth)
        self.dialog_datesEditor.lineedit_dayofMonth.setEnabled(showWidgets_DaysofMonth)    
        self.dialog_datesEditor.lineedit_startDate.setEnabled(showWidgets_StartEndDates)
        self.dialog_datesEditor.lineedit_endDate.setEnabled(showWidgets_StartEndDates)
    
    def radiobutton_DatesEditor_changed(self):
        self.loadDates()
    
    def on_button_saveDates_clicked(self):
        timesteps_index = []        

        if self.dialog_datesEditor.checkbox_alldates.isChecked():            
            if self.dialog_datesEditor.radiobutton_DatesEditor_Table.isChecked():
                self.configTimestepsParams_sets = "ALL"
                value = QMessageBox.information(None, "Concluído", "Datas para as TABELAS salvas com sucesso. \nSalve também o template para utilizar estas datas nas próximas vezes.")
                return
            else:
                self.configTimestepsParams_graphs = "ALL"
                value = QMessageBox.information(None, "Concluído", "Datas para as CURVAS salvas com sucesso. \nSalve também o template para utilizar estas datas nas próximas vezes.")        
                return
        else:
            if self.dialog_datesEditor.lineedit_startDate.hasAcceptableInput() == False or self.dialog_datesEditor.lineedit_endDate.hasAcceptableInput() == False:
                value = QMessageBox.warning(None, "Atenção", "Você precisa selecionar datas de início e fim válidas.")
                return            
            else:
                startDate = datetime.strptime(self.dialog_datesEditor.lineedit_startDate.text(), '%d/%m/%Y')
                endDate = datetime.strptime(self.dialog_datesEditor.lineedit_endDate.text(), '%d/%m/%Y')
                if endDate < startDate:
                    value = QMessageBox.warning(None, "Atenção", "A data fim deve ser maior que a data de início.")
                    return
                if self.dialog_datesEditor.radiobutton_DatesEditor_Table.isChecked():
                    if self.dialog_datesEditor.listwidget_daysofMonth.count() == 0:
                        value = QMessageBox.warning(None, "Atenção", "Você precisa adicionar ao menos um dia do mês.")
                        return                

            daysofMonth = []
            for row in range(self.dialog_datesEditor.listwidget_daysofMonth.count()):
                item = self.dialog_datesEditor.listwidget_daysofMonth.item(row)
                daysofMonth.append(int(item.text()))      
                
            if self.dialog_datesEditor.radiobutton_DatesEditor_Table.isChecked():
                self.configTimestepsParams_sets = [startDate, endDate, daysofMonth]
                value = QMessageBox.information(None, "Concluído", "Datas para as TABELAS salvas com sucesso. \nSalve também o template para utilizar estas datas nas próximas vezes.")
            else:
                self.configTimestepsParams_graphs = [startDate, endDate, daysofMonth]
                value = QMessageBox.information(None, "Concluído", "Datas para as CURVAS salvas com sucesso. \nSalve também o template para utilizar estas datas nas próximas vezes.")

                
        
        
# ----------------------------------------------------- FIM DA JANELA DO EDITOR DE DATAS ---------------------------



# ------------------------------------------------- JANELA DO EDITOR DE FORMULAS ---------------------------        
    
    def init_ConfigFormulas(self):
        self.dialog_formulasEditor = QtWidgets.QDialog()
        formulasEditor_ui = Ui_dialog_formulasEditor()
        formulasEditor_ui.setupUi(self.dialog_formulasEditor)  
                
        self.dialog_formulasEditor.verticalLayout_formulas = formulasEditor_ui.verticalLayout_formulasAdded
        self.dialog_formulasEditor.verticalLayout_formulas.setAlignment(QtCore.Qt.AlignTop)
                
        self.dialog_formulasEditor.verticalLayout_formulasAdded = formulasEditor_ui.verticalLayout_formulasAdded        
        self.dialog_formulasEditor.verticalLayout_formulasAdded.setAlignment(QtCore.Qt.AlignTop)    

        self.dialog_formulasEditor.button_NewFormula = self.dialog_formulasEditor.findChild(QtWidgets.QPushButton, "button_NewFormula")
        self.dialog_formulasEditor.button_NewFormula.setStyleSheet("background-color: rgba(255, 255, 255, 0)");
        self.dialog_formulasEditor.button_NewFormula.clicked.connect(self.on_button_NewFormula_clicked)              
        
        self.dialog_formulasEditor.lineedit_formulaName = self.dialog_formulasEditor.findChild(QtWidgets.QLineEdit, "lineedit_formulaName")
        validador = QtCore.QRegExp("[a-zA-Z0-9()_ -]+")
        self.dialog_formulasEditor.lineedit_formulaName.setValidator(QtGui.QRegExpValidator(validador, self))
        self.dialog_formulasEditor.lineedit_formulaName.textChanged.connect(self.lineedit_formulaName_textChanged)
        
        self.dialog_formulasEditor.textedit_formulaExpression = self.dialog_formulasEditor.findChild(TextEdit_DropFormulas, "textedit_formulaExpression")
        self.dialog_formulasEditor.textedit_formulaExpression.textChanged.connect(self.textedit_formulaExpression_textChanged)
        
        self.dialog_formulasEditor.lbl_formula_type = self.dialog_formulasEditor.findChild(QtWidgets.QLabel, "lbl_formula_type")
        
        self.dialog_formulasEditor.listwidget_formulas_variables = self.dialog_formulasEditor.findChild(QtWidgets.QListWidget, "listwidget_formulas_variables")
        self.dialog_formulasEditor.combobox_formulas_type = self.dialog_formulasEditor.findChild(QtWidgets.QComboBox, "combobox_formulas_type")
        self.dialog_formulasEditor.combobox_formulas_type.currentTextChanged.connect(self.on_combobox_formulas_type_currentTextChanged)
        self.dialog_formulasEditor.lbl_formula_type.setText(self.dialog_formulasEditor.combobox_formulas_type.currentText())
        
        self.dialog_formulasEditor.listwidget_formulas_constants = self.dialog_formulasEditor.findChild(QtWidgets.QListWidget, "listwidget_formulas_constants")
        self.dialog_formulasEditor.listwidget_formulas_constants.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.dialog_formulasEditor.listwidget_formulas_constants.customContextMenuRequested.connect(self.listwidget_formulas_constants_rightClick)                
        
        self.dialog_formulasEditor.button_SaveConstant = self.dialog_formulasEditor.findChild(QtWidgets.QPushButton, "button_SaveConstant")
        self.dialog_formulasEditor.button_SaveConstant.clicked.connect(self.on_button_SaveConstant_clicked) 
        self.dialog_formulasEditor.lineedit_constantName = self.dialog_formulasEditor.findChild(QtWidgets.QLineEdit, "lineedit_constantName")
        validador = QtCore.QRegExp("[a-zA-Z]+\w*")
        self.dialog_formulasEditor.lineedit_constantName.setValidator(QtGui.QRegExpValidator(validador, self))        
        self.dialog_formulasEditor.lineedit_constantName.textChanged.connect(self.lineedit_constantName_textChanged)
        self.dialog_formulasEditor.lineedit_constantValue = self.dialog_formulasEditor.findChild(QtWidgets.QLineEdit, "lineedit_constantValue")
        self.dialog_formulasEditor.lineedit_constantValue.textChanged.connect(self.lineedit_constantValue_textChanged)
        self.dialog_formulasEditor.combobox_constantType = self.dialog_formulasEditor.findChild(QtWidgets.QComboBox, "combobox_constantType")
        self.dialog_formulasEditor.combobox_constantType.currentTextChanged.connect(self.on_combobox_constantType_currentTextChanged)
        


    
    @QtCore.pyqtSlot()
    def on_action_ConfigFormulas_triggered(self):              
        if self.models != []:     
            self.load_listwidget_formulas_variables()
            self.loadConstants()
            self.dialog_formulasEditor.exec()      
        else:
            value = QMessageBox.warning(None, "Atenção", "Você não adicionou nenhum modelo.")                  


    def loadFormulas(self): 
        for formula in self.configFormulas:
            self.add_Widget_Formula(self.dialog_formulasEditor.verticalLayout_formulasAdded, formula)
    
    def loadConstants(self):
        self.load_listwidget_formulas_constants()
        self.dialog_formulasEditor.lineedit_constantName.setText("")
        self.dialog_formulasEditor.lineedit_constantName.setStyleSheet('QLineEdit { background-color: %s }' % '#ffffff')
        self.dialog_formulasEditor.lineedit_constantValue.setText("")
        self.dialog_formulasEditor.lineedit_constantValue.setStyleSheet('QLineEdit { background-color: %s }' % '#ffffff')
        self.on_combobox_constantType_currentTextChanged()
        
    
    def add_Widget_Formula(self, layout, formula):
        widget_formula = QtWidgets.QWidget()     
        
        countFormulas = len(self.configFormulas)
        countFormulas = countFormulas + 1
        
        formulasView_ui = Ui_widget_formulas()
        formulasView_ui.setupUi(widget_formula)
        widget_formula.setObjectName("widget_formula_" + str(countFormulas))
        
        lbl_formulaName = widget_formula.findChild(QtWidgets.QLabel, "lbl_formulaName")
        lbl_formulaExpression = widget_formula.findChild(QtWidgets.QLabel, "lbl_formulaExpression")
        lbl_formulaType = widget_formula.findChild(QtWidgets.QLabel, "lbl_formulaType")
        
        button_DeleteFormula = widget_formula.findChild(QtWidgets.QPushButton, "button_DeleteFormula")
                
        button_DeleteFormula.setStyleSheet("background-color: rgba(255, 255, 255, 0)");
        button_DeleteFormula.clicked.connect(lambda: self.on_button_DeleteFormula_clicked(widget_formula.objectName()))
        
                                
        lbl_formulaName.setText(formula.name)
        lbl_formulaExpression.setText(formula.expression)      
        lbl_formulaType.setText(formula.timeseriesType)
        
        lbl_formulaName.setStyleSheet("QLabel { font-weight: normal; }");
        lbl_formulaExpression.setStyleSheet("QLabel { font-weight: normal; }");
        lbl_formulaType.setStyleSheet("QLabel { font-weight: normal; }");
        layout.addWidget(widget_formula)          
                
    def on_button_NewFormula_clicked(self):                
        newFormula = Model.Formula()
        if self.dialog_formulasEditor.lineedit_formulaName.hasAcceptableInput() == True:
            newFormula.name = self.dialog_formulasEditor.lineedit_formulaName.text()            
        else:
            QtWidgets.QToolTip.showText(self.dialog_formulasEditor.lineedit_formulaName.mapToGlobal(QtCore.QPoint()), "O nome da fórmula deve conter ao menos uma letra, podendo utilizar números, espaço e underscore.")
            self.dialog_formulasEditor.lineedit_formulaName.setStyleSheet('QLineEdit { background-color: %s }' % '#f6989d')
            return
        
        if self.dialog_formulasEditor.textedit_formulaExpression.toPlainText() != "":
            newFormula.expression = self.dialog_formulasEditor.textedit_formulaExpression.toPlainText()
            newFormula.expression = newFormula.expression.replace("[","")
            newFormula.expression = newFormula.expression.replace("]","")
        else:
            QtWidgets.QToolTip.showText(self.dialog_formulasEditor.textedit_formulaExpression.mapToGlobal(QtCore.QPoint()), "Preecher com dados válidos.")
            self.dialog_formulasEditor.textedit_formulaExpression.setStyleSheet('QTextEdit { background-color: %s }' % '#f6989d')
            return
        newFormula.timeseriesType = self.dialog_formulasEditor.combobox_formulas_type.currentText()
        params = self.service.getParams_byFormulaExpression(newFormula.expression)
        variables_list = []
        for item in self.dialog_formulasEditor.listwidget_formulas_variables.findItems("*", Qt.MatchWrap | Qt.MatchWildcard):
            if item.text() == 'DATE':
                variables_list.append('DATE')
            else:
                variables_list.append(item.data(QtCore.Qt.UserRole).keyword)        
        newFormula.variables = variables_list
        newFormula.constants = self.service.getConstants_fromList_byParams(params, self.configConstants)
        
        self.configFormulas.append(newFormula) 
        self.add_Widget_Formula(self.dialog_formulasEditor.verticalLayout_formulasAdded, newFormula)
        
        self.dialog_formulasEditor.lineedit_formulaName.setText("")
        self.dialog_formulasEditor.textedit_formulaExpression.setText("")                    
        
        for widget_graphic in self.widget_graph_list: 
            self.load_listwidget_graph_formulas(widget_graphic)
            
        for widget_set in self.widget_set_list: 
            self.load_listwidget_set_formulas(widget_set)
    
    def on_combobox_formulas_type_currentTextChanged(self):
        self.load_listwidget_formulas_variables()
        self.dialog_formulasEditor.lbl_formula_type.setText(self.dialog_formulasEditor.combobox_formulas_type.currentText())
        
    
    def load_listwidget_formulas_variables(self):                
        timeseriesType = self.dialog_formulasEditor.combobox_formulas_type.currentText()
        variables = self.modelsVariables[timeseriesType]
                
        self.dialog_formulasEditor.listwidget_formulas_variables.clear()
        self.dialog_formulasEditor.listwidget_formulas_variables.setDragEnabled(True)
        
        var = Model.Variable()
        var.keyword = 'DATE'
        item = QtWidgets.QListWidgetItem('DATE', self.dialog_formulasEditor.listwidget_formulas_variables, 0)            
        item.setData(QtCore.Qt.UserRole, var)
        self.dialog_formulasEditor.listwidget_formulas_variables.addItem(item)
        variables.sort(key = lambda v: v.keyword)
        for var in variables:
            if var.keyword in self.configUnits[timeseriesType].keys():
                outputUnit = self.configUnits[timeseriesType][var.keyword][0]
            else:                
                outputUnit = var.outputUnit 
            item = QtWidgets.QListWidgetItem(var.keyword + " (" + outputUnit + ")", self.dialog_formulasEditor.listwidget_formulas_variables, 0)            
            item.setData(QtCore.Qt.UserRole, var)
            self.dialog_formulasEditor.listwidget_formulas_variables.addItem(item)
            
    def load_listwidget_formulas_constants(self):                                      
        self.dialog_formulasEditor.listwidget_formulas_constants.clear()
        self.dialog_formulasEditor.listwidget_formulas_constants.setDragEnabled(True)
        
        for constant in self.configConstants:
            item = QtWidgets.QListWidgetItem(constant.name + ": " + self.service.constantValue_toString(constant), self.dialog_formulasEditor.listwidget_formulas_constants, 0)                        
            item.setData(QtCore.Qt.UserRole, constant)
            self.dialog_formulasEditor.listwidget_formulas_constants.addItem(item)
                    
    
    def listwidget_formulas_constants_rightClick(self, QPos):
        self.listMenu= QtWidgets.QMenu()
        menu_item_delete = self.listMenu.addAction("Excluir")
        menu_item_edit = self.listMenu.addAction("Editar")
        menu_item_delete.triggered.connect(self.listwidget_formulas_constants_rightClick_delete) 
        menu_item_edit.triggered.connect(self.listwidget_formulas_constants_rightClick_edit) 
        parentPosition = self.dialog_formulasEditor.listwidget_formulas_constants.mapToGlobal(QtCore.QPoint(0, 0))        
        self.listMenu.move(parentPosition + QPos)
        self.listMenu.show()
    
    def listwidget_formulas_constants_rightClick_edit(self):
        row = self.dialog_formulasEditor.listwidget_formulas_constants.currentRow()
        item = self.dialog_formulasEditor.listwidget_formulas_constants.item(row)
        constant = item.data(QtCore.Qt.UserRole)
        
        self.dialog_formulasEditor.lineedit_constantName.setText(constant.name)
        self.dialog_formulasEditor.lineedit_constantValue.setText(self.service.constantValue_toString(constant))
        if constant.type_ == "Data":
            self.dialog_formulasEditor.combobox_constantType.setCurrentText("Data")
        elif constant.type_ == "Número":
            self.dialog_formulasEditor.combobox_constantType.setCurrentText("Número")
        
    def listwidget_formulas_constants_rightClick_delete(self):
        row = self.dialog_formulasEditor.listwidget_formulas_constants.currentRow()
        item = self.dialog_formulasEditor.listwidget_formulas_constants.item(row)
        self.dialog_formulasEditor.listwidget_formulas_constants.takeItem(row)
        
        self.configConstants.remove(item.data(QtCore.Qt.UserRole))
            
    def on_combobox_constantType_currentTextChanged(self):           
        
        if self.dialog_formulasEditor.combobox_constantType.currentText() == "Número":            
            validador = QtCore.QRegExp("\d+.?\d*")
            self.dialog_formulasEditor.lineedit_constantValue.setValidator(QtGui.QRegExpValidator(validador, self))
        elif self.dialog_formulasEditor.combobox_constantType.currentText() == "Data":            
            validador = QtCore.QRegExp("[0-9]{2}/[0-9]{2}/[0-9]{4}")
            self.dialog_formulasEditor.lineedit_constantValue.setValidator(QtGui.QRegExpValidator(validador, self))
                
            
    def lineedit_constantValue_textChanged(self):
        if self.dialog_formulasEditor.combobox_constantType.currentText() == "Data":  
            if self.dialog_formulasEditor.lineedit_constantValue.hasAcceptableInput() == False:
                QtWidgets.QToolTip.showText(self.dialog_formulasEditor.lineedit_constantValue.mapToGlobal(QtCore.QPoint()), "A data deve ser no formado dd/mm/yyyy")
            else:
                self.dialog_formulasEditor.lineedit_constantValue.setStyleSheet('QLineEdit { background-color: %s }' % '#ffffff')
                QtWidgets.QToolTip.hideText()
        elif self.dialog_formulasEditor.combobox_constantType.currentText() == "Número":  
            if self.dialog_formulasEditor.lineedit_constantValue.hasAcceptableInput() == False:
                QtWidgets.QToolTip.showText(self.dialog_formulasEditor.lineedit_constantValue.mapToGlobal(QtCore.QPoint()), "Informar um valor inteiro ou decimal.")
            else:
                self.dialog_formulasEditor.lineedit_constantValue.setStyleSheet('QLineEdit { background-color: %s }' % '#ffffff')
                QtWidgets.QToolTip.hideText()
    
    def lineedit_constantName_textChanged(self):
            if self.dialog_formulasEditor.lineedit_constantName.hasAcceptableInput() == False:
                QtWidgets.QToolTip.showText(self.dialog_formulasEditor.lineedit_constantName.mapToGlobal(QtCore.QPoint()), "O nome da constante deve conter ao menos uma letra, podendo utilizar números e underscore.")
            else:
                self.dialog_formulasEditor.lineedit_constantName.setStyleSheet('QLineEdit { background-color: %s }' % '#ffffff')
                QtWidgets.QToolTip.hideText()     
    
    def lineedit_formulaName_textChanged(self):
            if self.dialog_formulasEditor.lineedit_formulaName.hasAcceptableInput() == False:
                QtWidgets.QToolTip.showText(self.dialog_formulasEditor.lineedit_formulaName.mapToGlobal(QtCore.QPoint()), "O nome da fórmula deve conter ao menos uma letra, podendo utilizar números, espaço e underscore.")
            else:
                self.dialog_formulasEditor.lineedit_formulaName.setStyleSheet('QLineEdit { background-color: %s }' % '#ffffff')
                QtWidgets.QToolTip.hideText()     
    
    def textedit_formulaExpression_textChanged(self):
            if self.dialog_formulasEditor.textedit_formulaExpression.toPlainText() == "":
                QtWidgets.QToolTip.showText(self.dialog_formulasEditor.textedit_formulaExpression.mapToGlobal(QtCore.QPoint()), "Preencher com dados válidos.")
            else:
                self.dialog_formulasEditor.textedit_formulaExpression.setStyleSheet('QTextEdit { background-color: %s }' % '#ffffff')
                QtWidgets.QToolTip.hideText() 
    
                
    def on_button_SaveConstant_clicked(self):
        constant = Model.Constant()
        if self.dialog_formulasEditor.lineedit_constantName.hasAcceptableInput() == True:
            constant.name = self.dialog_formulasEditor.lineedit_constantName.text()  
        else:
            QtWidgets.QToolTip.showText(self.dialog_formulasEditor.lineedit_constantName.mapToGlobal(QtCore.QPoint()), "O nome da constante deve conter ao menos uma letra, podendo utilizar números e underscore.")
            self.dialog_formulasEditor.lineedit_constantName.setStyleSheet('QLineEdit { background-color: %s }' % '#f6989d')
            return
        
        constant.type_ = self.dialog_formulasEditor.combobox_constantType.currentText()                      
        
        if self.dialog_formulasEditor.lineedit_constantValue.hasAcceptableInput() == True:        
            if self.dialog_formulasEditor.combobox_constantType.currentText() == "Número":
                constant.value = float(self.dialog_formulasEditor.lineedit_constantValue.text())
            if self.dialog_formulasEditor.combobox_constantType.currentText() == "Data":
                constant.value = datetime.strptime(self.dialog_formulasEditor.lineedit_constantValue.text()  , '%d/%m/%Y')
        else:            
            QtWidgets.QToolTip.showText(self.dialog_formulasEditor.lineedit_constantValue.mapToGlobal(QtCore.QPoint()), "Entrada inválida.")
            self.dialog_formulasEditor.lineedit_constantValue.setStyleSheet('QLineEdit { background-color: %s }' % '#f6989d')
            return
        
        c = self.service.getConstant_fromList_byName(self.configConstants, constant.name)
        if c != None:
            self.configConstants.remove(c)            
            
        self.configConstants.append(constant)
        
        self.loadConstants()
        
        for widget_graphic in self.widget_graph_list: 
            self.load_listwidget_graph_formulas(widget_graphic)
            
        for widget_set in self.widget_set_list: 
            self.load_listwidget_set_formulas(widget_set)
            
     
    def on_button_DeleteFormula_clicked(self, objectName):
        widget_formula =  self.dialog_formulasEditor.findChild(QtWidgets.QWidget, objectName)
        lbl_formulaName = widget_formula.findChild(QtWidgets.QLabel, "lbl_formulaName")
        lbl_formulaType = widget_formula.findChild(QtWidgets.QLabel, "lbl_formulaType")
          
        formula = self.service.getFormula_fromList_byName(self.configFormulas, lbl_formulaName.text())

        self.configFormulas.remove(formula)
        
        self.dialog_formulasEditor.verticalLayout_formulasAdded.removeWidget(widget_formula)
        sip.delete(widget_formula)        
        widget_formula = None    
        
        for widget_graphic in self.widget_graph_list: 
            self.load_listwidget_graph_formulas(widget_graphic)
            
        for widget_set in self.widget_set_list: 
            self.load_listwidget_set_formulas(widget_set)
        
    def loadBasicFormulas(self, timeseriesType):              
        basicFormulas = {}
        basicFormulas['WELLS'] = []
        basicFormulas['GROUPS'] = []
        basicFormulas['SECTORS'] = []
        
        basicFormulas['WELLS'] = self.service.addFormula(basicFormulas['WELLS'], 'Oil Rate SC - INST', 'OILRATSC/ONFRAC', ['OILRATSC', 'ONFRAC'])
        basicFormulas['WELLS'] = self.service.addFormula(basicFormulas['WELLS'], 'Gas Rate SC - INST', 'GASRATSC/ONFRAC', ['GASRATSC', 'ONFRAC'])
        basicFormulas['WELLS'] = self.service.addFormula(basicFormulas['WELLS'], 'Water Rate SC - INST', 'WATRATSC/ONFRAC', ['WATRATSC', 'ONFRAC'])
        basicFormulas['WELLS'] = self.service.addFormula(basicFormulas['WELLS'], 'Liquid Rate SC - INST', 'LIQRATSC/ONFRAC', ['LIQRATSC', 'ONFRAC'])
        basicFormulas['WELLS'] = self.service.addFormula(basicFormulas['WELLS'], 'RGO', 'GASRATSC/OILRATSC', ['GASRATSC', 'OILRATSC'])
        basicFormulas['WELLS'] = self.service.addFormula(basicFormulas['WELLS'], 'RGL', 'GASRATSC/LIQRATSC', ['GASRATSC', 'LIQRATSC'])
        basicFormulas['WELLS'] = self.service.addFormula(basicFormulas['WELLS'], 'BSW(%)', 'WATRATSC*100/LIQRATSC', ['WATRATSC', 'LIQRATSC'])
        basicFormulas['WELLS'] = self.service.addFormula(basicFormulas['WELLS'], 'IP', '(LIQRATSC/ONFRAC)/(BLOCKP - BHP)', ['LIQRATSC', 'ONFRAC', 'BLOCKP', 'BHP'])
        basicFormulas['WELLS'] = self.service.addFormula(basicFormulas['WELLS'], 'QGL', 'derivative(CGLIFT, OFFSET)', ['CGLIFT', 'OFFSET'])
        basicFormulas['WELLS'] = self.service.addFormula(basicFormulas['WELLS'], 'Oil Rate RC - INST', 'OILRATRC/ONFRAC', ['OILRATRC', 'ONFRAC'])
        basicFormulas['WELLS'] = self.service.addFormula(basicFormulas['WELLS'], 'Gas Rate RC - INST', 'GASRATRC/ONFRAC', ['GASRATRC', 'ONFRAC'])
        basicFormulas['WELLS'] = self.service.addFormula(basicFormulas['WELLS'], 'Water Rate RC - INST', 'WATRATRC/ONFRAC', ['WATRATRC', 'ONFRAC'])
        basicFormulas['WELLS'] = self.service.addFormula(basicFormulas['WELLS'], 'Liquid Rate RC - INST', 'LIQRATRC/ONFRAC', ['LIQRATRC', 'ONFRAC'])        
        basicFormulas['WELLS'] = self.service.addFormula(basicFormulas['WELLS'], 'Np atualizado', 'np_updated(OILVOLSC, DATE, DATA_BASE, TMA)', ['OILVOLSC', 'DATE'], self.service.getConstants_fromList_byParams(['TMA', 'DATA_BASE'], self.configConstants))
        
        
        basicFormulas['GROUPS'] = self.service.addFormula(basicFormulas['GROUPS'], 'Oil Rate SC - INST', 'OILRATSC/ONFRAC', ['OILRATSC', 'ONFRAC'])
        basicFormulas['GROUPS'] = self.service.addFormula(basicFormulas['GROUPS'], 'Gas Rate SC - INST', 'GASRATSC/ONFRAC', ['GASRATSC', 'ONFRAC'])
        basicFormulas['GROUPS'] = self.service.addFormula(basicFormulas['GROUPS'], 'Water Rate SC - INST', 'WATRATSC/ONFRAC', ['WATRATSC', 'ONFRAC'])
        basicFormulas['GROUPS'] = self.service.addFormula(basicFormulas['GROUPS'], 'Liquid Rate SC - INST', 'LIQRATSC/ONFRAC', ['LIQRATSC', 'ONFRAC'])
        basicFormulas['GROUPS'] = self.service.addFormula(basicFormulas['GROUPS'], 'RGO', 'GASRATSC/OILRATSC', ['GASRATSC', 'OILRATSC'])
        basicFormulas['GROUPS'] = self.service.addFormula(basicFormulas['GROUPS'], 'RGL', 'GASRATSC/LIQRATSC', ['GASRATSC', 'LIQRATSC'])
        basicFormulas['GROUPS'] = self.service.addFormula(basicFormulas['GROUPS'], 'BSW(%)', 'WATRATSC*100/LIQRATSC', ['WATRATSC', 'LIQRATSC'])        
        basicFormulas['GROUPS'] = self.service.addFormula(basicFormulas['GROUPS'], 'Oil Rate RC - INST', 'OILRATRC/ONFRAC', ['OILRATRC', 'ONFRAC'])
        basicFormulas['GROUPS'] = self.service.addFormula(basicFormulas['GROUPS'], 'Gas Rate RC - INST', 'GASRATRC/ONFRAC', ['GASRATRC', 'ONFRAC'])
        basicFormulas['GROUPS'] = self.service.addFormula(basicFormulas['GROUPS'], 'Water Rate RC - INST', 'WATRATRC/ONFRAC', ['WATRATRC', 'ONFRAC'])
        basicFormulas['GROUPS'] = self.service.addFormula(basicFormulas['GROUPS'], 'Liquid Rate RC - INST', 'LIQRATRC/ONFRAC', ['LIQRATRC', 'ONFRAC'])        
        basicFormulas['GROUPS'] = self.service.addFormula(basicFormulas['GROUPS'], 'Np atualizado', 'np_updated(OILVOLSC, DATE, DATA_BASE, TMA)', ['OILVOLSC', 'DATE'], self.service.getConstants_fromList_byParams(['TMA', 'DATA_BASE'], self.configConstants))
                
       
        basicFormulas['SECTORS'] = []       
        
        return basicFormulas[timeseriesType]
# ----------------------------------------------------- FIM DA JANELA DO EDITOR DE FORMULAS ---------------------------
            
# ------------------------------------------------- JANELA DO EDITOR DE UNIDADES ---------------------------            

    def init_ConfigUnits(self):
        self.dialog_unitsEditor = QtWidgets.QDialog()
        unitsEditor_ui = Ui_dialog_unitsEditor()
        
                
        unitsEditor_ui.setupUi(self.dialog_unitsEditor)  
                
        self.dialog_unitsEditor.button_SaveUnit = self.dialog_unitsEditor.findChild(QtWidgets.QPushButton, "button_SaveUnit")
        self.dialog_unitsEditor.button_SaveUnit.clicked.connect(self.on_button_SaveUnit_clicked)
        
        self.dialog_unitsEditor.combobox_timeseriesType = self.dialog_unitsEditor.findChild(QtWidgets.QComboBox, "combobox_timeseriesType")
        self.dialog_unitsEditor.combobox_timeseriesType.currentTextChanged.connect(self.on_combobox_timeseriesType_currentTextChanged)
        
        self.dialog_unitsEditor.combobox_timeseriesType.setCurrentIndex(0)
        
        self.dialog_unitsEditor.listwidget_variables = self.dialog_unitsEditor.findChild(QtWidgets.QListWidget, "listwidget_variables")        
        self.dialog_unitsEditor.listwidget_variables.itemClicked.connect(self.listwidget_variables_item_clicked)
        
        self.dialog_unitsEditor.lbl_variable = self.dialog_unitsEditor.findChild(QtWidgets.QLabel, "lbl_variable")
        self.dialog_unitsEditor.lbl_unitName_orignal = self.dialog_unitsEditor.findChild(QtWidgets.QLabel, "lbl_unitName_orignal")
        
        self.dialog_unitsEditor.lineedit_unitName_new = self.dialog_unitsEditor.findChild(QtWidgets.QLineEdit, "lineedit_unitName_new")
        validador = QtCore.QRegExp("[a-zA-Z0-9()_ -]+")
        self.dialog_unitsEditor.lineedit_unitName_new.setValidator(QtGui.QRegExpValidator(validador, self))
        self.dialog_unitsEditor.lineedit_unitName_new.textChanged.connect(self.lineedit_unitName_new_textChanged)
       
        self.dialog_unitsEditor.lineedit_unitMultplier = self.dialog_unitsEditor.findChild(QtWidgets.QLineEdit, "lineedit_unitMultplier")        
        validador = QtCore.QRegExp("[0-9]+.?[0-9]*")
        self.dialog_unitsEditor.lineedit_unitMultplier.setValidator(QtGui.QRegExpValidator(validador, self))
        self.dialog_unitsEditor.lineedit_unitMultplier.textChanged.connect(self.lineedit_unitMultplier_textChanged)
        
    @QtCore.pyqtSlot()
    def on_action_ConfigUnit_triggered(self):
        if self.models != []:     
            self.load_listwidget_units_variables()
            
            self.dialog_unitsEditor.exec()      
        else:
            value = QMessageBox.warning(None, "Atenção", "Você não adicionou nenhum modelo.")               
 
    def loadUnitEditor(self, timeseriesType, item):        
        var = item.data(QtCore.Qt.UserRole)           
        
        self.dialog_unitsEditor.lbl_variable.setText(var.name)
        if var.outputUnit != None:
            self.dialog_unitsEditor.lbl_unitName_orignal.setText(var.outputUnit)
        else:
            self.dialog_unitsEditor.lbl_unitName_orignal.setText("-")
        
        self.dialog_unitsEditor.lineedit_unitName_new.setText(self.configUnits[timeseriesType][var.keyword][0])
        self.dialog_unitsEditor.lineedit_unitMultplier.setText(self.configUnits[timeseriesType][var.keyword][1])
        
        
    def load_listwidget_units_variables(self):
        timeseriesType = self.dialog_unitsEditor.combobox_timeseriesType.currentText()
        variables = self.modelsVariables[timeseriesType]              
        self.dialog_unitsEditor.listwidget_variables.clear()        
        variables.sort(key = lambda v: v.keyword)
        for var in variables:
            item = QtWidgets.QListWidgetItem(var.keyword, self.dialog_unitsEditor.listwidget_variables, 0)            
            item.setData(QtCore.Qt.UserRole, var)
            self.dialog_unitsEditor.listwidget_variables.addItem(item)        
                            
        self.dialog_unitsEditor.listwidget_variables.setCurrentRow(0)
        item = self.dialog_unitsEditor.listwidget_variables.item(self.dialog_unitsEditor.listwidget_variables.currentRow())
        self.loadUnitEditor(timeseriesType, item)
        
    def listwidget_variables_item_clicked(self, item):
        timeseriesType = self.dialog_unitsEditor.combobox_timeseriesType.currentText()        
        self.loadUnitEditor(timeseriesType, item)
        
    def on_combobox_timeseriesType_currentTextChanged(self):
        self.load_listwidget_units_variables()
            
    def on_button_SaveUnit_clicked(self):
        timeseriesType = self.dialog_unitsEditor.combobox_timeseriesType.currentText()
        item = self.dialog_unitsEditor.listwidget_variables.item(self.dialog_unitsEditor.listwidget_variables.currentRow())
        var = item.data(QtCore.Qt.UserRole)  
        
        if self.dialog_unitsEditor.lineedit_unitName_new.hasAcceptableInput() == True:
            newUnitName = self.dialog_unitsEditor.lineedit_unitName_new.text()
        else:
            QtWidgets.QToolTip.showText(self.dialog_unitsEditor.lineedit_unitName_new.mapToGlobal(QtCore.QPoint()), "O nome da unidade deve conter ao menos uma letra, podendo utilizar números, espaço e underscore.")
            self.dialog_unitsEditor.lineedit_unitName_new.setStyleSheet('QLineEdit { background-color: %s }' % '#f6989d')
            return
        
        if self.dialog_unitsEditor.lineedit_unitMultplier.hasAcceptableInput() == True:
            newUnitMultiplier = self.dialog_unitsEditor.lineedit_unitMultplier.text()
        else:
            QtWidgets.QToolTip.showText(self.dialog_unitsEditor.lineedit_unitMultplier.mapToGlobal(QtCore.QPoint()), "Informar um valor inteiro ou decimal.")
            self.dialog_unitsEditor.lineedit_unitMultplier.setStyleSheet('QLineEdit { background-color: %s }' % '#f6989d')
            return    

        self.configUnits[timeseriesType].update({var.keyword: [newUnitName, newUnitMultiplier]})
        self.configUnits.update({timeseriesType: self.configUnits[timeseriesType]})
        
        for widget_graphic in self.widget_graph_list: 
            self.load_listwidget_graph_variables(widget_graphic)
            
        for widget_set in self.widget_set_list: 
            self.load_listwidget_set_variables(widget_set)

        value = QMessageBox.information(None, "Concluído", "Nova unidade salva com sucesso. Salve também o template para utilizar esta unidade nas próximas vezes.")

    def lineedit_unitName_new_textChanged(self):
            if self.dialog_unitsEditor.lineedit_unitName_new.hasAcceptableInput() == False:
                QtWidgets.QToolTip.showText(self.dialog_unitsEditor.lineedit_unitName_new.mapToGlobal(QtCore.QPoint()), "Preencher com dados válidos.")
            else:
                self.dialog_unitsEditor.lineedit_unitName_new.setStyleSheet('QLineEdit { background-color: %s }' % '#ffffff')
                QtWidgets.QToolTip.hideText() 
    
    def lineedit_unitMultplier_textChanged(self):
            if self.dialog_unitsEditor.lineedit_unitMultplier.hasAcceptableInput() == False:
                QtWidgets.QToolTip.showText(self.dialog_unitsEditor.lineedit_unitMultplier.mapToGlobal(QtCore.QPoint()), "Informar um valor inteiro ou decimal.")
            else:
                self.dialog_unitsEditor.lineedit_unitMultplier.setStyleSheet('QLineEdit { background-color: %s }' % '#ffffff')
                QtWidgets.QToolTip.hideText() 
    
# ----------------------------------------------------- FIM DA JANELA DO EDITOR DE UNIDADES ---------------------------
            


        
# ------------------------------------------------- JANELA DO EDITOR DAS COLUNAS (ORDEM E APELIDOS)  ---------------------------    
        
    def init_ConfigColumns(self):
        self.dialog_columnsEditor = QtWidgets.QDialog()
        columnsEditor_ui = Ui_dialog_columnsEditor()
        columnsEditor_ui.setupUi(self.dialog_columnsEditor)  
                

        self.dialog_columnsEditor.combobox_columns_type = self.dialog_columnsEditor.findChild(QtWidgets.QComboBox, "combobox_columns_type")
        self.dialog_columnsEditor.combobox_columns_type.currentTextChanged.connect(self.on_combobox_columns_type_currentTextChanged)
        
        self.dialog_columnsEditor.listwidget_columns_variables = self.dialog_columnsEditor.findChild(QtWidgets.QListWidget, "listwidget_columns_variables")
        self.dialog_columnsEditor.listwidget_columns_formulas = self.dialog_columnsEditor.findChild(QtWidgets.QListWidget, "listwidget_columns_formulas")
            
        self.dialog_columnsEditor.listwidget_columnsEdit = self.dialog_columnsEditor.findChild(ListWidget_DropVariables, "listwidget_columnsEdit")
        self.dialog_columnsEditor.listwidget_columnsEdit.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.dialog_columnsEditor.listwidget_columnsEdit.customContextMenuRequested.connect(self.listwidget_columnsEdit_rightClick)
        self.dialog_columnsEditor.listwidget_columnsEdit.setStyleSheet("QListWidget::item { "
                                                                                              "border-style: solid;" 
                                                                                              "border-width: 1px;" 
                                                                                              "border-color: black;}"                                                   
                                                                        "QListWidget::item:selected {"
                                                                                              "border-style: solid;" 
                                                                                              "border-width: 1px;" 
                                                                                              "border-color: black;" 
                                                                                              "color: black; }")
                                                
        self.dialog_columnsEditor.button_SaveColumns = self.dialog_columnsEditor.findChild(QtWidgets.QPushButton, "button_SaveColumns")                        
        self.dialog_columnsEditor.button_SaveColumns.clicked.connect(self.on_button_SaveColumns_clicked)
    
    @QtCore.pyqtSlot()
    def on_action_ConfigColumns_triggered(self):              
        if self.models != []:     
            self.loadColumns()
            self.dialog_columnsEditor.exec()      
        else:
            value = QMessageBox.warning(None, "Atenção", "Você não adicionou nenhum modelo.")                  


    def on_combobox_columns_type_currentTextChanged(self):
        self.load_listwidget_columns_variables()
        self.load_listwidget_columns_formulas()
    
    def loadColumns(self):
        self.load_listwidget_columns_variables()
        self.load_listwidget_columns_formulas()
        self.load_listwidget_columnsEdit()
    
    def load_listwidget_columns_variables(self):
        timeseriesType = self.dialog_formulasEditor.combobox_formulas_type.currentText()
        variables = self.modelsVariables[timeseriesType]
        
        variables.sort(key = lambda v: v.keyword)
        self.dialog_columnsEditor.listwidget_columns_variables.clear()        
        for var in variables:
            ouputUnit = ""
            if var.keyword in self.configUnits[timeseriesType].keys():
                outputUnit = self.configUnits[timeseriesType][var.keyword][0]
            else:                
                outputUnit = var.outputUnit 
            item = QtWidgets.QListWidgetItem(var.keyword + " (" + outputUnit + ")", self.dialog_columnsEditor.listwidget_columns_variables, 0)            
            item.setData(QtCore.Qt.UserRole, var.keyword)
            self.dialog_columnsEditor.listwidget_columns_variables.addItem(item)        
                            
    def load_listwidget_columns_formulas(self):       
        timeseriesType = self.dialog_columnsEditor.combobox_columns_type.currentText()
        
        formulas = self.loadBasicFormulas(timeseriesType)
        formulas = formulas + self.service.getFormulaList_fromList_byTimeseriesType(self.configFormulas, timeseriesType)
        formulas.sort(key = lambda f: f.name)
        self.dialog_columnsEditor.listwidget_columns_formulas.clear()        
        for formula in formulas:
            item = QtWidgets.QListWidgetItem(formula.name, self.dialog_columnsEditor.listwidget_columns_formulas, 0)            
            item.setData(QtCore.Qt.UserRole, formula.name)
            self.dialog_columnsEditor.listwidget_columns_formulas.addItem(item)      
    
    
    def load_listwidget_columnsEdit(self):
        self.dialog_columnsEditor.listwidget_columnsEdit.clear()
        for columnName, columnAlias in self.configColumnsOrder.items():
            item = QtWidgets.QListWidgetItem(columnAlias, self.dialog_columnsEditor.listwidget_columnsEdit, 0)
            item.setData(QtCore.Qt.UserRole, columnName)                        
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable) 
            self.dialog_columnsEditor.listwidget_columnsEdit.addItem(item)  
    
    def listwidget_columnsEdit_rightClick(self, QPos):
        self.listMenu= QtWidgets.QMenu()
        menu_item = self.listMenu.addAction("Excluir")
        menu_item.triggered.connect(self.listwidget_columnsEdit_rightClick_delete) 
        parentPosition = self.dialog_columnsEditor.listwidget_columnsEdit.mapToGlobal(QtCore.QPoint(0, 0))        
        self.listMenu.move(parentPosition + QPos)
        self.listMenu.show()
    
    def listwidget_columnsEdit_rightClick_delete(self):
        self.dialog_columnsEditor.listwidget_columnsEdit.takeItem(self.dialog_columnsEditor.listwidget_columnsEdit.currentRow())
    
    def on_button_SaveColumns_clicked(self):
        self.configColumnsOrder = {}
        try:
            for index in range(self.dialog_columnsEditor.listwidget_columnsEdit.count()):
                item = self.dialog_columnsEditor.listwidget_columnsEdit.item(index)
                self.configColumnsOrder.update({item.data(QtCore.Qt.UserRole): item.text()})            
            value = QMessageBox.information(None, "Concluído", "Colunas salvas com sucesso. Salve também o template para utilizar esta configuração nas próximas vezes.")
        except Exception as e:
            value = QMessageBox.warning(None, "Atenção", "Erro ao salvar as colunas: " + str(e.args[-1]))        

    
            
# ------------------------------------------------- FIM JANELA DO EDITOR DA COLUNAS (ORDEM E APELIDOS)  ---------------------------      



# ----------------------------------------------------- JANELA PRINCIPAL: INÍCIO DA ABA CURVAS ------------------------------------
        
    def addGraph(self, graph = None):        
        widget_graphic = QtWidgets.QWidget()
        graphEditor_ui = Ui_widget_graphEditor()
        graphEditor_ui.setupUi(widget_graphic)
        
        contGraph = len(self.widget_graph_list)
        widget_graphic.index = contGraph     
                
        contGraph = contGraph + 1        
        
        lbl_graphHeader =  widget_graphic.findChild(QtWidgets.QLabel, "lbl_graphHeader")  
        lbl_graph_typeHeader =  widget_graphic.findChild(QtWidgets.QLabel, "lbl_graph_typeHeader")
        lbl_graph_originsHeader =  widget_graphic.findChild(QtWidgets.QLabel, "lbl_graph_originsHeader")
        lbl_graph_variablesHeader =  widget_graphic.findChild(QtWidgets.QLabel, "lbl_graph_variablesHeader")
        
        if(contGraph != 1):
            lbl_graphHeader.setVisible(False)
            lbl_graph_typeHeader.setVisible(False)
            lbl_graph_originsHeader.setVisible(False)
            lbl_graph_variablesHeader.setVisible(False)
        
        lbl_graphName =  widget_graphic.findChild(QtWidgets.QLabel, "lbl_graphName")
        if graph == None:
            lbl_graphName.setText("GRÁFICO " + str(contGraph))
        else:
            lbl_graphName.setText(graph.name)
            
        widget_graphic.name = lbl_graphName.text()
        lbl_graphName.setHidden(False)
        
        button_DeleteGraph =  widget_graphic.findChild(QtWidgets.QPushButton, "button_DeleteGraph")
        button_DeleteGraph.setHidden(False)
        button_DeleteGraph.clicked.connect(self.on_button_DeleteGraph_clicked)
        
        button_EditGraph =  widget_graphic.findChild(QtWidgets.QPushButton, "button_EditGraph")
        button_EditGraph.setHidden(False)
        button_EditGraph.clicked.connect(self.on_button_EditGraph_clicked)        
        
        lineedit_graphName =  widget_graphic.findChild(QtWidgets.QLineEdit, "lineedit_graphName")
        lineedit_graphName.setHidden(True)
        validador = QtCore.QRegExp("[a-zA-Z0-9()_ -]+")
        lineedit_graphName.setValidator(QtGui.QRegExpValidator(validador, self))
        lineedit_graphName.textChanged.connect(self.lineedit_graphName_textChanged)
                
        button_SaveGraph =  widget_graphic.findChild(QtWidgets.QPushButton, "button_SaveGraph")
        button_SaveGraph.setHidden(True)   
        button_SaveGraph.clicked.connect(self.on_button_SaveGraph_clicked)
        
        combobox_graph_type =  widget_graphic.findChild(QtWidgets.QComboBox, "combobox_graph_type")
        combobox_graph_type.currentTextChanged.connect(self.on_combobox_graph_type_currentTextChanged)
        if graph != None:
            index = combobox_graph_type.findText(graph.timeseriesType, QtCore.Qt.MatchFixedString)
            if index >= 0:
                combobox_graph_type.setCurrentIndex(index)
        
        radiobutton_graph_cathegoryOrigin =  widget_graphic.findChild(QtWidgets.QRadioButton, "radiobutton_graph_cathegoryOrigin")        
        radiobutton_graph_cathegoryOrigin.clicked.connect(self.on_radiobutton_graph_cathegoryOrigin_clicked)
        
        radiobutton_graph_cathegoryModel =  widget_graphic.findChild(QtWidgets.QRadioButton, "radiobutton_graph_cathegoryModel")
        radiobutton_graph_cathegoryModel.clicked.connect(self.on_radiobutton_graph_cathegoryModel_clicked)
        
        radiobutton_graph_columnOrigin =  widget_graphic.findChild(QtWidgets.QRadioButton, "radiobutton_graph_columnOrigin")
        radiobutton_graph_columnOrigin.clicked.connect(self.on_radiobutton_graph_columnOrigin_clicked)
        
        radiobutton_graph_columnModel =  widget_graphic.findChild(QtWidgets.QRadioButton, "radiobutton_graph_columnModel")
        radiobutton_graph_columnModel.clicked.connect(self.on_radiobutton_graph_columnModel_clicked)
        
        if graph != None:
            if graph.cathegoryType == "MODEL":
                radiobutton_graph_cathegoryModel.setChecked(True)
                radiobutton_graph_cathegoryOrigin.setChecked(False)
            elif graph.cathegoryType == "ORIGIN":
                radiobutton_graph_cathegoryModel.setChecked(False)
                radiobutton_graph_cathegoryOrigin.setChecked(True)
            if graph.columnType == "MODEL":
                radiobutton_graph_columnModel.setChecked(True)
                radiobutton_graph_columnOrigin.setChecked(False)
            elif graph.cathegoryType == "ORIGIN":
                radiobutton_graph_columnModel.setChecked(False)
                radiobutton_graph_columnOrigin.setChecked(True)
                
        
        self.setRadioButtons(widget_graphic)            
                                          
        checkbox_graph_selectAll_Origins = widget_graphic.findChild(QtWidgets.QCheckBox, "checkbox_graph_selectAll_Origins")
        checkbox_graph_selectAll_Origins.setTristate(False)
        checkbox_graph_selectAll_Origins.setChecked(False)
        checkbox_graph_selectAll_Origins.clicked.connect(self.checkbox_graph_selectAll_Origins_CheckChanged)
        
        button_graph_CheckOrigins_byGroup = widget_graphic.findChild(QtWidgets.QPushButton, "button_graph_CheckOrigins_byGroup")
        button_graph_CheckOrigins_byGroup.clicked.connect(self.on_button_graph_CheckOrigins_byGroup_clicked)
        button_graph_CheckOrigins_byGroup.setStyleSheet("background-color: rgba(255, 255, 255, 0)");
                
        checkbox_graph_selectAll_VariablesFormulas = widget_graphic.findChild(QtWidgets.QCheckBox, "checkbox_graph_selectAll_VariablesFormulas")
        checkbox_graph_selectAll_VariablesFormulas.setTristate(False)
        checkbox_graph_selectAll_VariablesFormulas.setChecked(False)
        checkbox_graph_selectAll_VariablesFormulas.clicked.connect(self.checkbox_graph_selectAll_VariablesFormulas_CheckChanged)        
        
        widget_graphic.graph = graph
        
        self.load_listwidget_graph_ModelsAdded(widget_graphic)    
                        
        self.load_listwidget_graph_variables(widget_graphic)
        self.load_listwidget_graph_formulas(widget_graphic)
        
        self.load_graph_origins(widget_graphic)           
         
        self.verticalLayout_graphListWidget.addWidget(widget_graphic)
    
        self.widget_graph_list.append(widget_graphic)        
        
    def checkbox_graph_selectAll_VariablesFormulas_CheckChanged(self):
        widget_graphic = self.sender().parent()
        checkbox_graph_selectAll_VariablesFormulas = widget_graphic.findChild(QtWidgets.QCheckBox, "checkbox_graph_selectAll_VariablesFormulas")
        listwidget_graph_variables = widget_graphic.findChild(QtWidgets.QListWidget, "listwidget_graph_variables")
        for row in range(listwidget_graph_variables.count()):
            item = listwidget_graph_variables.item(row)
            if checkbox_graph_selectAll_VariablesFormulas.isChecked(): 
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)
        listwidget_graph_formulas = widget_graphic.findChild(QtWidgets.QListWidget, "listwidget_graph_formulas")
        for row in range(listwidget_graph_formulas.count()):
            item = listwidget_graph_formulas.item(row)
            if checkbox_graph_selectAll_VariablesFormulas.isChecked(): 
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)
                    
    def listwidget_graph_VariablesFormulas_CheckChanged(self):
        widget_graphic = self.sender().parent()
        checkbox_graph_selectAll_VariablesFormulas = widget_graphic.findChild(QtWidgets.QCheckBox, "checkbox_graph_selectAll_VariablesFormulas")
        listwidget_graph_variables = widget_graphic.findChild(QtWidgets.QListWidget, "listwidget_graph_variables")
        listwidget_graph_formulas = widget_graphic.findChild(QtWidgets.QListWidget, "listwidget_graph_formulas")
        
        itemsVariables = [listwidget_graph_variables.item(row) for row in range(listwidget_graph_variables.count())]
        itemsFormulas = [listwidget_graph_formulas.item(row) for row in range(listwidget_graph_formulas.count())]
    
        if all(item.checkState() == QtCore.Qt.Checked for item in itemsVariables) and all(item.checkState() == QtCore.Qt.Checked for item in itemsFormulas):
            checkbox_graph_selectAll_VariablesFormulas.setTristate(False)
            checkbox_graph_selectAll_VariablesFormulas.setCheckState(QtCore.Qt.Checked)
        elif any(item.checkState() == QtCore.Qt.Checked for item in itemsVariables) or any(item.checkState() == QtCore.Qt.Checked for item in itemsFormulas):
            checkbox_graph_selectAll_VariablesFormulas.setTristate(True)
            checkbox_graph_selectAll_VariablesFormulas.setCheckState(QtCore.Qt.PartiallyChecked)
        else:
            checkbox_graph_selectAll_VariablesFormulas.setTristate(False)
            checkbox_graph_selectAll_VariablesFormulas.setCheckState(QtCore.Qt.Unchecked)   
                 
    def checkbox_graph_selectAll_Origins_CheckChanged(self):
        widget_graphic = self.sender().parent()
        checkbox_graph_selectAll_Origins = widget_graphic.findChild(QtWidgets.QCheckBox, "checkbox_graph_selectAll_Origins")
        listwidget_graph_origins = widget_graphic.findChild(QtWidgets.QListWidget, "listwidget_graph_origins")
        for row in range(listwidget_graph_origins.count()):
            item = listwidget_graph_origins.item(row)
            if checkbox_graph_selectAll_Origins.isChecked():
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)

    def listwidget_graph_origins_CheckChanged(self):
        widget_graphic = self.sender().parent()
        checkbox_graph_selectAll_Origins = widget_graphic.findChild(QtWidgets.QCheckBox, "checkbox_graph_selectAll_Origins")
        listwidget_graph_origins = widget_graphic.findChild(QtWidgets.QListWidget, "listwidget_graph_origins")
        
        items = [listwidget_graph_origins.item(row) for row in range(listwidget_graph_origins.count())]
    
        if all(item.checkState() == QtCore.Qt.Checked for item in items):
            checkbox_graph_selectAll_Origins.setTristate(False)
            checkbox_graph_selectAll_Origins.setCheckState(QtCore.Qt.Checked)
        elif any(item.checkState() == QtCore.Qt.Checked for item in items):
            checkbox_graph_selectAll_Origins.setTristate(True)
            checkbox_graph_selectAll_Origins.setCheckState(QtCore.Qt.PartiallyChecked)
        else:
            checkbox_graph_selectAll_Origins.setTristate(False)
            checkbox_graph_selectAll_Origins.setCheckState(QtCore.Qt.Unchecked)  


    def load_listwidget_graph_ModelsAdded(self, widget_graphic):
        listwidget_graph_ModelsAdded = widget_graphic.findChild(QtWidgets.QListWidget, "listwidget_graph_ModelsAdded")
        listwidget_graph_ModelsAdded.clear()
        for model in self.models:
            item = QtWidgets.QListWidgetItem(model.name, listwidget_graph_ModelsAdded, self.models.index(model))
            item.setData(QtCore.Qt.UserRole, model)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Checked)        
            listwidget_graph_ModelsAdded.addItem(item)    
            
    def load_listwidget_graph_variables(self, widget_graphic):
        combobox_graph_type =  widget_graphic.findChild(QtWidgets.QComboBox, "combobox_graph_type")
        timeseriesType = combobox_graph_type.currentText()
        variables = self.modelsVariables[timeseriesType]
        
        listwidget_graph_variables = widget_graphic.findChild(QtWidgets.QListWidget, "listwidget_graph_variables")
        listwidget_graph_variables.clear()
        variables.sort(key = lambda v: v.id)
        for var in variables:
            ouputUnit = ""
            if var.keyword in self.configUnits[timeseriesType].keys():
                outputUnit = self.configUnits[timeseriesType][var.keyword][0]
            else:                
                outputUnit = var.outputUnit
            item = QtWidgets.QListWidgetItem(var.name + " (" + outputUnit +")", listwidget_graph_variables, var.id)
            item.setData(QtCore.Qt.UserRole, var.keyword)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            if widget_graphic.graph != None and var.keyword in widget_graphic.graph.variables: 
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)        
            listwidget_graph_variables.addItem(item)
        listwidget_graph_variables.clicked.connect(self.listwidget_graph_VariablesFormulas_CheckChanged)     
    
    def load_listwidget_graph_formulas(self, widget_graphic):
        combobox_graph_type =  widget_graphic.findChild(QtWidgets.QComboBox, "combobox_graph_type")
        
        timeseriesType = combobox_graph_type.currentText()
        
        listwidget_graph_formulas = widget_graphic.findChild(QtWidgets.QListWidget, "listwidget_graph_formulas")
        listwidget_graph_formulas.clear()
        formulas = self.loadBasicFormulas(timeseriesType)
        formulas = formulas + self.service.getFormulaList_fromList_byTimeseriesType(self.configFormulas, timeseriesType)
        formulas.sort(key = lambda f: f.name)
        for formula in formulas:
            item = QtWidgets.QListWidgetItem(formula.name, listwidget_graph_formulas, 0)
            formula.expression = formula.expression.replace("[", "")
            formula.expression = formula.expression.replace("]", "")
            item.setData(QtCore.Qt.UserRole, formula)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            if widget_graphic.graph != None and formula.name in [f.name for f in widget_graphic.graph.formulas]: 
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)        
            listwidget_graph_formulas.addItem(item)
        listwidget_graph_formulas.clicked.connect(self.listwidget_graph_VariablesFormulas_CheckChanged)  
    
    def load_graph_origins(self, widget_graphic):
        combobox_graph_type =  widget_graphic.findChild(QtWidgets.QComboBox, "combobox_graph_type")
        combobox_graph_originGroup = widget_graphic.findChild(QtWidgets.QComboBox, "combobox_graph_originGroup")
        
        wells = []
        for model in self.models:
            wells = wells + self.service.getAllGroups(model)
        
        wells = list(set(wells))
        wells.sort()
        combobox_graph_originGroup.clear()
        combobox_graph_originGroup.addItem("TODOS")
        combobox_graph_originGroup.addItems(wells)
        
        self.setup_graph_OriginsWidgets(widget_graphic, combobox_graph_type.currentText())
        self.load_listwidget_graph_origins(widget_graphic)
        
    
    def setup_graph_OriginsWidgets(self, widget_graphic, text):
        label_graph_originGroup = widget_graphic.findChild(QtWidgets.QLabel, "label_graph_originGroup")
        combobox_graph_originGroup = widget_graphic.findChild(QtWidgets.QComboBox, "combobox_graph_originGroup")
        button_graph_CheckOrigins_byGroup = widget_graphic.findChild(QtWidgets.QPushButton, "button_graph_CheckOrigins_byGroup")
        checkbox_graph_selectAll_Origins = widget_graphic.findChild(QtWidgets.QCheckBox, "checkbox_graph_selectAll_Origins")

        if text == "WELLS":
            label_graph_originGroup.setHidden(False)
            combobox_graph_originGroup.setHidden(False)
            button_graph_CheckOrigins_byGroup.setHidden(False)
            
            checkbox_graph_selectAll_Origins.setHidden(True)
            
        else:
            label_graph_originGroup.setHidden(True)
            combobox_graph_originGroup.setHidden(True)
            button_graph_CheckOrigins_byGroup.setHidden(True)
            
            checkbox_graph_selectAll_Origins.setHidden(False)
    
    def load_listwidget_graph_origins(self, widget_graphic):
        combobox_graph_type =  widget_graphic.findChild(QtWidgets.QComboBox, "combobox_graph_type")
                        
        timeseriesType = combobox_graph_type.currentText()
        origins = self.modelsOrigins[timeseriesType]
            
        listwidget_graph_origins = widget_graphic.findChild(QtWidgets.QListWidget, "listwidget_graph_origins")
        listwidget_graph_origins.clear()
        origins.sort(key = lambda o: o.name)
        for origin in origins:
            item = QtWidgets.QListWidgetItem(origin.name, listwidget_graph_origins, origin.id)
            item.setData(QtCore.Qt.UserRole, origin.name)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            if widget_graphic.graph != None and origin.name in widget_graphic.graph.origins:
                item.setCheckState(QtCore.Qt.Checked)        
            else:
                item.setCheckState(QtCore.Qt.Unchecked)        
            listwidget_graph_origins.addItem(item)     
        listwidget_graph_origins.clicked.connect(self.listwidget_graph_origins_CheckChanged)
            
    
    def on_button_graph_CheckOrigins_byGroup_clicked(self):
        widget_graphic = self.sender().parent()        
        
        combobox_graph_originGroup = widget_graphic.findChild(QtWidgets.QComboBox, "combobox_graph_originGroup")
        listwidget_graph_origins = widget_graphic.findChild(QtWidgets.QListWidget, "listwidget_graph_origins")
        
        if combobox_graph_originGroup.currentText() != 'TODOS':
            groups = self.service.getWells_byParent(self.models[0], combobox_graph_originGroup.currentText())
            
            for row in range(listwidget_graph_origins.count()):
                item = listwidget_graph_origins.item(row)
                if item.text() in groups:
                    if item.checkState() == QtCore.Qt.Unchecked:
                        item.setCheckState(QtCore.Qt.Checked)
                    elif item.checkState() == QtCore.Qt.Checked:
                        item.setCheckState(QtCore.Qt.Unchecked)
        else:
            itemOrigins = [listwidget_graph_origins.item(row) for row in range(listwidget_graph_origins.count())]
            if any(item.checkState() == QtCore.Qt.Unchecked for item in itemOrigins):
                for item in itemOrigins:
                    item.setCheckState(QtCore.Qt.Checked)
            else:
                for item in itemOrigins:
                    item.setCheckState(QtCore.Qt.Unchecked)
            
    
    def setRadioButtons(self, widget_graphic):
        radiobutton_graph_cathegoryOrigin =  widget_graphic.findChild(QtWidgets.QRadioButton, "radiobutton_graph_cathegoryOrigin")        
        radiobutton_graph_cathegoryModel =  widget_graphic.findChild(QtWidgets.QRadioButton, "radiobutton_graph_cathegoryModel")
        radiobutton_graph_columnOrigin =  widget_graphic.findChild(QtWidgets.QRadioButton, "radiobutton_graph_columnOrigin")            
        radiobutton_graph_columnModel =  widget_graphic.findChild(QtWidgets.QRadioButton, "radiobutton_graph_columnModel")
          
        if len(self.models) == 1:
            radiobutton_graph_columnOrigin.setChecked(False)
            radiobutton_graph_cathegoryOrigin.setChecked(True)
            
            radiobutton_graph_cathegoryModel.setChecked(False)
            radiobutton_graph_columnModel.setChecked(True)
            radiobutton_graph_cathegoryModel.setEnabled(False)
            radiobutton_graph_cathegoryOrigin.setEnabled(False)
            radiobutton_graph_columnModel.setEnabled(False)
            radiobutton_graph_columnOrigin.setEnabled(False)
        else:
            radiobutton_graph_cathegoryModel.setEnabled(True)
            radiobutton_graph_cathegoryOrigin.setEnabled(True)
            radiobutton_graph_columnModel.setEnabled(True)
            radiobutton_graph_columnOrigin.setEnabled(True)
        
    
    def loadGraphs(self):       
        for widget_graphic in self.widget_graph_list:
            self.load_listwidget_graph_ModelsAdded(widget_graphic)
            self.load_graph_origins(widget_graphic)
            self.load_listwidget_graph_variables(widget_graphic)   
            self.load_listwidget_graph_formulas(widget_graphic)

            self.setRadioButtons(widget_graphic)            
                    
        
    def on_radiobutton_graph_cathegoryModel_clicked(self):         
        widget_graphic = self.sender().parent().parent()
        radiobutton_graph_columnOrigin =  widget_graphic.findChild(QtWidgets.QRadioButton, "radiobutton_graph_columnOrigin")
        radiobutton_graph_columnOrigin.setChecked(True)
        radiobutton_graph_columnModel =  widget_graphic.findChild(QtWidgets.QRadioButton, "radiobutton_graph_columnModel")
        radiobutton_graph_columnModel.setChecked(False)
        
    def on_radiobutton_graph_cathegoryOrigin_clicked(self): 
        widget_graphic = self.sender().parent().parent()
        radiobutton_graph_columnOrigin =  widget_graphic.findChild(QtWidgets.QRadioButton, "radiobutton_graph_columnOrigin")
        radiobutton_graph_columnOrigin.setChecked(False)
        radiobutton_graph_columnModel =  widget_graphic.findChild(QtWidgets.QRadioButton, "radiobutton_graph_columnModel")
        radiobutton_graph_columnModel.setChecked(True)
    
    def on_radiobutton_graph_columnModel_clicked(self): 
        widget_graphic = self.sender().parent().parent()
        radiobutton_graph_cathegoryOrigin =  widget_graphic.findChild(QtWidgets.QRadioButton, "radiobutton_graph_cathegoryOrigin")
        radiobutton_graph_cathegoryOrigin.setChecked(True)
        radiobutton_graph_cathegoryModel =  widget_graphic.findChild(QtWidgets.QRadioButton, "radiobutton_graph_cathegoryModel")
        radiobutton_graph_cathegoryModel.setChecked(False)
    
    def on_radiobutton_graph_columnOrigin_clicked(self): 
        widget_graphic = self.sender().parent().parent()
        radiobutton_graph_cathegoryOrigin =  widget_graphic.findChild(QtWidgets.QRadioButton, "radiobutton_graph_cathegoryOrigin")
        radiobutton_graph_cathegoryOrigin.setChecked(False)
        radiobutton_graph_cathegoryModel =  widget_graphic.findChild(QtWidgets.QRadioButton, "radiobutton_graph_cathegoryModel")
        radiobutton_graph_cathegoryModel.setChecked(True)

    def on_button_SaveGraph_clicked(self): 
        widget_graphic = self.sender().parent().parent()
        
        lineedit_graphName =  widget_graphic.findChild(QtWidgets.QLineEdit, "lineedit_graphName")
        lbl_graphName =  widget_graphic.findChild(QtWidgets.QLabel, "lbl_graphName")
        button_DeleteGraph =  widget_graphic.findChild(QtWidgets.QPushButton, "button_DeleteGraph")
        button_EditGraph =  widget_graphic.findChild(QtWidgets.QPushButton, "button_EditGraph")
        button_SaveGraph =  widget_graphic.findChild(QtWidgets.QPushButton, "button_SaveGraph")
        
        if lineedit_graphName.hasAcceptableInput() == True:
            lbl_graphName.setText(lineedit_graphName.text())            
        else:
            QtWidgets.QToolTip.showText(lineedit_graphName.mapToGlobal(QtCore.QPoint()), "O nome deve conter ao menos uma letra, podendo utilizar números, espaço e underscore.")
            lineedit_graphName.setStyleSheet('QLineEdit { background-color: %s }' % '#f6989d')
            return
                
        lbl_graphName.setHidden(False)                
        lineedit_graphName.setHidden(True)
        button_DeleteGraph.setHidden(False)        
        button_EditGraph.setHidden(False)
        button_SaveGraph.setHidden(True)
                
        widget_graphic.name = lbl_graphName.text()
    
    def lineedit_graphName_textChanged(self):
        widget_graphic = self.sender().parent().parent()
        lineedit_graphName =  widget_graphic.findChild(QtWidgets.QLineEdit, "lineedit_graphName")
        
        if lineedit_graphName.hasAcceptableInput() == False:
            QtWidgets.QToolTip.showText(lineedit_graphName.mapToGlobal(QtCore.QPoint()), "Utilizar letras, números, espaços ou underscore.")
        else:
            lineedit_graphName.setStyleSheet('QLineEdit { background-color: %s }' % '#ffffff')
            QtWidgets.QToolTip.hideText()   
        
    def on_button_DeleteGraph_clicked(self): 
        widget_graphic = self.sender().parent().parent()
        self.widget_graph_list.remove(widget_graphic)
        self.verticalLayout_graphListWidget.removeWidget(widget_graphic)
        sip.delete(widget_graphic)
        widget_graphic = None        
        
    def on_button_EditGraph_clicked(self): 
        widget_graphic = self.sender().parent().parent()
        
        lbl_graphName =  widget_graphic.findChild(QtWidgets.QLabel, "lbl_graphName")
        lbl_graphName.setHidden(True)
        
        button_DeleteGraph =  widget_graphic.findChild(QtWidgets.QPushButton, "button_DeleteGraph")
        button_DeleteGraph.setHidden(True)
        
        button_EditGraph =  widget_graphic.findChild(QtWidgets.QPushButton, "button_EditGraph")
        button_EditGraph.setHidden(True)
                
        lineedit_graphName =  widget_graphic.findChild(QtWidgets.QLineEdit, "lineedit_graphName")
        lineedit_graphName.setHidden(False)
        
        button_SaveGraph =  widget_graphic.findChild(QtWidgets.QPushButton, "button_SaveGraph")
        button_SaveGraph.setHidden(False)
        
        lineedit_graphName.setText(lbl_graphName.text())
    
    def on_combobox_graph_type_currentTextChanged(self, text):                
        widget_graphic = self.sender().parent().parent()
        if widget_graphic != None:
            self.setup_graph_OriginsWidgets(widget_graphic, text)    
            
            self.load_listwidget_graph_variables(widget_graphic)
            self.load_listwidget_graph_formulas(widget_graphic)
            
            self.load_graph_origins(widget_graphic)     
            
                
    @QtCore.pyqtSlot()
    def on_button_NewGraph_clicked(self):
        if self.models != []:
            self.addGraph()
        else:
            value = QMessageBox.warning(None, "Atenção", "Você não adicionou nenhum modelo.")

    @QtCore.pyqtSlot()
    def on_button_ReportGraphs_clicked(self):
        if self.widget_graph_list != []:
            self.verticalLayout.addWidget(self.spinner)
    
            self.centralwidget.setEnabled(False)
            self.spinner.start()   
            self.thread_ReportGraphs.start()    

        else:
            value = QMessageBox.warning(None, "Atenção", "Você não adicionou nenhuma curva.")
        
    def ReportGraphs(self):                
        for i in reversed(range(self.dialog_graphViewer.verticalLayout.count())): 
            self.dialog_graphViewer.verticalLayout.itemAt(i).widget().setParent(None)
        
        wells_origins = []
        wells_variables = []
        groups_origins = []
        groups_variables = []
        sectors_origins = []
        sectors_variables = []    
        
        
        self.graphsToShow = []
        
        for widget_graphic in self.widget_graph_list:
            combobox_graph_type =  widget_graphic.findChild(QtWidgets.QComboBox, "combobox_graph_type")
            lineedit_graphName =  widget_graphic.findChild(QtWidgets.QLineEdit, "lineedit_graphName")
            checkbox_graph_selectAll_Origins = widget_graphic.findChild(QtWidgets.QCheckBox, "checkbox_graph_selectAll_Origins")
            checkbox_graph_selectAll_VariablesFormulas = widget_graphic.findChild(QtWidgets.QCheckBox, "checkbox_graph_selectAll_VariablesFormulas")
            radiobutton_graph_cathegoryOrigin = widget_graphic.findChild(QtWidgets.QRadioButton, "radiobutton_graph_cathegoryOrigin")
            radiobutton_graph_cathegoryModel = widget_graphic.findChild(QtWidgets.QRadioButton, "radiobutton_graph_cathegoryModel")
            radiobutton_graph_columnOrigin = widget_graphic.findChild(QtWidgets.QRadioButton, "radiobutton_graph_columnOrigin")
            radiobutton_graph_columnModel = widget_graphic.findChild(QtWidgets.QRadioButton, "radiobutton_graph_columnModel")
            listwidget_graph_origins = widget_graphic.findChild(QtWidgets.QListWidget, "listwidget_graph_origins")
            listwidget_graph_variables = widget_graphic.findChild(QtWidgets.QListWidget, "listwidget_graph_variables")
            listwidget_graph_formulas = widget_graphic.findChild(QtWidgets.QListWidget, "listwidget_graph_formulas")
            listwidget_graph_ModelsAdded = widget_graphic.findChild(QtWidgets.QListWidget, "listwidget_graph_ModelsAdded")
            
            graph = Model.Graph()
            
            graph.name = lineedit_graphName.text()
            for index in range(listwidget_graph_ModelsAdded.count()):
                    if listwidget_graph_ModelsAdded.item(index).checkState() == QtCore.Qt.Checked:
                        graph.models.append(listwidget_graph_ModelsAdded.item(index).data(QtCore.Qt.UserRole))
                                                
            graph.timeseriesType = combobox_graph_type.currentText()
                
            itemsOrigins = [listwidget_graph_origins.item(row) for row in range(listwidget_graph_origins.count())]
    

            for index in range(listwidget_graph_origins.count()):
                if listwidget_graph_origins.item(index).checkState() == QtCore.Qt.Checked:
                    graph.origins.append(listwidget_graph_origins.item(index).text())
            origin_list = graph.origins
            
            if all(item.checkState() == QtCore.Qt.Checked for item in itemsOrigins):
                origin_list = "ALL"

            for index in range(listwidget_graph_variables.count()):
                if listwidget_graph_variables.item(index).checkState() == QtCore.Qt.Checked: 
                    graph.variables.append(listwidget_graph_variables.item(index).data(QtCore.Qt.UserRole))
            variable_list = graph.variables
            
            if checkbox_graph_selectAll_VariablesFormulas.checkState() == QtCore.Qt.Checked:
                variable_list = "ALL"
                
            for index in range(listwidget_graph_formulas.count()):
                    if listwidget_graph_formulas.item(index).checkState() == QtCore.Qt.Checked:
                        graph.formulas.append(listwidget_graph_formulas.item(index).data(QtCore.Qt.UserRole)) 
            
            if radiobutton_graph_cathegoryModel.isChecked():
                graph.cathegoryType = "MODEL"
            elif radiobutton_graph_cathegoryOrigin.isChecked():
                graph.cathegoryType = "ORIGIN"
            
            if radiobutton_graph_columnModel.isChecked():
                graph.columnType = "MODEL"
            elif radiobutton_graph_columnOrigin.isChecked():
                graph.columnType = "ORIGIN"
                
            
            try:                
                dataframe, units_groups = self.service.loadDataFrame(graph.models, graph.timeseriesType, variable_list, origin_list, graph.formulas, self.configTimestepsParams_graphs, self.configUnits[graph.timeseriesType])   
                dataframe = dataframe[dataframe['OFFSET'] != 0]
                dataframe.drop('OFFSET', axis = 1, inplace = True)
                graph.dataframe = dataframe
                    
                self.graphsToShow.append(graph)
            
            except Exception as e:                
                return str(e.args[-1]) 
                        
        self.currentGraphPage = 0

        return "success"                
                                                        
                                   
    def SaveGraphs(self):
        self.configGraph_list = []
        for widget_graphic in self.widget_graph_list:
            combobox_graph_type =  widget_graphic.findChild(QtWidgets.QComboBox, "combobox_graph_type")
            lineedit_graphName =  widget_graphic.findChild(QtWidgets.QLineEdit, "lineedit_graphName")
            checkbox_graph_selectAll_Origins = widget_graphic.findChild(QtWidgets.QCheckBox, "checkbox_graph_selectAll_Origins")
            checkbox_graph_selectAll_VariablesFormulas = widget_graphic.findChild(QtWidgets.QCheckBox, "checkbox_graph_selectAll_VariablesFormulas")
            radiobutton_graph_cathegoryOrigin = widget_graphic.findChild(QtWidgets.QRadioButton, "radiobutton_graph_cathegoryOrigin")
            radiobutton_graph_cathegoryModel = widget_graphic.findChild(QtWidgets.QRadioButton, "radiobutton_graph_cathegoryModel")
            radiobutton_graph_columnOrigin = widget_graphic.findChild(QtWidgets.QRadioButton, "radiobutton_graph_columnOrigin")
            radiobutton_graph_columnModel = widget_graphic.findChild(QtWidgets.QRadioButton, "radiobutton_graph_columnModel")
            listwidget_graph_origins = widget_graphic.findChild(QtWidgets.QListWidget, "listwidget_graph_origins")
            listwidget_graph_variables = widget_graphic.findChild(QtWidgets.QListWidget, "listwidget_graph_variables")
            listwidget_graph_formulas = widget_graphic.findChild(QtWidgets.QListWidget, "listwidget_graph_formulas")
            listwidget_graph_ModelsAdded = widget_graphic.findChild(QtWidgets.QListWidget, "listwidget_graph_ModelsAdded")
            
            graph = Model.Graph()
            
            graph.name = lineedit_graphName.text()
            for index in range(listwidget_graph_ModelsAdded.count()):
                    if listwidget_graph_ModelsAdded.item(index).checkState() == QtCore.Qt.Checked:
                        graph.models.append(listwidget_graph_ModelsAdded.item(index).data(QtCore.Qt.UserRole))
                                                
            graph.timeseriesType = combobox_graph_type.currentText()
                
            itemsOrigins = [listwidget_graph_origins.item(row) for row in range(listwidget_graph_origins.count())]
    
            for index in range(listwidget_graph_origins.count()):
                if listwidget_graph_origins.item(index).checkState() == QtCore.Qt.Checked:
                    graph.origins.append(listwidget_graph_origins.item(index).text())

            for index in range(listwidget_graph_variables.count()):
                if listwidget_graph_variables.item(index).checkState() == QtCore.Qt.Checked: 
                    graph.variables.append(listwidget_graph_variables.item(index).data(QtCore.Qt.UserRole))
            
            for index in range(listwidget_graph_formulas.count()):
                    if listwidget_graph_formulas.item(index).checkState() == QtCore.Qt.Checked:
                        graph.formulas.append(listwidget_graph_formulas.item(index).data(QtCore.Qt.UserRole)) 
            
            if radiobutton_graph_cathegoryModel.isChecked():
                graph.cathegoryType = "MODEL"
            elif radiobutton_graph_cathegoryOrigin.isChecked():
                graph.cathegoryType = "ORIGIN"
            
            if radiobutton_graph_columnModel.isChecked():
                graph.columnType = "MODEL"
            elif radiobutton_graph_columnOrigin.isChecked():
                graph.columnType = "ORIGIN"
            
            self.configGraph_list.append(graph)
            

    def init_WidgetGraphs(self):
        for graph in self.configGraph_list:
            self.addGraph(graph)
            
    def init_GraphViewer(self):
        self.dialog_graphViewer = QtWidgets.QDialog()
        graphViewer_ui = Ui_dialog_graphViewer()
        graphViewer_ui.setupUi(self.dialog_graphViewer) 
        
        self.dialog_graphViewer.verticalLayout = graphViewer_ui.verticalLayout
        
        self.dialog_graphViewer.button_Next = self.dialog_graphViewer.findChild(QtWidgets.QPushButton, "button_Next")
        self.dialog_graphViewer.button_Next.setStyleSheet("background-color: rgba(255, 255, 255, 0)");
        self.dialog_graphViewer.button_Next.clicked.connect(self.on_button_Next_clicked)
        self.dialog_graphViewer.button_Previous = self.dialog_graphViewer.findChild(QtWidgets.QPushButton, "button_Previous")
        self.dialog_graphViewer.button_Previous.setStyleSheet("background-color: rgba(255, 255, 255, 0)");
        self.dialog_graphViewer.button_Previous.clicked.connect(self.on_button_Previous_clicked)
        
        self.dialog_graphViewer.button_showIterativeGraph = self.dialog_graphViewer.findChild(QtWidgets.QPushButton, "button_showIterativeGraph")
        self.dialog_graphViewer.button_showIterativeGraph.clicked.connect(self.on_button_showIterativeGraph_clicked)
        
    def on_button_Next_clicked(self):
        if self.currentGraphPage < len(self.graphsToShow) - 1:
            self.currentGraphPage = self.currentGraphPage + 1
            self.plotGraph(self.graphsToShow[self.currentGraphPage])
            self.showGraph()
             
    def on_button_Previous_clicked(self):
        if self.currentGraphPage > 0:
            self.currentGraphPage = self.currentGraphPage - 1
            self.plotGraph(self.graphsToShow[self.currentGraphPage])
            self.showGraph()
    
    
    def ReportGraphs_Finished(self, signal):               
        self.centralwidget.setEnabled(True)
        self.spinner.stop()                      
        
        if signal == "success": 
            try:
               self.plotGraph(self.graphsToShow[0])
               self.showGraph()
            
               self.dialog_graphViewer.exec()
           
            except Exception as e:
                value = QMessageBox.warning(None, "Atenção", "Erro ao gerar o gráfico. " + str(e.args[-1]))
        else:
            value = QMessageBox.warning(None, "Atenção", "Erro ao carregar dados para gerar o gráfico: " + signal)
    
        
    def plotGraph(self, graph):                                         
        if graph.cathegoryType == 'MODEL' and graph.columnType == 'ORIGIN':
            self.f, axes = plt.subplots(nrows = 1, ncols = len(graph.origins), squeeze = False)
            coluna = 0
            for origin in graph.origins:
                for var in graph.dataframe.columns:
                    if var not in ['MODEL', 'DATE', 'ORIGIN']:                        
                        sns.lineplot(data = graph.dataframe[graph.dataframe['ORIGIN'] == origin], x = "DATE", y = var, hue = graph.cathegoryType, ax = axes[0, coluna])                        
                coluna = coluna + 1
        elif graph.cathegoryType == 'ORIGIN' and graph.columnType == 'MODEL':
            self.f, axes = plt.subplots(nrows = 1, ncols = len(graph.models), squeeze = False)
            coluna = 0
            for model in graph.models:
                for var in graph.dataframe.columns:
                    if var not in ['MODEL', 'DATE', 'ORIGIN']:                        
                        sns.lineplot(data = graph.dataframe[graph.dataframe['MODEL'] == model.name], x = "DATE", y = var, hue = graph.cathegoryType, ax = axes[0, coluna])
                coluna = coluna + 1
                        
        if graph.html == "":
            coluna = 1
            if graph.cathegoryType == 'MODEL' and graph.columnType == 'ORIGIN':
                fig = make_subplots(rows = 1, cols = len(graph.origins))                
                for origin in graph.origins:
                    for model, df in graph.dataframe.groupby('MODEL'):
                        for var in graph.dataframe.columns:
                            if var not in ['MODEL', 'DATE', 'ORIGIN']:
                                fig.add_trace(go.Scatter(x = df[df['ORIGIN'] == origin]['DATE'], y = df[df['ORIGIN'] == origin][var], name = model, mode = 'lines'), row = 1, col = coluna)
                    coluna = coluna + 1
            elif graph.cathegoryType == 'ORIGIN' and graph.columnType == 'MODEL':
                fig = make_subplots(rows = 1, cols = len(graph.models))
                for model in graph.models:
                    for origin, df in graph.dataframe.groupby('ORIGIN'):
                        for var in graph.dataframe.columns:
                            if var not in ['MODEL', 'DATE', 'ORIGIN']:
                                fig.add_trace(go.Scatter(x = df[df['MODEL'] == model.name]['DATE'], y = df[df['MODEL'] == model.name][var], name = origin, mode = 'lines'), row = 1, col = coluna)
                    coluna = coluna + 1
                                    
            graph.html = '<html><head><meta charset="utf-8" />'
            graph.html += '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script></head>'
            graph.html += '<body></body>'
            graph.html += po.plot(fig, include_plotlyjs=False, output_type='div')                                         
                            
            functionResize = """var resizeDebounce = null;
                                var graph = document.querySelector('div[class^="plotly-graph"');

                                function resizePlot() {
                                    var bb = graph.getBoundingClientRect();
                                    Plotly.relayout(graph, { width: bb.width, height: bb.height });
                                    }

                                window.addEventListener("resize", function () {
                                    if (resizeDebounce) {
                                            window.clearTimeout(resizeDebounce);
                                        }
                                    resizeDebounce = window.setTimeout(resizePlot, 100);
                                    });        
                            resizePlot();"""
            graph.html += '<script>' + functionResize + '</script>'
        
    def on_button_showIterativeGraph_clicked(self):
        graph = self.graphsToShow[self.currentGraphPage]
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
            url = 'file://' + f.name
            f.write(graph.html)
    
        webbrowser.open(url)   
    
    def showGraph(self):
        for i in reversed(range(self.dialog_graphViewer.verticalLayout.count())): 
            self.dialog_graphViewer.verticalLayout.itemAt(i).widget().setParent(None)

        self.canvas = FigureCanvas(self.f)                
          
        if self.currentGraphPage == len(self.graphsToShow) - 1:
            self.dialog_graphViewer.button_Next.setEnabled(False)
        else:
            self.dialog_graphViewer.button_Next.setEnabled(True)
            
        if self.currentGraphPage == 0:
            self.dialog_graphViewer.button_Previous.setEnabled(False)
        else:
            self.dialog_graphViewer.button_Previous.setEnabled(True)
        
        self.dialog_graphViewer.verticalLayout.addWidget(self.canvas)
        

# ----------------------------------------------------- JANELA PRINCIPAL: FIM DA ABA CURVAS
        
        
# ----------------------------------------------------- JANELA PRINCIPAL: INÍCIO DA ABA TABELAS

    def init_WidgetSets(self):
        for tableSet in self.configSet_list:
            self.addSet(tableSet)
    
    def addSet(self, tableSet = None):        
        widget_set = QtWidgets.QWidget()
        tableEditor_ui = Ui_widget_setEditor()
        tableEditor_ui.setupUi(widget_set)

        countSets = len(self.widget_set_list)
        widget_set.index = countSets      
                
        countSets = countSets + 1        
        
        lbl_setHeader =  widget_set.findChild(QtWidgets.QLabel, "lbl_setHeader")  
        lbl_set_typeHeader =  widget_set.findChild(QtWidgets.QLabel, "lbl_set_typeHeader")
        lbl_set_originsHeader =  widget_set.findChild(QtWidgets.QLabel, "lbl_set_originsHeader")
        lbl_set_variablesHeader =  widget_set.findChild(QtWidgets.QLabel, "lbl_set_variablesHeader")
        
        if(countSets != 1):
            lbl_setHeader.setVisible(False)
            lbl_set_typeHeader.setVisible(False)
            lbl_set_originsHeader.setVisible(False)
            lbl_set_variablesHeader.setVisible(False)
        
        lbl_setName =  widget_set.findChild(QtWidgets.QLabel, "lbl_setName")
        if tableSet == None:
            lbl_setName.setText("CONJUNTO " + str(countSets))
        else:
            lbl_setName.setText(tableSet.name)
        widget_set.name = lbl_setName.text()
        lbl_setName.setHidden(False)
        
        button_DeleteSet =  widget_set.findChild(QtWidgets.QPushButton, "button_DeleteSet")
        button_DeleteSet.setHidden(False)
        button_DeleteSet.clicked.connect(self.on_button_DeleteSet_clicked)
        
        button_EditSet =  widget_set.findChild(QtWidgets.QPushButton, "button_EditSet")
        button_EditSet.setHidden(False)
        button_EditSet.clicked.connect(self.on_button_EditSet_clicked)        
        
        lineedit_setName =  widget_set.findChild(QtWidgets.QLineEdit, "lineedit_setName")
        lineedit_setName.setHidden(True)
        validador = QtCore.QRegExp("[a-zA-Z0-9()_ -]+")
        lineedit_setName.setValidator(QtGui.QRegExpValidator(validador, self))
        lineedit_setName.textChanged.connect(self.lineedit_setName_textChanged)
                
        button_SaveSet =  widget_set.findChild(QtWidgets.QPushButton, "button_SaveSet")
        button_SaveSet.setHidden(True)   
        button_SaveSet.clicked.connect(self.on_button_SaveSet_clicked)
        
        combobox_set_type =  widget_set.findChild(QtWidgets.QComboBox, "combobox_set_type")
        combobox_set_type.currentTextChanged.connect(self.on_combobox_set_type_currentTextChanged)              
        if tableSet != None:
            index = combobox_set_type.findText(tableSet.timeseriesType, QtCore.Qt.MatchFixedString)
            if index >= 0:
                combobox_set_type.setCurrentIndex(index) 
                  
        checkbox_set_selectAll_Origins = widget_set.findChild(QtWidgets.QCheckBox, "checkbox_set_selectAll_Origins")
        checkbox_set_selectAll_Origins.setTristate(False)
        checkbox_set_selectAll_Origins.setChecked(False)
        checkbox_set_selectAll_Origins.clicked.connect(self.checkbox_set_selectAll_Origins_CheckChanged)
                
        checkbox_set_selectAll_VariablesFormulas = widget_set.findChild(QtWidgets.QCheckBox, "checkbox_set_selectAll_VariablesFormulas")
        checkbox_set_selectAll_VariablesFormulas.setTristate(False)
        checkbox_set_selectAll_VariablesFormulas.setChecked(False)
        checkbox_set_selectAll_VariablesFormulas.clicked.connect(self.checkbox_set_selectAll_VariablesFormulas_CheckChanged)        
        
        
        button_set_CheckOrigins_byGroup = widget_set.findChild(QtWidgets.QPushButton, "button_set_CheckOrigins_byGroup")
        button_set_CheckOrigins_byGroup.clicked.connect(self.on_button_set_CheckOrigins_byGroup_clicked)
        button_set_CheckOrigins_byGroup.setStyleSheet("background-color: rgba(255, 255, 255, 0)");
        
        widget_set.tableSet = tableSet
        
        self.load_listwidget_set_ModelsAdded(widget_set)    
                
        self.load_listwidget_set_variables(widget_set)
        self.load_listwidget_set_formulas(widget_set)
        
        self.load_set_origins(widget_set)
         
        self.verticalLayout_setListWidget.addWidget(widget_set)
        self.widget_set_list.append(widget_set)        
        
    def SaveSets(self):
        self.configSet_list = []
        for widget_set in self.widget_set_list:
            combobox_set_type =  widget_set.findChild(QtWidgets.QComboBox, "combobox_set_type")
            lineedit_setName =  widget_set.findChild(QtWidgets.QLineEdit, "lineedit_setName")
            checkbox_set_selectAll_Origins = widget_set.findChild(QtWidgets.QCheckBox, "checkbox_set_selectAll_Origins")
            checkbox_set_selectAll_VariablesFormulas = widget_set.findChild(QtWidgets.QCheckBox, "checkbox_set_selectAll_VariablesFormulas")
            listwidget_set_origins = widget_set.findChild(QtWidgets.QListWidget, "listwidget_set_origins")
            listwidget_set_variables = widget_set.findChild(QtWidgets.QListWidget, "listwidget_set_variables")
            listwidget_set_formulas = widget_set.findChild(QtWidgets.QListWidget, "listwidget_set_formulas")
            listwidget_set_ModelsAdded = widget_set.findChild(QtWidgets.QListWidget, "listwidget_set_ModelsAdded")
            
            tableSet = Model.Set()
            
            tableSet.name = lineedit_setName.text()
            for index in range(listwidget_set_ModelsAdded.count()):
                    if listwidget_set_ModelsAdded.item(index).checkState() == QtCore.Qt.Checked:
                        tableSet.models.append(listwidget_set_ModelsAdded.item(index).data(QtCore.Qt.UserRole))
                                                
            tableSet.timeseriesType = combobox_set_type.currentText()
                
            itemsOrigins = [listwidget_set_origins.item(row) for row in range(listwidget_set_origins.count())]
    
            for index in range(listwidget_set_origins.count()):
                if listwidget_set_origins.item(index).checkState() == QtCore.Qt.Checked:
                    tableSet.origins.append(listwidget_set_origins.item(index).text())

            for index in range(listwidget_set_variables.count()):
                if listwidget_set_variables.item(index).checkState() == QtCore.Qt.Checked: 
                    tableSet.variables.append(listwidget_set_variables.item(index).data(QtCore.Qt.UserRole))
            
            for index in range(listwidget_set_formulas.count()):
                    if listwidget_set_formulas.item(index).checkState() == QtCore.Qt.Checked:
                        tableSet.formulas.append(listwidget_set_formulas.item(index).data(QtCore.Qt.UserRole)) 
            
            self.configSet_list.append(tableSet)

    def checkbox_set_selectAll_VariablesFormulas_CheckChanged(self):
        widget_set = self.sender().parent()
        checkbox_set_selectAll_VariablesFormulas = widget_set.findChild(QtWidgets.QCheckBox, "checkbox_set_selectAll_VariablesFormulas")
        listwidget_set_variables = widget_set.findChild(QtWidgets.QListWidget, "listwidget_set_variables")
        for row in range(listwidget_set_variables.count()):
            item = listwidget_set_variables.item(row)
            if checkbox_set_selectAll_VariablesFormulas.isChecked(): 
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)
        listwidget_set_formulas = widget_set.findChild(QtWidgets.QListWidget, "listwidget_set_formulas")
        for row in range(listwidget_set_formulas.count()):
            item = listwidget_set_formulas.item(row)
            if checkbox_set_selectAll_VariablesFormulas.isChecked(): 
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)
                    
    def listwidget_set_VariablesFormulas_CheckChanged(self):
        widget_set = self.sender().parent()
        checkbox_set_selectAll_VariablesFormulas = widget_set.findChild(QtWidgets.QCheckBox, "checkbox_set_selectAll_VariablesFormulas")
        listwidget_set_variables = widget_set.findChild(QtWidgets.QListWidget, "listwidget_set_variables")
        listwidget_set_formulas = widget_set.findChild(QtWidgets.QListWidget, "listwidget_set_formulas")
        
        itemsVariables = [listwidget_set_variables.item(row) for row in range(listwidget_set_variables.count())]
        itemsFormulas = [listwidget_set_formulas.item(row) for row in range(listwidget_set_formulas.count())]
    
        if all(item.checkState() == QtCore.Qt.Checked for item in itemsVariables) and all(item.checkState() == QtCore.Qt.Checked for item in itemsFormulas):
            checkbox_set_selectAll_VariablesFormulas.setTristate(False)
            checkbox_set_selectAll_VariablesFormulas.setCheckState(QtCore.Qt.Checked)
        elif any(item.checkState() == QtCore.Qt.Checked for item in itemsVariables) or any(item.checkState() == QtCore.Qt.Checked for item in itemsFormulas):
            checkbox_set_selectAll_VariablesFormulas.setTristate(True)
            checkbox_set_selectAll_VariablesFormulas.setCheckState(QtCore.Qt.PartiallyChecked)
        else:
            checkbox_set_selectAll_VariablesFormulas.setTristate(False)
            checkbox_set_selectAll_VariablesFormulas.setCheckState(QtCore.Qt.Unchecked)    
                 
    def checkbox_set_selectAll_Origins_CheckChanged(self):
        widget_set = self.sender().parent()
        checkbox_set_selectAll_Origins = widget_set.findChild(QtWidgets.QCheckBox, "checkbox_set_selectAll_Origins")
        listwidget_set_origins = widget_set.findChild(QtWidgets.QListWidget, "listwidget_set_origins")
        for row in range(listwidget_set_origins.count()):
            item = listwidget_set_origins.item(row)
            if checkbox_set_selectAll_Origins.isChecked():
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)

    def listwidget_set_origins_CheckChanged(self):
        widget_set = self.sender().parent()
        checkbox_set_selectAll_Origins = widget_set.findChild(QtWidgets.QCheckBox, "checkbox_set_selectAll_Origins")
        listwidget_set_origins = widget_set.findChild(QtWidgets.QListWidget, "listwidget_set_origins")
        
        items = [listwidget_set_origins.item(row) for row in range(listwidget_set_origins.count())]
    
        if all(item.checkState() == QtCore.Qt.Checked for item in items):
            checkbox_set_selectAll_Origins.setTristate(False)
            checkbox_set_selectAll_Origins.setCheckState(QtCore.Qt.Checked)
        elif any(item.checkState() == QtCore.Qt.Checked for item in items):
            checkbox_set_selectAll_Origins.setTristate(True)
            checkbox_set_selectAll_Origins.setCheckState(QtCore.Qt.PartiallyChecked)
        else:
            checkbox_set_selectAll_Origins.setTristate(False)
            checkbox_set_selectAll_Origins.setCheckState(QtCore.Qt.Unchecked)  


    def load_listwidget_set_ModelsAdded(self, widget_set):
        listwidget_set_ModelsAdded = widget_set.findChild(QtWidgets.QListWidget, "listwidget_set_ModelsAdded")
        listwidget_set_ModelsAdded.clear()
        for model in self.models:
            item = QtWidgets.QListWidgetItem(model.name, listwidget_set_ModelsAdded, self.models.index(model))
            item.setData(QtCore.Qt.UserRole, model)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Checked)        
            listwidget_set_ModelsAdded.addItem(item)    
            
    def load_listwidget_set_variables(self, widget_set):
        combobox_set_type =  widget_set.findChild(QtWidgets.QComboBox, "combobox_set_type")
        
        timeseriesType = combobox_set_type.currentText()
        variables = self.modelsVariables[timeseriesType]
        
        listwidget_set_variables = widget_set.findChild(QtWidgets.QListWidget, "listwidget_set_variables")
        listwidget_set_variables.clear()
        variables.sort(key = lambda v: v.id)
        for var in variables:                                   
            ouputUnit = ""
            if var.keyword in self.configUnits[timeseriesType].keys():
                outputUnit = self.configUnits[timeseriesType][var.keyword][0]
            else:                
                outputUnit = var.outputUnit    
            item = QtWidgets.QListWidgetItem(var.name + " (" + outputUnit + ")", listwidget_set_variables, var.id)
            item.setData(QtCore.Qt.UserRole, var.keyword)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            if widget_set.tableSet != None and var.keyword in widget_set.tableSet.variables: 
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)         
            listwidget_set_variables.addItem(item)
        listwidget_set_variables.clicked.connect(self.listwidget_set_VariablesFormulas_CheckChanged)     
        
    def load_listwidget_set_formulas(self, widget_set):
        combobox_set_type =  widget_set.findChild(QtWidgets.QComboBox, "combobox_set_type")
        
        timeseriesType = combobox_set_type.currentText()
        
        listwidget_set_formulas = widget_set.findChild(QtWidgets.QListWidget, "listwidget_set_formulas")
        listwidget_set_formulas.clear()
        formulas = self.loadBasicFormulas(timeseriesType)         
        formulas = formulas + self.service.getFormulaList_fromList_byTimeseriesType(self.configFormulas, timeseriesType)
        formulas.sort(key = lambda f: f.name)
        for formula in formulas:
            item = QtWidgets.QListWidgetItem(formula.name, listwidget_set_formulas, 0)
            formula.expression = formula.expression.replace("[", "")
            formula.expression = formula.expression.replace("]", "")
            item.setData(QtCore.Qt.UserRole, formula)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            if widget_set.tableSet != None and formula.name in [f.name for f in widget_set.tableSet.formulas]: 
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)         
            listwidget_set_formulas.addItem(item)
        listwidget_set_formulas.clicked.connect(self.listwidget_set_VariablesFormulas_CheckChanged)           
    
    
    def load_set_origins(self, widget_set):
        combobox_set_type =  widget_set.findChild(QtWidgets.QComboBox, "combobox_set_type")
        combobox_set_originGroup = widget_set.findChild(QtWidgets.QComboBox, "combobox_set_originGroup")
        
        wells = []
        for model in self.models:
            wells = wells + self.service.getAllGroups(model)
        
        wells = list(set(wells))
        wells.sort()
        combobox_set_originGroup.clear()
        combobox_set_originGroup.addItem("TODOS")
        combobox_set_originGroup.addItems(wells)
        
        self.setup_set_OriginsWidgets(widget_set, combobox_set_type.currentText())
        self.load_listwidget_set_origins(widget_set)
        
    
    def setup_set_OriginsWidgets(self, widget_set, text):
        label_set_originGroup = widget_set.findChild(QtWidgets.QLabel, "label_set_originGroup")
        combobox_set_originGroup = widget_set.findChild(QtWidgets.QComboBox, "combobox_set_originGroup")
        button_set_CheckOrigins_byGroup = widget_set.findChild(QtWidgets.QPushButton, "button_set_CheckOrigins_byGroup")
        checkbox_set_selectAll_Origins = widget_set.findChild(QtWidgets.QCheckBox, "checkbox_set_selectAll_Origins")

        if text == "WELLS":
            label_set_originGroup.setHidden(False)
            combobox_set_originGroup.setHidden(False)
            button_set_CheckOrigins_byGroup.setHidden(False)
            
            checkbox_set_selectAll_Origins.setHidden(True)
            
        else:
            label_set_originGroup.setHidden(True)
            combobox_set_originGroup.setHidden(True)
            button_set_CheckOrigins_byGroup.setHidden(True)
            
            checkbox_set_selectAll_Origins.setHidden(False)
    
    def load_listwidget_set_origins(self, widget_set):
        combobox_set_type =  widget_set.findChild(QtWidgets.QComboBox, "combobox_set_type")
        
        timeseriesType = combobox_set_type.currentText()
        origins = self.modelsOrigins[timeseriesType]
            
        listwidget_set_origins = widget_set.findChild(QtWidgets.QListWidget, "listwidget_set_origins")
        listwidget_set_origins.clear()
        origins.sort(key = lambda o: o.name)
        for origin in origins:
            item = QtWidgets.QListWidgetItem(origin.name, listwidget_set_origins, origin.id)
            item.setData(QtCore.Qt.UserRole, origin.name)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            if widget_set.tableSet != None and origin.name in widget_set.tableSet.origins: 
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)        
            listwidget_set_origins.addItem(item)     
        listwidget_set_origins.clicked.connect(self.listwidget_set_origins_CheckChanged) 
            
    
    def on_button_set_CheckOrigins_byGroup_clicked(self):
        widget_set = self.sender().parent()
        
        combobox_set_originGroup = widget_set.findChild(QtWidgets.QComboBox, "combobox_set_originGroup")
        listwidget_set_origins = widget_set.findChild(QtWidgets.QListWidget, "listwidget_set_origins")
        
        if combobox_set_originGroup.currentText() != 'TODOS':
            groups = self.service.getWells_byParent(self.models[0], combobox_set_originGroup.currentText())
            
            for row in range(listwidget_set_origins.count()):
                item = listwidget_set_origins.item(row)
                if item.text() in groups:
                    if item.checkState() == QtCore.Qt.Unchecked:
                        item.setCheckState(QtCore.Qt.Checked)
                    elif item.checkState() == QtCore.Qt.Checked:
                        item.setCheckState(QtCore.Qt.Unchecked)
        else:
            itemOrigins = [listwidget_set_origins.item(row) for row in range(listwidget_set_origins.count())]
            if any(item.checkState() == QtCore.Qt.Unchecked for item in itemOrigins):
                for item in itemOrigins:
                    item.setCheckState(QtCore.Qt.Checked)
            else:
                for item in itemOrigins:
                    item.setCheckState(QtCore.Qt.Unchecked)       
    
    def loadSets(self):        
        for widget_set in self.widget_set_list:
            self.load_listwidget_set_ModelsAdded(widget_set)
            self.load_listwidget_set_origins(widget_set)
            self.load_listwidget_set_variables(widget_set)   
            self.load_listwidget_set_formulas(widget_set)

    def on_button_SaveSet_clicked(self): 
        widget_set = self.sender().parent().parent()
        
        lbl_setName =  widget_set.findChild(QtWidgets.QLabel, "lbl_setName")
        button_DeleteSet =  widget_set.findChild(QtWidgets.QPushButton, "button_DeleteSet")
        button_EditSet =  widget_set.findChild(QtWidgets.QPushButton, "button_EditSet")
        lineedit_setName =  widget_set.findChild(QtWidgets.QLineEdit, "lineedit_setName")
        button_SaveSet =  widget_set.findChild(QtWidgets.QPushButton, "button_SaveSet")
        
        if lineedit_setName.hasAcceptableInput() == True:
            lbl_setName.setText(lineedit_setName.text())
        else:
            QtWidgets.QToolTip.showText(lineedit_setName.mapToGlobal(QtCore.QPoint()), "Utilizar letras, números, espaços ou underscore.")
            lineedit_setName.setStyleSheet('QLineEdit { background-color: %s }' % '#f6989d')
            return
                
        lbl_setName.setHidden(False)        
        button_DeleteSet.setHidden(False)        
        button_EditSet.setHidden(False)        
        lineedit_setName.setHidden(True)                
        button_SaveSet.setHidden(True)
        
        
        widget_set.name = lbl_setName.text()
    
    def lineedit_setName_textChanged(self):
        widget_set = self.sender().parent().parent()
        lineedit_setName =  widget_set.findChild(QtWidgets.QLineEdit, "lineedit_setName")
        if lineedit_setName.hasAcceptableInput() == False:
            QtWidgets.QToolTip.showText(lineedit_setName.mapToGlobal(QtCore.QPoint()), "O nome deve conter ao menos uma letra, podendo utilizar números e underscore.")
        else:
            lineedit_setName.setStyleSheet('QLineEdit { background-color: %s }' % '#ffffff')
            QtWidgets.QToolTip.hideText()     
    
    def on_button_DeleteSet_clicked(self): 
        widget_set = self.sender().parent().parent()
        self.widget_set_list.remove(widget_set)
        self.verticalLayout_setListWidget.removeWidget(widget_set)
        sip.delete(widget_set)
        widget_set = None        
        
    def on_button_EditSet_clicked(self): 
        widget_set = self.sender().parent().parent()
        
        lbl_setName =  widget_set.findChild(QtWidgets.QLabel, "lbl_setName")
        lbl_setName.setHidden(True)
        
        button_DeleteSet =  widget_set.findChild(QtWidgets.QPushButton, "button_DeleteSet")
        button_DeleteSet.setHidden(True)
        
        button_EditSet =  widget_set.findChild(QtWidgets.QPushButton, "button_EditSet")
        button_EditSet.setHidden(True)
                
        lineedit_setName =  widget_set.findChild(QtWidgets.QLineEdit, "lineedit_setName")
        lineedit_setName.setHidden(False)
        
        button_SaveSet =  widget_set.findChild(QtWidgets.QPushButton, "button_SaveSet")
        button_SaveSet.setHidden(False)
        
        lineedit_setName.setText(lbl_setName.text())
    
    def on_combobox_set_type_currentTextChanged(self, text):                
        widget_set = self.sender().parent().parent()
        
        if widget_set != None:
            self.setup_set_OriginsWidgets(widget_set, text)
                
            self.load_listwidget_set_variables(widget_set)
            self.load_listwidget_set_formulas(widget_set)
            self.load_listwidget_set_origins(widget_set)    
                        
    @QtCore.pyqtSlot()
    def on_button_NewSet_clicked(self):
        if self.models != []:
            self.addSet()
        else:
            value = QMessageBox.warning(None, "Atenção", "Você não adicionou nenhum modelo.")
       

    @QtCore.pyqtSlot()
    def on_button_prepareTable_clicked(self):        
        if self.widget_set_list != []:
            self.verticalLayout.addWidget(self.spinner)
            self.spinner.start()
            self.centralwidget.setEnabled(False)             
            self.thread_PrepareTable.start()
        else:
            value = QMessageBox.warning(None, "Atenção", "Você não adicionou nenhum dado à tabela.")
            
    def PrepareTable(self):        
        start_time = time.time()         
        try:
            df_list = [] 
            units_dict_list = {}
            units_dict_list['WELLS'] = {}
            units_dict_list['GROUPS'] = {}
            units_dict_list['SECTORS'] = {}
            
                   
            for widget_set in self.widget_set_list:
                combobox_set_type =  widget_set.findChild(QtWidgets.QComboBox, "combobox_set_type")
                listwidget_set_origins = widget_set.findChild(QtWidgets.QListWidget, "listwidget_set_origins")
                listwidget_set_variables = widget_set.findChild(QtWidgets.QListWidget, "listwidget_set_variables")
                listwidget_set_formulas = widget_set.findChild(QtWidgets.QListWidget, "listwidget_set_formulas")
                listwidget_set_ModelsAdded = widget_set.findChild(QtWidgets.QListWidget, "listwidget_set_ModelsAdded")
                checkbox_set_selectAll_VariablesFormulas = widget_set.findChild(QtWidgets.QCheckBox, "checkbox_set_selectAll_VariablesFormulas")
                checkbox_set_selectAll_Origins = widget_set.findChild(QtWidgets.QCheckBox, "checkbox_set_selectAll_Origins")
                
                models = []
                timeseriesType = ""
                variables_list = []
                origins_list = []
                formulas = []
                
                for index in range(listwidget_set_ModelsAdded.count()):
                    if listwidget_set_ModelsAdded.item(index).checkState() == QtCore.Qt.Checked:
                        models.append(listwidget_set_ModelsAdded.item(index).data(QtCore.Qt.UserRole))
                
                timeseriesType = combobox_set_type.currentText()
                
                itemsOrigins = [listwidget_set_origins.item(row) for row in range(listwidget_set_origins.count())]
    
                if all(item.checkState() == QtCore.Qt.Checked for item in itemsOrigins):
                    origins_list = "ALL"
                else:
                    for index in range(listwidget_set_origins.count()):
                        if listwidget_set_origins.item(index).checkState() == QtCore.Qt.Checked:
                            origins_list.append(listwidget_set_origins.item(index).text())
                
                
                if checkbox_set_selectAll_VariablesFormulas.checkState() == QtCore.Qt.Checked:
                    variables_list = "ALL"
                else:
                    for index in range(listwidget_set_variables.count()):
                        if listwidget_set_variables.item(index).checkState() == QtCore.Qt.Checked:
                            variables_list.append(listwidget_set_variables.item(index).data(QtCore.Qt.UserRole))
                
                
                for index in range(listwidget_set_formulas.count()):
                        if listwidget_set_formulas.item(index).checkState() == QtCore.Qt.Checked:
                            formulas.append(listwidget_set_formulas.item(index).data(QtCore.Qt.UserRole))                                
                                                    
                start_time_inside = time.time()
                            
                df, units = self.service.loadDataFrame(models, timeseriesType, variables_list, origins_list, formulas, self.configTimestepsParams_sets, self.configUnits[timeseriesType])
                
                print("IMPORTAR CONJUNTO DE DADOS = DATAFRAME: %s seconds ---" % (time.time() - start_time_inside)) 
           
                df_list.append(df)
                
                for u_var, u_unit in units.items():
                    if u_var not in units_dict_list[timeseriesType].keys():
                        units_dict_list[timeseriesType].update({u_var: u_unit})                    
            
            df_final = pd.concat(df_list, axis = 0)
            df_final = df_final[df_final['OFFSET'] != 0]
            df_final.drop('OFFSET', axis = 1, inplace = True)
            
            
            df_final = self.service.orderDataFrame_byColumns(df_final, self.configColumnsOrder.keys())        
                       
            self.df_forTable = df_final
            self.units_forTable = units_dict_list
                
            variables = self.modelsVariables[timeseriesType]
            listwidget_tableHeaders = self.listwidget_tableHeaders
            listwidget_tableHeaders.clear()
            for col in df_final.columns:
                if col in self.configColumnsOrder.keys():
                    item = QtWidgets.QListWidgetItem(self.configColumnsOrder[col], listwidget_tableHeaders, 0)
                else:
                    found = False
                    for var in variables:
                        if var.keyword in self.configUnits[timeseriesType].keys():
                            outputUnit = self.configUnits[timeseriesType][var.keyword][0]
                        else:                
                            outputUnit = var.outputUnit
                        if var.keyword == col and outputUnit is not None:
                            item = QtWidgets.QListWidgetItem(col + " (" + outputUnit + ")", listwidget_tableHeaders, 0)
                            found = True
                            break       
                    if not(found):
                        item = QtWidgets.QListWidgetItem(col, listwidget_tableHeaders, 0)
                item.setData(QtCore.Qt.UserRole, col)
                item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)      
                listwidget_tableHeaders.addItem(item)
                
            listwidget_tableHeaders.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            listwidget_tableHeaders.customContextMenuRequested.connect(self.listwidget_tableHeaders_rightClick)
                
            listwidget_tableHeaders.setStyleSheet("QListWidget::item { "
                                                      "border-style: solid;" 
                                                      "border-width: 1px;" 
                                                      "border-color: black;}"                                                   
                                                  "QListWidget::item:selected {"
                                                      "border-style: solid;" 
                                                      "border-width: 1px;" 
                                                      "border-color: black;" 
                                                      "color: black; }")
    
            self.button_ReportSets.setVisible(True)
            self.scrollarea_TableHeaders.setVisible(True)
            listwidget_tableHeaders.setVisible(True)
            return "success"
    
        except Exception as e:            
            return str(e.args[-1])
 
    def PrepareTable_Finished(self, signal):        
        self.centralwidget.setEnabled(True)
        self.spinner.stop()
        if signal != "success":
            value = QMessageBox.warning(None, "Atenção", "Erro ao preparar a tabela: " + signal)
            
        
    def listwidget_tableHeaders_rightClick(self, QPos):
        self.listMenu= QtWidgets.QMenu()
        menu_item = self.listMenu.addAction("Excluir")
        menu_item.triggered.connect(self.listwidget_tableHeaders_rightClick_delete) 
        parentPosition = self.listwidget_tableHeaders.mapToGlobal(QtCore.QPoint(0, 0))        
        self.listMenu.move(parentPosition + QPos)
        self.listMenu.show()
    
    def listwidget_tableHeaders_rightClick_delete(self):
        self.listwidget_tableHeaders.takeItem(self.listwidget_tableHeaders.currentRow())
    
    
    @QtCore.pyqtSlot()
    def on_button_ReportSets_clicked(self):
        self.excelTable_output = QFileDialog.getSaveFileName(None, 'Salvar arquivo', 'TABELA.xlsx', 'EXCEL(*.xlsx)')[0]
        if self.excelTable_output:             
            if self.widget_set_list != []:
                self.verticalLayout.addWidget(self.spinner) 
                self.spinner.start()
                self.centralwidget.setEnabled(False)     
                self.thread_Export_toExcel.start()
            else:
                value = QMessageBox.warning(None, "Atenção", "Você não adicionou nenhum dado à tabela.")                                   
            

    def Export_toExcel(self):
        try:
            start_time_excel = time.time()      
            columns = {}
            listwidget_tableHeaders = self.listwidget_tableHeaders
            for index in range(listwidget_tableHeaders.count()):
                original_name = listwidget_tableHeaders.item(index).data(QtCore.Qt.UserRole)
                new_name = listwidget_tableHeaders.item(index).text()      
                columns.update({original_name: new_name})
            
            df_final = self.service.prepareFinalDataFrame(self.df_forTable, columns, self.units_forTable)
            self.service.exportDataFrame_toExcel(df_final, output = self.excelTable_output) 
            
            print("GERAR EXCEL: %s seconds ---" % (time.time() - start_time_excel))   
            return "success"                    
        except Exception as e:                
            return str(e.args[-1])
    
    def Export_toExcel_Finished(self, signal):           
        self.centralwidget.setEnabled(True)
        self.spinner.stop()    
        if signal == "success":
            value = QMessageBox.information(None, "Concluído", "Arquivo " + str(self.excelTable_output.split("/")[-1]) + " salvo com sucesso.")                
        elif signal == "fail":
            value = QMessageBox.information(None, "Atenção", "Erro ao exportar para excel:" + signal)                


# ----------------------------------------------------- JANELA PRINCIPAL: FIM DA ABA TABELAS

def main():
    """Main app function."""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    window = ResReporter()    
    window.show()
    exit(app.exec_())

if __name__ == '__main__':
    main()  
    

