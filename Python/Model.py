import pandas as pd

class Modelo():
    def __init__(self):
        self.general = None
        self.name = ""
        self.fileSR3 = ""
        self.timesteps = []
        self.wellTable = pd.DataFrame()
        self.groupTable = pd.DataFrame()
        self.timesteps_indexes = []

class General():    
    def __init__(self):        
        self.sim_info = {}            
        self.masterTimeTable = pd.DataFrame()               
        self.unitsConversionTable = pd.DataFrame()
        self.unitsTable = pd.DataFrame()
        self.nameRecordTable = pd.DataFrame()
                          
class Variable:       
    def __init__(self):        
        self.id = ""
        self.keyword = ""
        self.name = ""
        self.alias = ""
        self.gain = None
        self.offset = None
        self.outputUnit = ""
        self.timeseriesType= ""
          
class Origin:    
    def __init__(self):        
        self.id = ""
        self.name = "" 


class Formula:    
    def __init__(self):        
        self.name = ""         
        self.expression = ""        
        self.timeseriesType = ""
        
        self.variablesKeywords = []
        self.constants = []
    
class Constant:    
    def __init__(self, name = "", value = "", type_ = ""):                
        self.name = ""     
        self.value = ""
        self.type_ = ""


class Graph:    
    def __init__(self):                
        self.name = ""   
        self.models = []
        self.timeseriesType = ""
        self.origins = []
        self.variables = []
        self.formulas = []
        self.cathegoryType = ""
        self.columnType = ""
        self.dataframe = pd.DataFrame()
        self.html = ""

class Set:
    def __init__(self):
        self.name = ""   
        self.models = []
        self.timeseriesType = ""
        self.origins = []
        self.variables = []
        self.formulas = []
    
        