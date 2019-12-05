from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QTextCursor, QRegExpValidator, QValidator

class LineEdit_DateMask(QtWidgets.QLineEdit):
    def __init__( self, *args):
        QtWidgets.QLineEdit.__init__( self, *args)        
    
    def focusOutEvent(self, event):
        if self.text() == "//":
            self.setStyleSheet('QLineEdit { background-color: %s }' % '#ffffff')
        elif self.hasAcceptableInput() == False:
            QtWidgets.QToolTip.showText(self.mapToGlobal(QtCore.QPoint()), "Entrada inválida. A data deve ser no formado dd/mm/yyyy")
            self.setStyleSheet('QLineEdit { background-color: %s }' % '#f6989d')
        else:
            QtWidgets.QToolTip.hideText()
            self.setStyleSheet('QLineEdit { background-color: %s }' % '#c4df9b')
                
        super(LineEdit_DateMask, self).focusOutEvent(event)

class TextEdit_DropFormulas(QtWidgets.QTextEdit):
    def __init__(self, *args, **kwargs):
        QtWidgets.QTextEdit.__init__(self, *args, **kwargs)
        regexp = QtCore.QRegExp("[^\'\"¨&\[\]{};`~?|!@#$\\=]*") 
        self.validator = QRegExpValidator(regexp)
        
    def keyPressEvent(self, event):        
        keypress = self.validator.validate(event.text(), 0)
        if keypress[0] == QValidator.Acceptable or event.key() == QtCore.Qt.Key_Backspace:
            QtWidgets.QTextEdit.keyPressEvent(self, event)  
            
    def dragEnterEvent(self, event):
        if isinstance(event.source(), QtWidgets.QListWidget):
            event.accept()
            self.setAcceptDrops(True)
            event.acceptProposedAction()
    
    def dragMoveEvent (self, event):
        if isinstance(event.source(), QtWidgets.QListWidget):
            event.accept()

    def dropEvent(self, event):        
        if isinstance(event.source(), QtWidgets.QListWidget):
            listwidget = event.source()
            item = listwidget.item(listwidget.currentRow())
                                   
            if listwidget.objectName() == "listwidget_formulas_constants":
                text = item.data(QtCore.Qt.UserRole).name
            if listwidget.objectName() == "listwidget_formulas_variables":
                
                text = item.data(QtCore.Qt.UserRole).keyword
                
            self.insertHtml("[")    
            self.insertHtml("<span style='font-size:8pt; color:#00aa00;'>" + text)                     
            self.insertHtml("]")           
            
            self.setFocus()            
            cursor = QTextCursor(self.document()) 
            cursor.movePosition(QTextCursor.End)   
            self.setTextCursor(cursor)
            
    
class ListWidget_DropVariables(QtWidgets.QListWidget):
    
    def __init__(self, *args, **kwargs):
        QtWidgets.QListWidget.__init__(self, *args, **kwargs)        
               
    def dragMoveEvent (self, event):
        if isinstance(event.source(), QtWidgets.QListWidget):
            event.accept()

    def dropEvent(self, event):        
        if isinstance(event.source(), QtWidgets.QListWidget):                     
            super(ListWidget_DropVariables, self).dropEvent(event)
            for index in range(self.count()):
                item = self.item(index)
                item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable) 
            
                                
        