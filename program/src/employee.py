'''Import the packages'''
from datetime import date
import numpy as np
import pandas as pd
from src.functions import get_uuid4

class GetEmploeey:
    '''
    Loads the main HR spreadsheet that contains employee data.
    From this spreadsheet the construction of the others.
    Generates the employees' sheet with the unique ID, used in all other sheets.
    '''
    def __init__(self) -> None:
        pass

    #--------------------Reading Dataframe--------------------#
    data = pd.read_excel("planilhas\\rh_main.xlsx")

    data['employee_id'] = '' # Creat the new column on dataframe
    data['leader_id'] = ''

    today = date.today().strftime("%m-%d-%Y")

    data.replace('',np.nan,inplace=True)

    # Generates random Id's to fill the ID Column of the main spreadsheet
    get_uuid4(data,'Nome Funcionário','employee_id')

    #--------------------Generating the Employee Spreadsheet--------------------#
    employee_sheet = pd.DataFrame({'id': data['employee_id'],
                                'Nome': data['Nome Funcionário'],
                                'Telefone': data['Celular'],
                                'Email': data['E-Mail'],
                                'Situação': data['Situação'],
                                'Criado_em':today,
                                'Upload_em':today})

    # Save the new spreadsheet
    employee_sheet.to_csv('program\\output_sheets\\funcionarios.csv', index=False)
    