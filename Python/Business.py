import Model
from Util import ExpressionParser
from SR3Reader import SR3Reader
import pandas as pd


class Business:
 
# -------------------------------------------- MODEL--------------------------------------------------------
    
    def importModel(self, file):
        return SR3Reader.importModel(file)    
    
    
    def importGroupAndWellTable(model):
        return SR3Reader.importGroupAndWellTable(model)

# -------------------------------------------- VARIABLE ---------------------------------------------------
    
    def importVariables(self, model, timeseriesType):
        return SR3Reader.importVariables(model, timeseriesType)
    
# -------------------------------------------- ORIGINS --------------------------------------------------------
    
    def importOrigins(self, model, timeseriesType):
        return SR3Reader.importOrigins(model, timeseriesType)
    
    def getAllGroups(self, model):       
        return SR3Reader.getAllGroups(model)
        
    def getWells_byParent(self, model, parent):                    
        return SR3Reader.getWells_byParent(model, parent)
        
                    
# -------------------------------------------- FORMULA --------------------------------------------------------
    
    def getFormula_fromList_byName(self, formula_list, name):
        for f in formula_list:
            if f.name == name:
                return f
        return None
    
    def getFormulaList_fromList_byTimeseriesType(self, formula_list, timeseriesType):
        formulas = []
        for f in formula_list:
            if f.timeseriesType == timeseriesType:                
                formulas.append(f)
        return formulas
    
    
    def addFormula(self, formula_list, name, expression, variables = [], constants = {}):
        formula = Model.Formula()
        formula.name = name
        formula.expression = expression
        formula.variables = variables
        formula.constants = constants
        formula_list.append(formula)
        
        return formula_list
    
        
    def getParams_byFormulaExpression(self, formulaExpression):
        parser = ExpressionParser.Parser()
        
        expr = parser.parse(formulaExpression)        
        params = []
        for p in expr.variables():
            params.append(p)
        
        return params
    
# -------------------------------------------- CONSTANT --------------------------------------------------------

    def constantValue_toString(self, constant):
        value = ""
        if constant.type_ == "Número":
                value = str(constant.value)
        elif constant.type_ == "Data":
                value = constant.value.strftime("%d/%m/%Y")        
        
        return value
    
    def getConstant_fromList_byName(self, constantList, name):
        for c in constantList:
            if c.name == name:
                return c
        return None
    
    def getConstants_fromList_byParams(self, params, constant_list):
        constants = []
        for p in params:
            if p in [c.name for c in constant_list]:
                constants.append(self.getConstant_fromList_byName(constant_list, p))
        
        return constants
    
    def addConstant(self, constant_list, name, value, type_, timeseriesType = "", origin = "", date = ""):
        constant = Model.Constant()
        constant.name = name
        constant.value = value
        constant.type_ = type_
        constant.timeseriesType = timeseriesType
        constant.origin = origin
        constant.date = date
        constant_list.append(constant)
        
        return constant_list  
    
    
