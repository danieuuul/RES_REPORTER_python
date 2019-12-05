import h5py
import Model
import xarray as xr
import pandas as pd
import numpy as np
from Util import SR3Helper



class SR3Reader:
    
    def importModel(fileSR3):
        newModel = Model.Modelo()
        newModel.fileSR3 = fileSR3
        newModel.name = fileSR3.split('/')[-1] 
        newModel.timesteps = "ALL"
        newModel.timesteps_indexes = "ALL"
        newModel.general = SR3Reader.importGeneralInfos_fromModel(newModel)
         
        return newModel
    
    def importGeneralInfos_fromModel(model):
        general = Model.General()
        with h5py.File(model.fileSR3, 'r') as f:
            general.sim_info = {i: v.decode('utf-8') for i, v in f.attrs.items()}
            
            general.masterTimeTable = pd.DataFrame(f['General/MasterTimeTable'].value).set_index('Index')    
            
            general.unitsConversionTable = pd.DataFrame(f['General/UnitConversionTable'].value)
            general.unitsConversionTable.loc[:, 'Unit Name'] = general.unitsConversionTable.loc[:, 'Unit Name'].apply(lambda s: s.decode('utf-8'))
    
            general.unitsTable = pd.DataFrame(f['General/UnitsTable'].value)
            general.unitsTable.loc[:, 'Dimensionality'] = general.unitsTable.loc[:,'Dimensionality'].apply(lambda s: s.decode('utf-8'))
            general.unitsTable.loc[:, 'Output Unit'] = general.unitsTable.loc[:,'Output Unit'].apply(lambda s: s.decode('utf-8'))
            general.unitsTable.loc[:, 'Internal Unit'] = general.unitsTable.loc[:,'Internal Unit'].apply(lambda s: s.decode('utf-8'))
    
            general.nameRecordTable = pd.DataFrame(f['General/NameRecordTable'].value).applymap(lambda x: x.decode() if type(x) == bytes else x)
            
            return general    
    
    def getTimesteps(model, timeseriesType):      
        with h5py.File(model.fileSR3, 'r') as f: 
            all_timesteps = f['/TimeSeries/' + timeseriesType + '/Timesteps'].value

        if model.timesteps != "ALL":
            temp = model.timesteps
            timesteps = []
            for ts in temp:
                if ts in all_timesteps:
                    timesteps.append(ts)
            return timesteps
        else:
            return all_timesteps
    
    def getTimestepsIndexes(model, timeseriesType):          
        if model.timesteps == "ALL":
            model.timesteps = SR3Reader.getTimesteps(model, timeseriesType)
            
        with h5py.File(model.fileSR3, 'r') as f: 
            df = pd.DataFrame(f['/TimeSeries/' + timeseriesType + '/Timesteps'].value)
        df.columns = ['Timestep']
        
        return df.loc[df['Timestep'].isin(model.timesteps)].index.tolist()     

    def getTimestepIndex_byTimestep(model, timeseriesType, timestep):          
        with h5py.File(model.fileSR3, 'r') as f: 
            df = pd.DataFrame(f['/TimeSeries/' + timeseriesType + '/Timesteps'].value)
        df.columns = ['Timestep']
        
        return df.loc[df['Timestep'] == timestep].index[-1]
            
    def getDatesOffsets(model, timeseriesType):
        model.timesteps = SR3Reader.getTimesteps(model, timeseriesType)

        times = {col: model.general.masterTimeTable.loc[model.timesteps, col].values for col in model.general.masterTimeTable.columns}
        dates = times['Date']
        offsets = times['Offset in days']            
        dates = pd.to_datetime(dates, format="%Y%m%d") + pd.to_timedelta(dates - np.floor(dates), unit='D')
        
        return dates, offsets
        
    def getTimesteps_byDates(model, startDate, endDate, daysofMonth = [i for i in range(1,32)]):
        dates_dict = {pd.to_datetime(model.general.masterTimeTable.loc[index, 'Date'], format="%Y%m%d") 
         + pd.to_timedelta(model.general.masterTimeTable.loc[index, 'Date'] 
                           - np.floor(model.general.masterTimeTable.loc[index, 'Date']), unit='D'): index  
                           for index in model.general.masterTimeTable.index.tolist()}
        timesteps = []
        for date, index in dates_dict.items():
            if date >= startDate and date <= endDate and date.day in daysofMonth:
                timesteps.append(index)
        
        return timesteps
    
    def getTimestep_byDate(model, date):
        dates_dict = {pd.to_datetime(model.general.masterTimeTable.loc[index, 'Date'], format="%Y%m%d") 
         + pd.to_timedelta(model.general.masterTimeTable.loc[index, 'Date'] 
                           - np.floor(model.general.masterTimeTable.loc[index, 'Date']), unit='D'): index  
                           for index in model.general.masterTimeTable.index.tolist()}
        for date_, index in dates_dict.items():
            if date == date_:
                if index == 0:
                    return index + 1
                else:
                    return index
        
        return None
        
    def getAllGroups(model):    
        if model.groupTable.empty or model.wellTable.empty:
            SR3Reader.importGroupAndWellTable_fromModel(model)
        return list(model.groupTable['Name'])
    
    def importGroupAndWellTable_fromModel(model):
        with h5py.File(model.fileSR3, 'r') as f: 
            model.groupTable = pd.DataFrame(f['/TimeSeries/GROUPS/GroupTable'].value)
            model.wellTable = pd.DataFrame(f['/TimeSeries/WELLS/WellTable'].value)
              
        model.groupTable.loc[:, 'Name'] = model.groupTable.loc[:,'Name'].apply(lambda s: s.decode('utf-8'))
        model.groupTable.loc[:, 'Parent'] = model.groupTable.loc[:,'Parent'].apply(lambda s: s.decode('utf-8'))
        model.wellTable.loc[:, 'Name'] = model.wellTable.loc[:,'Name'].apply(lambda s: s.decode('utf-8'))
        model.wellTable.loc[:, 'Parent'] = model.wellTable.loc[:,'Parent'].apply(lambda s: s.decode('utf-8'))
    
    def getWells_byParent(model, parent):
        temp = []
        wells = []

        if model.groupTable.empty or model.wellTable.empty:
            SR3Reader.importGroupAndWellTable_fromModel(model)
        
        temp = list(model.groupTable[model.groupTable['Parent'] == parent]['Name'])
        if (len(temp) > 0):
            for t in temp:
                if len(model.groupTable[model.groupTable['Parent'] == t].index) > 0:
                    wells = SR3Reader.getWells_byParent(model, t)
                else:
                    wells = wells + list(model.wellTable[model.wellTable['Parent'] == t]['Name'])
        else:
            wells = list(model.wellTable[model.wellTable['Parent'] == parent]['Name'])
                        
        return wells
        
    def importVariables(model, timeseriesType, variables_list = "ALL"):
        variables = []

        with h5py.File(model.fileSR3, 'r') as f: 
            variables_temp = [s.decode() for s in f['/TimeSeries/' + timeseriesType + '/Variables'].value]
                
        for i in range (0, len(variables_temp)):
            if variables_temp[i] != "":
                if variables_list == "ALL":
                    variable = Model.Variable()
                    variable.id = i
                    variable.keyword = variables_temp[i]
                    if variable.keyword in model.general.nameRecordTable.Keyword.values:
                        variable.name = model.general.nameRecordTable[model.general.nameRecordTable.Keyword == variable.keyword]['Name'].values[0]
                        variable.gain, variable.offset = SR3Helper.conversion_gain_offset(model.general, variable.keyword)
                        variable.outputUnit = SR3Helper.get_output_unit(model.general, variable.keyword)
                    else:
                        variable.name = variable.keyword
                        variable.gain, variable.offset = SR3Helper.conversion_gain_offset(model.general, variable.keyword.split('(')[0])
                        variable.outputUnit = SR3Helper.get_output_unit(model.general, variable.keyword.split('(')[0])
                    variables.append(variable)                    
                else:
                    if variables_temp[i] in variables_list:
                        variable = Model.Variable()
                        variable.id = i
                        variable.keyword = variables_temp[i]
                        if variable.keyword in model.general.nameRecordTable.Keyword.values:
                            variable.name = model.general.nameRecordTable[model.general.nameRecordTable.Keyword == variable.keyword]['Name'].values[0]
                            variable.gain, variable.offset = SR3Helper.conversion_gain_offset(model.general, variable.keyword)
                            variable.outputUnit = SR3Helper.get_output_unit(model.general, variable.keyword)
                        else:
                            variable.name = variable.keyword
                            variable.gain, variable.offset = SR3Helper.conversion_gain_offset(model.general, variable.keyword.split('(')[0])
                            variable.outputUnit = SR3Helper.get_output_unit(model.general, variable.keyword.split('(')[0])
                        variables.append(variable)
        return variables
                        
        
    def getVariable_byKeyword(model, timeseriesType, keyword):
        with h5py.File(model.fileSR3, 'r') as f: 
            variables_temp = [s.decode() for s in f['/TimeSeries/' + timeseriesType + '/Variables'].value]
        
        for i in range (0, len(variables_temp)):
            if keyword == variables_temp[i]:
                variable = Model.Variable()
                variable.id = i
                variable.keyword = variables_temp[i]
                if variable.keyword in model.general.nameRecordTable.Keyword.values:
                    variable.name = model.general.nameRecordTable[model.general.nameRecordTable.Keyword == variable.keyword]['Name'].values[0]
                    variable.gain, variable.offset = SR3Helper.conversion_gain_offset(model.general, variable.keyword)
                    variable.outputUnit = SR3Helper.get_output_unit(model.general, variable.keyword)
                else:
                    variable.name = variable.keyword
                    variable.gain, variable.offset = SR3Helper.conversion_gain_offset(model.general, variable.keyword.split('(')[0])
                    variable.outputUnit = SR3Helper.get_output_unit(model.general, variable.keyword.split('(')[0])
                return variable
        
        return None
                        
    def importOrigins(model, timeseriesType, origins_list = "ALL"):
        origins = []

        with h5py.File(model.fileSR3, 'r') as f: 
            origins_temp = [s.decode() for s in f['/TimeSeries/' + timeseriesType + '/Origins'].value]
            
        for i in range (0, len(origins_temp)):
            if origins_list != "ALL":
                if origins_temp[i] in origins_list and origins_temp[i] != "":
                    origin = Model.Origin()
                    origin.id = i
                    origin.name = origins_temp[i]
                    origins.append(origin)
            else:
                origin = Model.Origin()
                origin.id = i
                origin.name = origins_temp[i]
                origins.append(origin)
                
        return origins
    
    def getOrigin_byName(model, timeseriesType, name):
        with h5py.File(model.fileSR3, 'r') as f: 
            origins_temp = [s.decode() for s in f['/TimeSeries/' + timeseriesType + '/Origins'].value]
        
        for i in range (0, len(origins_temp)):
            if name == origins_temp[i]:
                origin = Model.Origin()
                origin.id = i
                origin.name = origins_temp[i]
                return origin
        
        return None
    
        
    def importTimeSeries_toXarray(models, timeseriesType, variables_list = "ALL", origins_list = "ALL"):      
        units = {}
        dates = []
        lista_ds = []
        for model in models:      
            with h5py.File(model.fileSR3, 'r') as f:                
                dates, offsets = SR3Reader.getDatesOffsets(model, timeseriesType)
                # POR UMA LIMITAÇÃO NA FUNÇÃO F DA BIBLIOTECA H5PY, NÃO É POSSÍVEL ESCOLHER MAIS DE UMA LISTA PARA BUSCAR
                # SENDO ASSIM, POR CAUSA DE PERFORMANCE, OPTEI POR RETORNAR TODAS AS ORIGINS QUANDO FOR ESCOLHIDO UMA LISTA DE TIMESTEPS                 
                if model.timesteps == "ALL":
                    origins = SR3Reader.importOrigins(model, timeseriesType, origins_list)                    
                else:
                    origins = SR3Reader.importOrigins(model, timeseriesType, "ALL") 
                                        
                origins_names = []
                origins_keys = []
                
                lista_offset_pd = []
                for origin in origins:
                    origins_names.append(origin.name)
                    origins_keys.append(origin.id)
                    lista_offset_pd.append(pd.DataFrame(offsets))
                offset_dataframe = pd.concat(lista_offset_pd, axis = 1)    
                               
                ds = xr.Dataset(coords={'MODEL': model.name, 'ORIGIN': origins_names, 'DATE': dates})   
                ds.coords['DATE'] = dates
                
                ds['OFFSET'] = (('DATE', 'ORIGIN'), offset_dataframe)
                units['OFFSET'] = "day" 
                
                ds.attrs['Units'] = units
                
                variables = SR3Reader.importVariables(model, timeseriesType, variables_list)                                                        
                for var in variables:
                    if var.outputUnit is not None:
                        units[var.keyword] = var.outputUnit
                        ds.attrs['Units'] = units
                
                    if model.timesteps == "ALL":
                        ds[var.keyword] = (('DATE', 'ORIGIN'), (f['/TimeSeries/' + timeseriesType + '/Data'][:, var.id, origins_keys] * var.gain + var.offset))                                                  
                    else:
                        timesteps_indexes = SR3Reader.getTimestepsIndexes(model, timeseriesType)
                        ds[var.keyword] = (('DATE', 'ORIGIN'), (f['/TimeSeries/' + timeseriesType + '/Data'][timesteps_indexes, var.id, :] * var.gain + var.offset))                                                  
                                                
                        
                    ds.attrs['MODEL'] = model.name                
                                        
                lista_ds.append(ds)
        
        
        units = {}     
        units = lista_ds[0].attrs['Units']
            
        lista_df = [k.to_dataframe() for k in lista_ds]
        df_union = pd.concat(lista_df, axis = 0)
        
        df_union.set_index(['MODEL'], append=True, inplace= True)

        if origins_list != "ALL":
            df_union = df_union[df_union.index.get_level_values('ORIGIN').isin(origins_list)]

        ds = df_union.to_xarray()             
                
        return ds, units
    
    
    def getDataValue_fromTimeSeries(model, timeseriesType, date, variable_keyword, origin_name):
        with h5py.File(model.fileSR3, 'r') as f:                                              
            timestep = SR3Reader.getTimestep_byDate(model, date)                                          
            origin = SR3Reader.getOrigin_byName(model, timeseriesType, origin_name)                                          
            variable = SR3Reader.getVariable_byKeyword(model, timeseriesType, variable_keyword)          
            timestep_index = SR3Reader.getTimestepIndex_byTimestep(model, timeseriesType, timestep)
            data = f['/TimeSeries/' + timeseriesType + '/Data'][timestep_index, variable.id, origin.id] * variable.gain + variable.offset   

        return data
        

