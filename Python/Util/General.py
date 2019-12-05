import os
import shutil
import subprocess

def copyFile(src, dst, buffer_size=10485760, perserveFileDate=True):
   
    #    Optimize the buffer for small files
    buffer_size = min(buffer_size, os.path.getsize(src))
    if(buffer_size == 0):
        buffer_size = 1024
   
    if shutil._samefile(src, dst):
        return
    for fn in [src, dst]:
        try:
            st = os.stat(fn)
        except OSError:
            pass
        else:
            if shutil.stat.S_ISFIFO(st.st_mode):
                raise shutil.SpecialFileError("`%s` is a named pipe" % fn)
    with open(src, 'rb') as fsrc:
        with open(dst, 'wb') as fdst:
            shutil.copyfileobj(fsrc, fdst, buffer_size)
   
    if(perserveFileDate):
        shutil.copystat(src, dst)


def copyFileList(arquivos):
    arquivos_temp = []
    for arquivo in arquivos:
        aux = arquivo.split("\\")
        
        src = arquivo
        dst = aux[-1]        

        if not os.path.isfile(dst) :
            copyFile(src, dst)        
        
        arquivos_temp.append(dst)

    return arquivos_temp


def copyFile_SUBPROCESS(src, dst):
    
    subprocess.Popen("copy " + src + " " + dst, shell = True)        
        
    return dst

def copyFileList_SUBPROCESS(arquivos):
    arquivos_temp = []
    for arquivo in arquivos:
        aux = arquivo.split('\\')
        
        src = arquivo
        dst = aux[-1]
        subprocess.Popen("copy " + src + " " + dst, shell = True)
        
        arquivos_temp.append(dst)
        
    return arquivos_temp
    
    
def Insert_row(row_number, df, row_value): 
    # Starting value of upper half 
    start_upper = 0
   
    # End value of upper half 
    end_upper = row_number 
   
    # Start value of lower half 
    start_lower = row_number 
   
    # End value of lower half 
    end_lower = df.shape[0] 
   
    # Create a list of upper_half index 
    upper_half = [*range(start_upper, end_upper, 1)] 
   
    # Create a list of lower_half index 
    lower_half = [*range(start_lower, end_lower, 1)] 
   
    # Increment the value of lower half by 1 
    lower_half = [x.__add__(1) for x in lower_half] 
   
    # Combine the two lists 
    index_ = upper_half + lower_half 
   
    # Update the index of the dataframe 
    df.index = index_ 
   
    # Insert a row at the end 
    df.loc[row_number] = row_value 
    
    # Sort the index labels 
    df = df.sort_index() 
   
    # return the dataframe 
    return df 

def split(txt, seps, lista):
    txt = txt.replace(" ", "")
    print(txt)
    unidades = {'metro': 'm', 'kilo': 'kg'}
    flag = 0
    pos = 0
    while pos < len(txt):
        if txt[pos] in seps:
            operador = txt[pos]
            atual = txt.split(txt[pos])[0]
            if atual != "":
                if atual in unidades.keys():
                    lista.append(unidades[atual])                
                else:
                    lista.append(atual)
            lista.append(operador)
            proximo = txt[pos+1:]
            split(proximo, seps, lista)
            flag = 1
            break
        pos = pos + 1
    if flag == 0:
        if txt in unidades.keys():
            lista.append(unidades[txt])    
    return lista
                           

def expression_unit_simplified(expression, units):
    op_permanent = ["*", "/"]
    op_temp = ["(", ")", "+", "-"]
    expression = expression.replace(" ", "")
    expression_list = []
    pos = 0
    buffer = ""
    buffer_operator = ""
    actual_unit = ""
    
    while pos < len(expression):
        buffer = buffer + expression[pos]
        if (pos + 1 == len(expression) or expression[pos + 1] in op_permanent + op_temp) and buffer in units.keys():
            if units[buffer] != actual_unit:
                expression_list.append(buffer_operator)
                expression_list.append(units[buffer])
                actual_unit = units[buffer]
                buffer = ""
                buffer_operator = ""
            else:
                buffer = ""
        if expression[pos] in op_permanent:
            buffer_operator = expression[pos]
            actual_unit = ""
            buffer = ""
        if buffer in op_temp:
            buffer = ""
            
        
        pos = pos + 1
        
    result = ""
    result = result.join(expression_list)
              
    return result 




    