# -------------------------------------------- MODEL DATAFRAME --------------------------------------------------------
        
    def importTimeSeries_toXarray(self, models, timeseriesType, variables_list = "ALL", origins_list = "ALL"):
        return SR3Reader.importTimeSeries_toXarray(models, timeseriesType, variables_list, origins_list)
    
    def loadDataFrame(self, models, timeseriesType, variables_list = "ALL", origins_list = "ALL", formulas = [], configTimestepsParams = "ALL", configUnits = {}):
        parser = ExpressionParser.Parser()
        
        # SELECIONANDO AS VARÍAVEIS NECESSÁRIAS PARA AS FÓRMULAS
        variables_list_extras = []
        
        if variables_list != "ALL":                        
            for formula in formulas:
                try:
                    expr = parser.parse(formula.expression)    
                    for e in expr.variables():
                        if e not in variables_list:
                            variables_list_extras.append(e)  
                except:
                    pass
            variables_list = variables_list + variables_list_extras
        
        # SETANDO TIMESTEPS ESCOLHIDOS
        if configTimestepsParams != "ALL":
            startDate = configTimestepsParams[0]
            endDate = configTimestepsParams[1]
            daysofMonth = configTimestepsParams[2]   
            for model in models:
                if daysofMonth == []:
                    model.timesteps = SR3Reader.getTimesteps_byDates(model, startDate, endDate)
                else:
                    model.timesteps = SR3Reader.getTimesteps_byDates(model, startDate, endDate, daysofMonth)
        
        # IMPORTAR DATASET
        dataset, units = SR3Reader.importTimeSeries_toXarray(models, timeseriesType, variables_list, origins_list)
        
        # TRANSFORMAR DATASET EM DATAFRAME
        results = dataset.to_dataframe().fillna(0)        
        results = results.reset_index(level=[0, 1, 2])     
                        
        #UNIDADES 
        for u_var, u_unit in units.items():
            try:                                    
                if u_var in configUnits.keys():
                    units.update({u_var: configUnits[u_var]})            
                    multiplier = configUnits[u_var][1].replace(",", ".")
                    multiplier = float(multiplier)
                    results[u_var] = multiplier*results[u_var]
            except ValueError:
                pass

        # FÓRMULAS    
        for formula in formulas:            
            lista = []
            for k, df_temp in results.groupby(['MODEL', 'ORIGIN']):
#                try:                   
                    expr = parser.parse(formula.expression) 
                    params = {}
                    for var in expr.variables():
                        if var in formula.variables:
                            params.update({var: df_temp[var]})
                        elif var in [c.name for c in formula.constants]:
                            params.update({var: self.getConstant_fromList_byName(formula.constants, var).value})
                        else: 
                            pass
                    df_temp[formula.name] = expr.evaluate(params)
#                except Exception as e:
#                    df_temp[formula.name] = "Erro na fórmula: " + str(e.args[-1])                             
        
                    lista.append(df_temp)
            
            results = pd.concat(lista, axis = 0)    
        
        results.fillna(0, inplace = True)                
        
        # RETIRANDO COLUNAS ADICIONADAS PARA CÁLCULO DE FÓRMULAS
        columns = []
        for c in results.columns:
            if c not in variables_list_extras:
                columns.append(c)
            elif c  == 'DATE' or c == 'OFFSET':
                columns.append(c)
        results = results[columns]
                           
        return results, units        
    
    def orderDataFrame_byColumns(self, df, columnsInOrder = []):
        # ORDEM DAS COLUNAS
        columns_toOrder = ['MODEL', 'ORIGIN', 'DATE']
        for column in columnsInOrder:
            if column in df.columns and column not in columns_toOrder:
                columns_toOrder.append(column)
        
        newColumnsOrder = columns_toOrder + (df.columns.drop(columns_toOrder).tolist())       
        df = df[newColumnsOrder]
        
        return df
        
    
    def prepareFinalDataFrame(self, df, new_columns, units):
        df.fillna(0, inplace = True)                    

        # ORDEM E NOME DAS DAS COLUNAS - OBS: somente colunas em "new_columns" serão retornadas
    
        for original_name, new_name in new_columns.items():
            if original_name in df.columns:
                df = df.rename(columns = {original_name: new_name})
            
        df = df[[*new_columns.values()]]

        # ORDENAR DATAFRAME por Modelo, Origem e Data
        
        df.sort_values(by=['MODEL', 'ORIGIN', 'DATE'], inplace = True)
        df['DATE'] = df['DATE'].apply(lambda timestamp: timestamp.date().strftime("%d/%m/%Y"))  
                         
        
        return df

    def exportDataFrame_toExcel(self, df, output = "OUTPUT.xlsx", withIndex = False):
        df.to_excel(output, index = withIndex, columns = df.columns)
    
